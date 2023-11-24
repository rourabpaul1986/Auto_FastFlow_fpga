import csv
import os

from py_lib.code_gen import *
from py_lib.check_rule import *
from py_lib.csv_lib import *
###############################################################################################
defualt_dev_id= 0
max_krnl=4
num_devices=2
arm_length=4 # [fpga, src, krnl, dst]
fpga_column=0 # [fpga column in proc flow]
ckt_file = 'input_file/circuit.csv'
proc_file = 'input_file/proc_flow.csv'
param_path = '../fpga/param.h'
host_file = 'host.cpp'
###############################################################################################
###########################################rule check##########################################
msg, error, req_fpga = rule_checker(proc_file,  ckt_file, fpga_column, num_devices, arm_length)
###############################################################################################
print("Required FPGA(s) to map given kernels are : "+str(req_fpga))
port_l=fetch_port(ckt_file)
write_param_file(param_path, ckt_file , defualt_dev_id, max_krnl,num_devices, port_l)

with open('./py_lib/header', 'r') as file1:
    header = file1.read()
with open('./py_lib/pre_main', 'r') as file1:
    pre_main = file1.read()        
with open('./py_lib/trail_main', 'r') as file1:
    trail_main = file1.read()        

with open(host_file, 'w') as output_file:
    
    output_file.write(header)    
    output_file.write(pre_main)  
    

get_device(host_file, req_fpga )
    
    
  
unique_farms = find_unique_farms(proc_file)

print("----------------------------------") 
print("The number of farms is : "+str(len(unique_farms))) 
print("emitter, collector, #worker") 
###############################################################################################
#################################dynamic code writing portion##################################
###############################################################################################
for combo in unique_farms:
    print(combo)  
    if (combo[2]>1): # multiple workers
      write_farms(host_file, proc_file, combo, arm_length)
    else:            # one worker
      write_no_farms(host_file, proc_file, combo, arm_length)
print("----------------------------------")  
###############################################################################################
#############################end of dynamic code writing portion###############################
###############################################################################################
with open(host_file, 'a') as output_file:
    # Write the content of the first file to the output file    
    output_file.write(trail_main)   

output_file.close()
################# Turn on to run on FPGA#######################
os.system("make test_host")
###############################################################
