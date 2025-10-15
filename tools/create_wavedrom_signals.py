########################################################
"""
    This file is part of the MOPS-Hub project.
    Author: Ahmed Qamesh (University of Wuppertal)
    email: ahmed.qamesh@cern.ch  
    Date: 01.05.2023
"""
########################################################
#pip install wavedrom
#pip install svglib reportlab
import wavedrom
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
from io import StringIO, BytesIO
import json
import os 
import sys
rootdir = os.path.dirname(os.path.abspath(__file__)) 
sys.path.insert(0, rootdir+'/mopshub/test_files')
output_dir = "wavedrom_signals"
def generate_wavedrom(wavedrom_svg_data = None, file_name = "wavedrom_svg_data"):
    # Render the WaveDrom diagram to SVG content
    svg_output = wavedrom.render(json.dumps(json.loads(wavedrom_svg_data)))
    
    # Convert the Drawing object to an SVG string
    svg_output = svg_output.tostring()
    
    # Convert SVG string to bytes and create a BytesIO object
    svg_bytes = BytesIO(svg_output.encode('utf-8'))
    
    # Convert SVG bytes to a ReportLab Drawing object
    drawing_rl = svg2rlg(svg_bytes)
    
    
    # Render the Drawing object to a PDF file
    pdf_filename = rootdir+"/wavedrom_signals/"+file_name+".pdf"
    print(f"Preparing Wave for {file_name}. Saved at {pdf_filename}")
    with open(pdf_filename, "wb") as pdf_file:
        renderPDF.drawToFile(drawing_rl, pdf_file)

ipbus_process = """

{
"signal": [
    {"name": "ipb_clk", "wave": "P........", "period": 2},
 ["Master",
    {"name": "ipb_strope", "wave": "0.1...0..1.0.1.0."},
    {"name": "ipb_addr", "wave": "xx=...xxx=.x.=.x..","data": ["A1","A2","A3"]}, 
    {"name": "ipb_write", "wave": "0.1...0..........."},  
    {"name": "ipb_wdata", "wave": "xx=...x...........", "data": ["D1"]}
],
    {},
    ["Slave",
    {"name": "ipb_ack", "wave": "0...1.0..1.0......"},
    {"name": "ipb_error", "wave": "0............1.0.."},
    {"name": " ipb_rdata", "wave": "x........=.x......", "data": ["D2"]}
  ],
     {"node": "..A...B..E.I.C.D"}
],
  "edge": [
    "A<->B Write",
    "E<->I Read",
    "C<->D Error"
  ]
}

"""


write_elink_process = """

{
"signal": [
    {"name": "ipb_clk", "wave": "P........", "period": 2},
 ["Master",
    {"name": "ipb_strope", "wave": "0.1.........0....."},
    {"name": "ipb_write" , "wave": "0.1.........0....."}, 
    {"name": "ipb_addr"  , "wave": "x.=.=.=.=.=.x.....", "data": ["6","7","8","9","B"]},
    {"name": "ipb_wdata" , "wave": "x.5.5.5.5.x.......", "data": ["D1","D2","D3","D4"]}
],
    {},
    ["eLink Slave",
     {"name": "ipb_ack", "wave": "0.1.........0....."},
     {"name": "ipb_error", "wave": "0................."},
     {"name": " ipb_wdata_buffer [95:64]", "wave": "x.5.........x.....", "data": ["D1"]},
     {"name": " ipb_wdata_buffer [63:32]", "wave": "x...5.......x.....", "data": ["D2"]},
     {"name": " ipb_wdata_buffer [31:0 ]", "wave": "x.....5.....x.....", "data": ["D3"]},
     {"name": " start_write_elink", "wave": "0.........1.0....."},
     {"name": " data_tra_elink [95:0]", "wave": "x...........5.x...", "data": ["D"]},
     {"name": " fifo_elink_flush", "wave": "0.............1.0"}
  ],
     {"node": "..A..............B........."}
],
  "edge": [
  "A<->B Writing process to eLink"
  ]
}

"""


read_elink_process = """

{
"signal": [
    {"name": "ipb_clk", "wave": "P......", "period": 2},
 ["Master",
    {"name": "ipb_strope", "wave": "0.1.........0."},
    {"name": "ipb_addr", "wave": "x.=.=.=.=.=.x.","data": ["3","A","0","1","2"]}, 
    {"name": "ipb_write", "wave": "0............."}
],
    {},
    ["eLink Slave",
    {"name": "ipb_ack", "wave": "0...1.......0."},
    {"name": "ipb_error", "wave": "0............."},
    {"name": "fifo_elink_empty", "wave": "1...0.1......."},
    {"name": "data_rec_elink [95:0]", "wave": "x...3.......x.", "data": ["E"]},
    {"name": "start_read_elink", "wave": "0...1.0......."},
    {"name": " ipb_rdata", "wave": "x.....3.3.3.x.", "data": ["E[95:64]","E[63:32]","E[31:0]"]}
  ],
      {"node": "......E.....I...."} 
],
  "edge": [
    "E<->I Read Process from eLink"
  ]
}

"""


    
write_can_process = """

{
"signal": [
    ["Avalon Interface",
     {"name": "clk_40"      , "wave": "P.............","period": 2},
     {"name": "CANAKari Register", "wave": "==..=..=..=..=..=..=..=..=..=,", "data": ["", "General", "Trans. ID 1", "Trans. Data 1-2", "Trans. Data 3-4", "Trans. Data 5-6", "Trans. Data 7-8", "Trans. Control", "General", "Interrupt"]},
     {"name": "CANAKari address"  , "wave": "==..=..=..=..=..=..=..=..=..=,", "data": ["","E", "C", "A", "9", "8", "7", "D", "E", "12"]},
     {"name": "Register Value", "wave": "==..5..............=..=..=..=,", "data": ["", "9C", "data_tra_downlink", "8008", "9C", "8070"]},
     {"name": "write_n", "wave": "10..........................1"},
     {"name": "cs ", "wave": "01.01.01.01.01.01.01.01.01.0."}
    ],
    {},
    ["CAN State Machine",
     {"name": "data_tra_downlink", "wave": "=...5..5..5..5..5..=.........,", "data": ["", "[75:64]", "[63:56]+[47:40]", "[55:48]+[39:32]", "[7:0]+[15:8]", "[23:16]+[31:24]"]},
     {"name": "start_write_can", "wave": "01.................0........."},
     {"name": "reset_irq_can", "wave": "10....................1.....0"},
     {"node": ".A.................B..C.....D"}
  ]
],
  "edge": [
    "A<->B Write Process  to CANAKari",
    "C<->D Reset CANAKari"
  ]
}

"""

read_can_process = """

{
"signal": [
    ["Avalon Interface",
     {"name": "clk_40"      , "wave": "P..........","period": 2},
     {"name": "CANAKari Register", "wave": "==..=..=..=..=..=..=..=,", "data": ["", "Rec. ID 1", "Rec. Data 1-2", "Rec. Data 3-4", "Rec. Data 5-6", "Rec. Data 7-8", "General", "Interrupt"]},
     {"name": "CANAKari address"  , "wave": "==..=..=..=..=..=..=..=,", "data": ["","5", "3", "2", "1", "0", "E", "12"]},
     {"name": "Register Value", "wave": "=3..............=..=..=,", "data": ["", "data_rec_uplink", "9C", "8070"]},
     {"name": "read_n", "wave": "10....................1"},
     {"name": "cs ", "wave": "01.01.01.01.01.01.01.0."}
    ],
    {},
    ["CAN State Machine",
     {"name": "data_rec_uplink", "wave": "=3..3..3..3..3..=......,", "data": ["", "[75:64]", "[63:56]+[47:40]", "[55:48]+[39:32]", "[7:0]+[15:8]", "[23:16]+[31:24]"]},
     {"name": "start_read_can", "wave": "01..............0......"},
     {"name": "reset_irq_can", "wave": "10..............1.....0"},
     {"node": ".A..............BC....D"}
  ]
  ],
  "edge": [
    "A<->B Read Process from CANAKari",
    "B<->D Reset CANAKari"
  ]
}

"""

generate_wavedrom(wavedrom_svg_data = ipbus_process ,file_name = "ipbus_process")
generate_wavedrom(wavedrom_svg_data = write_elink_process ,file_name = "write_elink_process")
generate_wavedrom(wavedrom_svg_data = read_elink_process ,file_name = "read_elink_process")
generate_wavedrom(wavedrom_svg_data = read_can_process ,file_name = "read_can_process")
generate_wavedrom(wavedrom_svg_data = write_can_process ,file_name = "write_can_process")







