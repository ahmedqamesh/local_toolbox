import os
import openai
import re

print("Current working directory:", os.getcwd())

#They’ll show:
#   What fraction of nets are routed
#   Critical paths
#   Resource usage
#   Failing constraints
#report_route_status
#report_timing
#report_drc
#report_utilization

def analyze_vivado_log(log_path):
    with open(log_path) as f:
        log = f.read()

    if "RTSTAT-13" in log:
        print(log)
        #return "Vivado reports insufficient routing. Try running implementation and reviewing constraints. Also check 'report_route_status'."
    # Extend with more rules or AI calls here
    return "No critical issues detected."

# Usage:
print(analyze_vivado_log("/home/aq/Downloads/vivado.log"))
