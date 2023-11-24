import csv
import re
import pandas as pd
from py_lib.csv_lib import *
from py_lib.yfarm import *

def read_last_line(csv_file):
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        lines = list(reader)

        # Check if there are any lines in the file
        if lines:
            # Filter out lines with unexpected number of fields
            valid_lines = [line for line in lines if len(line) == len(lines[-1])]
            return valid_lines[-1] if valid_lines else None
        else:
            return None

def delete_last_line(csv_file):
    # Read the content of the CSV file
    with open(csv_file, 'r') as file:
        lines = file.readlines()

    # Check if there is any line to delete
    if lines:
        # Rewrite the file excluding the last line
        with open(csv_file, 'w') as file:
            file.writelines(lines[:-1])
        print("Last line deleted.")
    else:
        print("CSV file is empty.")

def read_nth_line(csv_file, n):
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        for i, row in enumerate(reader):
            if i == n:
                return row
def find_unique_farms(filename):
    unique_combinations = {}
    
    with open(filename, 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader)  # Skip the header row if present

        for row in csv_reader:
            column1 = 1
            column2 = len(row) - 1
            if len(row) > max(column1, column2):
                combination = (row[column1], row[column2])
                if combination in unique_combinations:
                    unique_combinations[combination] += 1
                else:
                    unique_combinations[combination] = 1

    # Convert the dictionary to a list of tuples
    unique_combinations_list = [(key[0], key[1], value) for key, value in unique_combinations.items()]

    return unique_combinations_list                
#############start y arm ##########################
def y_arm_extract(row, arm_length, y_proc): 
 init_arm=row[0:arm_length]
 src_node=init_arm[1]
 head="fpga, src, krnl, dst"
 file=""
 #print(init_arm)
 with open(y_proc, 'w') as f:
  write = csv.writer(f)
  write.writerow(head)
  for i in range(1,len(row)//arm_length): 
   if(src_node==row[i*arm_length+1]):
    #print(f"i {i}")
    file=init_arm 
    write.writerow(file)
    init_arm=row[i*arm_length:i*arm_length+arm_length]  
   else:
    init_arm=init_arm+row[i*arm_length:i*arm_length+arm_length] 
   trail=init_arm
  write.writerow(trail)   
 
 last_line = read_last_line(y_proc)
 print(last_line)
 first_line = read_nth_line(y_proc, 1)# 0th skipped for row is header
 #print(first_line)
 #print(len(last_line))

 for i in range(1,len(last_line)//arm_length):
  
  if(last_line[arm_length*i+1]==first_line[len(first_line)-1]):
   split=arm_length*i+1
   break
  #print(last_line[arm_length*i+1])
  #print(first_line[len(first_line)-1])
 print(split)
 part1 = last_line[:split-1]
 part2 = last_line[split-1:]
 print(part1)
 print(part2)
 delete_last_line(y_proc)
 with open(y_proc, 'a') as f:
  write = csv.writer(f)
  write.writerow(part1)
  write.writerow(part2) 
#############end y arm ##########################
############################################################################################   
######################### write y farm which has more than one workers########################   
############################################################################################
def write_Yfarms(host_file, filename, combo, arm_length, src, dst, joint_kernel_name, joint_kernel_index):
    
    
    with open(filename, 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader)  # Skip the header row if present
        new_farm=0
        i=0
        for row in csv_reader:        
         if(row[1]==combo[0]) & (row[len(row)-1]==combo[1]):          
          if(new_farm==0):
            code="//*************************************************************************\n\t"
            code+="//***********start Y Farm Nodes ID : "+src+dst+", No. of Worker :"+str(combo[2])+"**********\n\t"
            code+="//****************************************************************************\n\t"
            code+="ff_pipeline p"+re.sub(r'\s+', '', str(src))+re.sub(r'\s+', '', str(dst))+";\n\t"
            code+="ff_farm farm"+str(combo[0])[1:]+str(combo[1])[1:]+";\n\t"
            code+="farm"+str(combo[0])[1:]+str(combo[1])[1:]+".add_collector(NULL);\n\t"
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
           one_pipe_yfarm(host_file, dev_id, combo, kernel_name, kernel_index, new_farm, joint_kernel_name, joint_kernel_index)
          elif(len(row)>arm_length):#mult pipe in the arm of farm 
           i=i+1
           dev_ids=[]
           kernel_names=[]
           kernel_indexes=[]
           for j in range(len(row)//arm_length): #arm_length is the arm lenght of 1 pipe
                  dev_ids.append(row[j*arm_length])
                  parts = row[j*arm_length+2].split("_")
                  kernel_names.append(parts[0][1:])
                  kernel_indexes.append(parts[1])
                
           mult_pipe_yfarm(host_file, dev_ids, combo, kernel_names, kernel_indexes, new_farm, joint_kernel_name, joint_kernel_index)
          ############################### 
         
          if(i==combo[2]):
            code="farm"+str(combo[0])[1:]+str(combo[1])[1:]+".add_workers(w"+str(combo[0])[1:]+str(combo[1])[1:]+");\n\t"
            #code+="farm"+str(combo[0])[1:]+str(combo[1])[1:]+".remove_collector();\n\t"
            code+="farm"+str(combo[0])[1:]+str(combo[1])[1:]+".cleanup_workers();\n\t"
            code+="p"+re.sub(r'\s+', '', str(src))+re.sub(r'\s+', '', str(dst))+".add_stage(&farm"+str(combo[0])[1:]+str(combo[1])[1:]+");\n\t"
            #code+="auto start"+str(combo[0])[1:]+str(combo[1])[1:]+" = get_time();\n\t"
            #code+="farm"+str(combo[0])[1:]+str(combo[1])[1:]+".run_and_wait_end();\n\t"
            #code+="auto end"+str(combo[0])[1:]+str(combo[1])[1:]+" = get_time();\n\t"
            #code+="std::cout << \"  Time : \" + std::to_string(time_diff_ms(start"+str(combo[0])[1:]+str(combo[1])[1:]+", end"+str(combo[0])[1:]+str(combo[1])[1:]+")) + \" ms\";\n\t"
            code+="//****************************************************************************\n\t"
            code+="//********************end of Y Farm Nodes ID : "+src+dst+"********************\n\t"
            code+="//****************************************************************************\n\t"
            with open(host_file, 'a') as output_file:   
             output_file.write(code) 
            
          new_farm=1

############################################################################################
############################################################################################   
######################### write y farm which has one workers##################################   
############################################################################################
def write_no_Yfarms(host_file, filename, combo, arm_length, src, dst):
    i=0
    
    with open(filename, 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader)  # Skip the header row if present
        new_farm=0
        #print("no farm "+str(combo))  
        for row in csv_reader:        
         if(row[1]==combo[0]) & (row[len(row)-1]==combo[1]) & (combo[2]==1):          
          code="//*************************************************************************\n\t"
          code+="//***********start No Y Farm Nodes ID : "+str(combo[0])[1:]+str(combo[1])[1:]+", No. of Worker :"+str(combo[2])+"**********\n\t"
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
           one_pipe_no_yfarm(host_file, dev_id, combo, kernel_name, kernel_index, new_farm, src, dst)
          elif(len(row)>arm_length):#mult pipe in the arm of farm 
           i=i+1
           dev_ids=[]
           kernel_names=[]
           kernel_indexes=[]
           for i in range(len(row)//arm_length): #arm_length is the lenght of 1 pipe
                  dev_ids.append(row[i*arm_length])
                  parts = row[i*arm_length+2].split("_")
                  kernel_names.append(parts[0][1:])
                  kernel_indexes.append(parts[1])
                
           mult_pipe_no_yfarm(host_file, dev_ids, combo, kernel_names, kernel_indexes, new_farm,  src, dst)           
          ###############################pipe trail part######################################### 
          #code+="auto start"+str(combo[0])[1:]+str(combo[1])[1:]+" = get_time();\n\t"
          #code+="p"+str(combo[0])[1:]+str(combo[1])[1:]+".run_and_wait_end();\n\t"
          #code+="auto end"+str(combo[0])[1:]+str(combo[1])[1:]+" = get_time();\n\t"
          #code+="std::cout << \"  Time : \" + std::to_string(time_diff_ms(start"+str(combo[0])[1:]+str(combo[1])[1:]+", end"+str(combo[0])[1:]+str(combo[1])[1:]+")) + \" ms\";\n\t"
          #code+="//*****end of Farm Nodes ID : "+str(combo[0])[1:]+str(combo[1])[1:]+"******\n\t\n\t"
          with open(host_file, 'a') as output_file:   
             output_file.write(code) 
            
          
################################################################################################   
def y_host_write(host_file, y_proc, arm_length): 
 unique_farms = find_unique_farms(y_proc)
 src=read_nth_line(y_proc, 1)
 dst=read_last_line(y_proc)
 joint_kernel=dst[2]
 parts = joint_kernel.split("_")
 joint_kernel_name=parts[0][1:]
 joint_kernel_index=parts[1]
 print(f"src {src[1]}")
 print(f"dst {dst[-1]}")
 print("----------------------------------") 
 print("The number of farms in y arm is : "+str(len(unique_farms))) 
 print("emitter, collector, #worker") 
 for combo in unique_farms:
    print(combo)  
    if (combo[2]>1): # multiple workers
      write_Yfarms(host_file, y_proc, combo, arm_length, src[1], dst[-1], joint_kernel_name, joint_kernel_index)
    else:            # one worker
      write_no_Yfarms(host_file, y_proc, combo, arm_length, src[1], dst[-1])
 print("----------------------------------")  









 

 
  
