########################################################
"""
    This file is part of the MOPS-Hub project.
    Author: Ahmed Qamesh (University of Wuppertal)
    email: ahmed.qamesh@cern.ch  
    Date: 01.05.2023
"""
########################################################
import sys
import os
import time
import csv
import pandas as pd
import re

rootdir = os.path.dirname(os.path.abspath(__file__)) 
sys.path.insert(0, rootdir+'/mopshub')


def remove_after_character(input_string, character):
    # Find the index of the character
    index = input_string.find(character)
    # If the character is found, remove everything after it
    if index != -1:result = input_string[:index]
    # If the character is not found, return the original string
    else:result = input_string
    return result



def extract_ports(file_path = None,files = None, file_type="verilog"):
    for vfile in files:
        with open(file_path+vfile, 'r') as file:
            #verilog_code = file.read()
            lines = file.readlines()
            # Process each line and extract the parameter values
            output_dict = {}
            input_dict  = {}
            for i in range(len(lines)):
                line= lines[i].strip()  # Remove leading/trailing whitespaces
                if file_type == "verilog":
                    if line.startswith('module') and i < len(lines) - 1:
                        new_line = remove_after_character(line,"#")
                        new_line = remove_after_character(new_line,"(")
                        _, module_name = new_line.split('module')
                    
                    elif line.startswith('input') and i < len(lines) - 1:
                        
                        # Check for comments
                        if '//' in line: comment = line.split('//')[1].strip()  # Extract comment
                        else: comment = "-"   
                        comment = comment.replace("_","\_")
                        
                        line = line.rstrip(',;')  # Remove "," or ";" from the end of the line
                        
                        if  line.find('reg')!= -1: type = "reg"
                        elif  line.find('wire') != -1: type = "wire"
                        else: type = "None"
                        
                        new_line = remove_after_character(line,"//")
                        port, invalue = new_line.split(type)  # Split the line at "reg"
                        port = port.strip()  # Remove leading/trailing whitespaces from the key
                        
                        invalue = invalue.replace("_","\_")#depends on the size of the statedeb
                        
                
                        match_array = re.findall(r'\[(\d+:\d+)\]', invalue)
                        match_array = "["+str(match_array)[2:-2]+"]"
                        
                        if match_array: invalue = invalue.replace(str(match_array),"")
                        if len(match_array) <=2: match_array = ""
                        invalue = invalue.strip()  # Remove leading/trailing whitespaces from the invalue
                        invalue = invalue.rstrip(',') 
                        
                        input_dict[invalue] = {'type': type, 'value': invalue, 'match_array': match_array, 'comment': comment}
                        
                    elif line.startswith('output') and i < len(lines) - 1:
                        # Check for comments
                        if '//' in line: comment = line.split('//')[1].strip()  # Extract comment
                        else: comment = "-"
                        
                        line = line.rstrip(',;')  # Remove "," or ";" from the end of the line
                        if  line.find('reg')!= -1: type = "reg"
                        elif  line.find('wire') != -1: type = "wire"
                        else: type = "None"
                        new_line = remove_after_character(line,"//")
                        port, outvalue = new_line.split(type)  # Split the line at "="
                        port = port.strip()  # Remove leading/trailing whitespaces from the key
                        outvalue = outvalue.replace("_","\_")#depends on the size of the statedeb
                
                        match_array = re.findall(r'\[(\d+:\d+)\]', outvalue)
                        match_array = "["+str(match_array)[2:-2]+"]"
                        if match_array: outvalue = outvalue.replace(str(match_array),"")
                        if len(match_array) <=2: match_array = ""
                        outvalue = outvalue.strip()  # Remove leading/trailing whitespaces from the outvalue
                        outvalue = outvalue.rstrip(',') 
                        output_dict[outvalue] = {'type': type, 'value': outvalue, 'match_array': match_array, 'comment': comment}
                if file_type == "vhdl":
                        # VHDL Parsing Logic
                        if "entity" in line and "is" in line:
                            new_line = remove_after_character(line, "is")
                            module_name = new_line.split("entity")[-1].strip()

                        elif "port" in line:
                            # Find the input/output direction and extract the ports
                            if "in" in line:
                                direction = "in"
                            elif "out" in line:
                                direction = "out"
                            else:
                                continue
                            
                            # Check for comments
                            comment = "-"
                            if '--' in line:
                                comment = line.split('--')[1].strip()

                            line = line.rstrip(',;')
                            type = "signal"
                            if "std_logic" in line:
                                type = "std_logic"
                            elif "std_logic_vector" in line:
                                type = "std_logic_vector"

                            new_line = remove_after_character(line, "--")
                            port, invalue = new_line.split(type)
                            port = port.strip()

                            invalue = invalue.replace("_", "\_")
                            
                            match_array = re.findall(r'\(\d+ downto \d+\)', invalue)
                            match_array = "[" + str(match_array)[2:-2] + "]"

                            if match_array:
                                invalue = invalue.replace(str(match_array), "")
                            if len(match_array) <= 2:
                                match_array = ""
                            invalue = invalue.strip().rstrip(',')
                            input_dict[invalue] = {'type': type, 'value': invalue, 'match_array': match_array, 'comment': comment}

                        elif "end" in line:
                            # If "end" is found, end the current module (optional).
                            pass                  
                else:
                    pass 
            # Print the dictionary
            output_string = ""
            for port, values in output_dict.items():
                port = values['value']
                match_array = values['match_array']
                comment = values['comment']
                output_string += f"{port}"+"/{"+f"{match_array}"+"}/"+f"{comment},"
                
            # Print the dictionary
            input_string = ""
            for port, values in input_dict.items():
                port = values['value']
                match_array = values['match_array']
                comment = values['comment']
                input_string += f"{port}"+"/{"+f"{match_array}"+"}/"+f"{comment},"
            
            
            len_output_dict =  len(output_dict)
            len_input_dict =  len(input_dict)
            if len_output_dict > len_input_dict : entity_size = len_output_dict
            else: entity_size = len_input_dict
            module_name = module_name.replace("_","\_")#depends on the size of the statedeb
            title_latex = """    \\node[draw=lcnorm, rectangle, rounded corners, minimum width=\\entitywidth cm, minimum height=1cm, fill=gray!40, font=\\Large\\bfseries,line width=2pt] (title) 
                        at (0,0) {\\textcolor{white}{\\textbf{"""+f"{module_name}"+"}}};"
            
            input_latex = "      \\pgfmathsetmacro{\\entitysize}{"+f"{entity_size}"+"}\n"+"        \\foreach \port/\label/\inComment [count=\i] in {"+f"{input_string[:-1]}"+"}{"+"""
                    \\node[port, anchor=west] at ([xshift = -0.2cm , yshift=\i*\\verticalshift cm]title.west) {
                    \\nodepart[align=left]{two}\\textcolor{lcnorm}{\\texttt{wire}\\texttt{\label}}
                    \\nodepart{one}\\tikz \\node[lwire]{};};
                    \\node[port, anchor=east] at ([xshift = -0.4cm , yshift=\i*\\verticalshift cm] title.west) {
                    \\nodepart[align=right]{two}\\textcolor{lcnorm}{\\texttt{\port}}};
                    \\node[port, anchor=west] at ([xshift = 0.1cm , yshift=-7.5+\i*\\verticalshift cm] title.west) {
                    \\nodepart[align=left]{two}\\textcolor{red}{\\texttt{\inComment}}};
                    }
            """
                        
            output_latex = "        \\foreach \port/\label/\outComment [count=\i] in {"+f"{output_string[:-1]}"+"}{"+"""
                    \\node[port, anchor=east] at ([xshift = \\rightportwidth cm , yshift=\i*\\verticalshift cm]title.west) {
                    \\nodepart[align=left]{one}\\textcolor{lcnorm}{\\texttt{\label}\\texttt{wire}}
                    \\nodepart{two}\\tikz \\node[lwire]{}; };
                    \\pgfmathsetmacro{\\rightlabelwidth}{\entitywidth+0.4}
                    \\node[port, anchor=west] at ([xshift =\\rightlabelwidth cm , yshift=\i*\\verticalshift cm] title.west) {
                    \\nodepart[align=left]{one}\\textcolor{lcnorm}{\\texttt{\port}}};
                    \\node[port, anchor=east] at ([xshift =\\rightlabelwidth cm , yshift=-7.5+\i*\\verticalshift cm] title.west){
                    \\nodepart[align=left]{one}\\textcolor{red}{\\texttt{\outComment}}};
                    }
            """
            print(f"\n======================[{module_name}]===================================\n",
                  title_latex,
                  "\n     %Input Ports\n ",
                  input_latex,"\n    ",
                  "%Output Ports\n ",output_latex)    
if __name__ == "__main__":
    verilog_files_entity = ["can_struct.v","ethernet_core_struct.v","debug_uart_core_struct.v"]
    vhdl_files_entity = ["emp_payload.vhd"]
    # A script made to build a tex file for my thesis
    #extract_ports(file_path = "/home/aq/Downloads/",files = verilog_files_entity[0:1], file_type="verilog")
    extract_ports(file_path="/home/aq/installations/cassette_tester/vcu118_work_area/src/vcu118-repo/an-algo/firmware/hdl/",
                   files=vhdl_files_entity, 
                   file_type="vhdl")   
    
    
    