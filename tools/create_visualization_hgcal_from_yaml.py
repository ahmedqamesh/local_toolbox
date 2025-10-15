#pip install PyYAML graphviz
#sudo apt install graphviz
import yaml
from graphviz import Digraph
import os
HOME_DIR=os.getcwd()
print("Current working directory:", os.getcwd())

# Define your input and output paths
input_yaml_path = HOME_DIR+"/tools/yaml_data/alpha_train_A6.yaml"
output_pdf_path = HOME_DIR+"/tools/yaml_data/hgcal_tileboard_A6_graph"
parent_frame_color = "#1C4587" # Darkblue
parent_fill_color = "#DAE8FC" # lightblue


child_frame_color ="#666666" # Darkgray
child_fill_color ="lightgray"

pin_frame_color = "#62874D" # Darkgreen
pin_fill_color = "#D5E8D4" # lightgreen

interface_frame_color = "#D6B656" # Darkyellow
interface_fill_color = "#FFF2CC"  # lightyellow

board_frame_color = "#DD442F" # red
board_fill_color = "#F8CECC" # lightred

# Load the YAML file
with open(input_yaml_path, "r") as f:
    data = yaml.safe_load(f)

# Initialize Graphviz
dot = Digraph(comment="HGCAL Configuration")
dot.attr(rankdir='LR',
         bgcolor='white',
         fontname='Helvetica', 
         splines='true')

# Track created nodes
created_nodes = set()

def add_legend(dot):
    with dot.subgraph(name='cluster_legend') as legend:
        legend.attr(label='', fontsize='2', fontname='Helvetica', style='dashed', color='gray')
        legend.attr(rank='sink')  # Pin to top of graph
        legend.attr(rankdir='TB')  # optional if you want horizontal layout elsewhere
        # Define legend items (label, color)
        table_rows = ""
        items = [
             ('Board', board_fill_color),
            ('Control', interface_fill_color),
            ('Pin', pin_fill_color),
            #('Child', child_fill_color),
            ('Chip', parent_fill_color),
        ]
        table_rows = '\n'.join(
            f'''
            <TR>
                <TD ALIGN="LEFT" WIDTH="16" HEIGHT="5" BGCOLOR="{color}"></TD>
                <TD ALIGN="LEFT"><FONT POINT-SIZE="10">{label}</FONT></TD>
            </TR>
            ''' for label, color in items
        )
        

        legend.node(
            'legend',
            label=f'''<
                <TABLE BORDER="0" CELLBORDER="0" CELLPADDING="0" CELLSPACING="2" ALIGN="LEFT">
                    {table_rows}
                </TABLE>
            >''',
            shape='plaintext'
        )

# Function to add a logo to the graph
def add_logo(dot, logo_path, logo_name="kitlogo_de_rgb.png"):
    logo_full_path = logo_path + logo_name

  # Create a subgraph to enforce top-left placement
    with dot.subgraph(name='cluster_logo') as logo_subgraph:
        #logo_subgraph.attr(rank='min')  # forces to the top of the graph
        logo_subgraph.attr(
            style='invis',  # hide cluster frame
            color='white'   # prevents default cluster border
        )
        logo_subgraph.node("logo", 
                           image=logo_full_path,
                           label="",
                           shape="none",
                           width="2", height="1", 
                           fixedsize="true")


def extract_formated_name(node_name):
    return node_name.replace(".", "_")

def extract_simple_type(type_string: str, Check_id: str):
    if not type_string:
        return ""
    s_clean = type_string.strip("()")
    Check_id_result = s_clean.endswith(Check_id)
    parts = s_clean.split(".") #.startswith
    # Always return the last part (most specific identifier)
    return parts[-1], Check_id_result


def build_node(node_name, label=None, n_lines=2):
    if node_name not in created_nodes:
        formatted_label = label or node_name
        if n_lines > 1 and '\n' in formatted_label:
            parts = formatted_label.split('\n', 1)
            part_1, _ = extract_simple_type(type_string = parts[1], Check_id = "emp")
            item_label =  parts[0]
            #print (f"{parts[1]}\n{parts[1][-4:]}")
            if part_1 == "group":
                frame_color = board_frame_color
                fill_color = board_fill_color
                item_label = item_label
            elif parts[0][0:3] == "pin" and part_1 != "group":
                frame_color = pin_frame_color
                fill_color = pin_fill_color
                item_label = item_label
            elif parts[0][0:3] == "i2c" and part_1 != "group":
                frame_color = interface_frame_color
                fill_color = interface_fill_color
                item_label = item_label + " Transport"
            elif parts[1][-4:] == "emp)" and part_1 != "group":
                frame_color = interface_frame_color
                fill_color = interface_fill_color
                item_label = item_label + " Control"
            else:
                item_label = item_label + " Chip"
                frame_color = parent_frame_color
                fill_color = parent_fill_color

            # Format the label with bold and italic
            formatted_label = f"<b>{item_label}</b><br/><i><font point-size='10'>({part_1})</font></i>"                
            dot.node(node_name, 
                     label=f"<{formatted_label}>", 
                     shape="box", 
                     style="rounded,filled", 
                     color=frame_color, 
                     fillcolor=fill_color)
        else:
            dot.node(node_name, 
                    label=label, 
                    shape="box", 
                    color=child_frame_color, 
                    style="rounded,filled")
        created_nodes.add(node_name)

def parse_yaml_tree(node_name = None, subtree= None, parent=None):
    # Recursive function to parse the YAML tree and create nodes
    extracted_node_name = extract_formated_name(node_name)  
    for k, v in subtree.items():
        # node_name: alpha_train
        # k : .ic_12
        if k not in ["type", "cfg", "transport", "carrier"]:
            #print(f"Processing node: {node_name}.{k} --- {v}")
            parse_yaml_tree(node_name = f"{node_name}.{k}", 
                            subtree = v,
                            parent=node_name)
        else: 
            pass

    if isinstance(subtree, dict):
        raw_type = subtree.get("type", "group")
        node_type = raw_type.replace("swamp.", "")
        child_label = node_name.split(".")[-1]
        label_name =f"{child_label}\n({node_type})"
        
        build_node(extracted_node_name, label=label_name)

        if "transport" in subtree: subtree_check = "transport"
        elif "carrier" in subtree: subtree_check = "carrier"
        else: subtree_check = False

        if subtree_check:
            subtree_value = subtree[subtree_check]
            if subtree_value.startswith(".."):
                parent_parts = parent.split(".")
                if len(parent_parts) >= 2: grandparent = ".".join(parent_parts[:-1])
                else: grandparent = parent_parts[0]  # fallback if structure is shallow
                # Step 2: Get raw target node_name like 'ec_12'
                raw_target = subtree_value.strip(".")
                # Step 3: Final target node path: e.g., alpha_train.ec_12
                full_target = f"{grandparent}_{raw_target}"
                
                target_node = extract_formated_name(raw_target)
                target_full = extract_formated_name(full_target)
                # Step 4: Check if raw node exists
                if target_full not in created_nodes:
                    build_node(node_name=target_node,
                               label="",
                               n_lines=1)
                    dot.edge(
                             target_node, 
                             extract_formated_name(node_name), 
                             color=child_frame_color, 
                             arrowhead="normal",  
                             #label=subtree_check, 
                             fontcolor=child_frame_color)
                else:
                    # Link to the actual full path node
                    # Relaed to EC and IC
                    dot.edge( 
                             target_full, 
                             extract_formated_name(node_name),
                             color=child_frame_color, 
                             arrowhead="normal", 
                             #dir="back",          
                             #label=subtree_check, 
                             fontcolor=child_frame_color)
                    
            if subtree_value.startswith(".") and not subtree_value.startswith(".."):
                parent_parts = parent.split(".")

                raw_target = subtree_value.strip(".")
                full_target = f"{parent}_{raw_target}"

                target_node = extract_formated_name(raw_target)
                target_full = extract_formated_name(full_target)

                dot.edge(
                         target_full, 
                         extract_formated_name(node_name), 
                         color=child_frame_color, 
                         arrowhead="normal", 
                         #dir="back", 
                         #label=subtree_check, 
                         fontcolor=child_frame_color)
        else:
            pass

    
        if parent :#and k.startswith("pin") == False:
            #part_1, Checked_id = extract_simple_type(type_string = parent, Check_id = "emp")
            #part_1, _ = extract_simple_type(type_string = parts[1], Check_id = "emp")
            dot.edge(extract_formated_name(parent), 
                    extracted_node_name, 
                    label="",
                    color=child_fill_color,
                    tailport="c",
                    headport="c",
                    style="dashed",
                    penwidth="0.4")
        else:
            pass  # No parent edge for top-level nodes


    elif isinstance(subtree, list):
        build_node(extracted_node_name, label=f"{node_name.split('.')[-1]}\n{str(subtree)}")
        if parent:
            dot.edge(extract_formated_name(parent), extracted_node_name, color=parent_frame_color)
        else: 
            pass  # No parent edge for top-level nodes
    # If the subtree is a list, iterate through its items
        for i, item in enumerate(subtree):
            parse_yaml_tree(node_name = f"{node_name}[{i}]", 
                            subtree=item,
                            parent=node_name)
    else:
        # Handle scalar value (leaf node)
        build_node(extracted_node_name, label=f"{node_name.split('.')[-1]}",n_lines=1)

        if parent:
            dot.edge(extract_formated_name(parent), extracted_node_name, color=parent_frame_color)
        else: 
            pass

# Call the legend function
add_legend(dot)

# Run tree walker from top-level keys
for section in data:
    if section != "__meta__" : 
        # Exclude metadata section
        parse_yaml_tree(node_name = section, 
                        subtree=data[section],
                        parent=None)
# Add the logo
add_logo(dot, logo_path=HOME_DIR + "/tools/yaml_data/")


# Output the graph to PDF
dot.render(output_pdf_path, format="pdf", cleanup=True)
print(f"✅ Graph saved to: {output_pdf_path}.pdf")
