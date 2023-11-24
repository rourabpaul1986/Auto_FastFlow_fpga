import csv
import pandas as pd
from py_lib.csv_lib import *
from py_lib.farm import *
from py_lib.y_arm.y_arm import *
y_proc='py_lib/y_proc_flow.csv'   

############################################################################################   
######################### write farm which has more than one workers########################   
############################################################################################
def write_farms(host_file, filename, combo, arm_length):
    
    
    with open(filename, 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader)  # Skip the header row if present
        new_farm=0
        i=0
        for row in csv_reader:        
         if(row[1]==combo[0]) & (row[len(row)-1]==combo[1]):          
          if(new_farm==0):
            code="//*************************************************************************\n\t"
            code+="//***********start Farm Nodes ID : "+str(combo[0])[1:]+str(combo[1])[1:]+", No. of Worker :"+str(combo[2])+"**********\n\t"
            code+="//****************************************************************************\n\t"
            code+="ff_farm farm"+str(combo[0])[1:]+str(combo[1])[1:]+";\n\t"
            code+="farm"+str(combo[0])[1:]+str(combo[1])[1:]+".add_emitter(new fake_emitter("+str(combo[2])+"));\n\t"
            code+="std::vector<ff_node *> w"+str(combo[0])[1:]+str(combo[1])[1:]+";\n\t"
            code+="ff_pipeline * p"+str(combo[0])[1:]+str(combo[1])[1:]+";\n\t"
            with open(host_file, 'a') as output_file:   
             output_file.write(code) 
          #############cheking    ###########################
          if(len(row)==arm_length):#one pipe in the arm of farm
           i=i+1
           parts = row[2].split("_")
           kernel_name=parts[0][1:]
           kernel_index=parts[1]
           dev_id=row[0]
           one_pipe_farm(host_file, dev_id, combo, kernel_name, kernel_index, new_farm)
          elif(len(row)>arm_length):#mult pipe in the arm of farm 
           farm=pipeORfarm(row, arm_length)
           #print(f"farm: {farm}")
           if(farm==0):
             i=i+1
             dev_ids=[]
             kernel_names=[]
             kernel_indexes=[]
             for j in range(len(row)//arm_length): #arm_length is the arm lenght of 1 pipe
                  dev_ids.append(row[j*arm_length])
                  parts = row[j*arm_length+2].split("_")
                  kernel_names.append(parts[0][1:])
                  kernel_indexes.append(parts[1])
                
             mult_pipe_farm(host_file, dev_ids, combo, kernel_names, kernel_indexes, new_farm)
          ############################### 
         
          if(i==combo[2]):
            code="farm"+str(combo[0])[1:]+str(combo[1])[1:]+".add_workers(w"+str(combo[0])[1:]+str(combo[1])[1:]+");\n\t"
            code+="farm"+str(combo[0])[1:]+str(combo[1])[1:]+".remove_collector();\n\t"
            code+="farm"+str(combo[0])[1:]+str(combo[1])[1:]+".cleanup_workers();\n\t"
            code+="auto start"+str(combo[0])[1:]+str(combo[1])[1:]+" = get_time();\n\t"
            code+="farm"+str(combo[0])[1:]+str(combo[1])[1:]+".run_and_wait_end();\n\t"
            code+="auto end"+str(combo[0])[1:]+str(combo[1])[1:]+" = get_time();\n\t"
            code+="std::cout << \"  Time : \" + std::to_string(time_diff_ms(start"+str(combo[0])[1:]+str(combo[1])[1:]+", end"+str(combo[0])[1:]+str(combo[1])[1:]+")) + \" ms\\n\";\n\t"
            code+="//*****end of Farm Nodes ID : "+str(combo[0])[1:]+str(combo[1])[1:]+"******\n\t\n\t"
            with open(host_file, 'a') as output_file:   
             output_file.write(code) 
            
          new_farm=1

############################################################################################   
######################### write farm which has one workers##################################   
############################################################################################
def write_no_farms(host_file, filename, combo, arm_length):
    i=0
    
    with open(filename, 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader)  # Skip the header row if present
        new_farm=0
        #print("no farm "+str(combo))  
        for row in csv_reader:        
         if(row[1]==combo[0]) & (row[len(row)-1]==combo[1]) & (combo[2]==1):          
          code="//*************************************************************************\n\t"
          code+="//***********start NoFarm Nodes ID : "+str(combo[0])[1:]+str(combo[1])[1:]+", No. of Worker :"+str(combo[2])+"**********\n\t"
          code+="//****************************************************************************\n\t"
          #code+="ff_pipeline  p"+str(combo[0])[1:]+str(combo[1])[1:]+";\n\t"
          #with open(host_file, 'a') as output_file:   
          #  output_file.write(code) 
          #############cheking    ###########################
          if(len(row)==arm_length):#one pipe in the arm of farm           
           i=i+1
           parts = row[2].split("_")
           kernel_name=parts[0][1:]
           kernel_index=parts[1]
           dev_id=row[0]
           one_pipe_no_farm(host_file, dev_id, combo, kernel_name, kernel_index, new_farm)
          elif(len(row)>arm_length):#mult pipe in the arm of farm 
           farm=pipeORfarm(row, arm_length)
           #print(f"farm: {farm}")
           if(farm==0):
             i=i+1
             dev_ids=[]
             kernel_names=[]
             kernel_indexes=[]
             for i in range(len(row)//arm_length): #arm_length is the lenght of 1 pipe
                  dev_ids.append(row[i*arm_length])
                  parts = row[i*arm_length+2].split("_")
                  kernel_names.append(parts[0][1:])
                  kernel_indexes.append(parts[1])
                
             mult_pipe_no_farm(host_file, dev_ids, combo, kernel_names, kernel_indexes, new_farm)
           elif(farm==1):
             y_arm_extract(row, arm_length, y_proc)
             y_host_write(host_file, y_proc, arm_length) 
          ###############################pipe trail part######################################### 
          code+="auto start"+str(combo[0])[1:]+str(combo[1])[1:]+" = get_time();\n\t"
          code+="p"+str(combo[0])[1:]+str(combo[1])[1:]+".run_and_wait_end();\n\t"
          code+="auto end"+str(combo[0])[1:]+str(combo[1])[1:]+" = get_time();\n\t"
          code+="std::cout << \"  Time : \" + std::to_string(time_diff_ms(start"+str(combo[0])[1:]+str(combo[1])[1:]+", end"+str(combo[0])[1:]+str(combo[1])[1:]+")) + \" ms\\n\";\n\t"
          code+="//*****end of Farm Nodes ID : "+str(combo[0])[1:]+str(combo[1])[1:]+"******\n\t\n\t"
          with open(host_file, 'a') as output_file:   
             output_file.write(code) 
            
          
################################################################################################


