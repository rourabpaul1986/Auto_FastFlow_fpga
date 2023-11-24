import csv
import re
############################################################################################   
######################### write farm which has more than one workers########################   
############################################################################################
def one_pipe_yfarm(host_file, dev_id, farm_name, kernel_name, kernel_index, new_farm, joint_kernel_name, joint_kernel_index):
 code="\n\t//***** Y Farm Nodes are : "+str(farm_name[:-1])+", no. of pipe: 1"+", Kernel Name : "+kernel_name+", Kernel index : "+kernel_index+" FPGA ID "+str(dev_id)+"*****\n\t"

    
    
 code+="p"+str(farm_name[0])[1:]+str(farm_name[1])[1:]+" = new ff_pipeline();\n\t"   
 code+="p"+str(farm_name[0])[1:]+str(farm_name[1])[1:]+"->add_stage(new generator(n, m, input_l_"+kernel_name+", output_l_"+kernel_name+", mem_offset_"+kernel_name+","+str(int(kernel_index)-1)+"));\n\t"
 code+="p"+str(farm_name[0])[1:]+str(farm_name[1])[1:]+"->add_stage(new FNodeTask(devices["+dev_id+"], kernel_"+kernel_name+"s["+str(int(kernel_index)-1)+"], chain));\n\t"
 code+="p"+str(farm_name[0])[1:]+str(farm_name[1])[1:]+"->add_stage(new middle(n, input_l_"+kernel_name+", input_l_"+joint_kernel_name+", output_l_"+joint_kernel_name+", mem_offset_"+joint_kernel_name+", "+str(int(joint_kernel_index)-1)+"));\n\t"
 code+="p"+str(farm_name[0])[1:]+str(farm_name[1])[1:]+"->cleanup_nodes();\n\tw"+str(farm_name[0])[1:]+str(farm_name[1])[1:]+".push_back(p"+str(farm_name[0])[1:]+str(farm_name[1])[1:]+");\n\t"
 with open(host_file, 'a') as output_file:   
            output_file.write(code) 
            
              

    #return unique_entries_list
    
############################################################################################
############################################################################################
############################################################################################     
def mult_pipe_yfarm(host_file, dev_ids, farm_name, kernel_names, kernel_indexes, new_farm, joint_kernel_name, joint_kernel_index):
 code="\n\t//* Y Farm Nodes are : "+str(farm_name[:-1])+", no. of pipe: "+str(len(kernel_names))+", Kernel Names : "+str(kernel_names)+", Kernel indexes : "+str(kernel_indexes)+" FPGA IDs "+str(dev_ids)+"\n\t"

    
 #here    
 code+="p"+str(farm_name[0])[1:]+str(farm_name[1])[1:]+" = new ff_pipeline();\n\t"   

 ####################################################################
 for i in range(len(kernel_names)):
   if(i==0):
       code+="p"+str(farm_name[0])[1:]+str(farm_name[1])[1:]+"->add_stage(new generator(n, m, input_l_"+kernel_names[i]+", output_l_"+kernel_names[i]+", mem_offset_"+kernel_names[i]+","+str(int(kernel_indexes[i])-1)+"));\n\t"
       
   code+="p"+str(farm_name[0])[1:]+str(farm_name[1])[1:]+"->add_stage(new FNodeTask(devices["+dev_ids[i]+"], kernel_"+kernel_names[i]+"s["+str(int(kernel_indexes[i])-1)+"], chain));\n\t"    
   
   if(i==len(kernel_names)-1):   
    code+="p"+str(farm_name[0])[1:]+str(farm_name[1])[1:]+"->add_stage(new middle(n, input_l_"+kernel_names[i]+", input_l_"+joint_kernel_name+", output_l_"+joint_kernel_name+", mem_offset_"+joint_kernel_name+","+str(int(joint_kernel_index)-1)+"));\n\t"
   else:
    code+="p"+str(farm_name[0])[1:]+str(farm_name[1])[1:]+"->add_stage(new middle(n, input_l_"+kernel_names[i]+", input_l_"+kernel_names[i+1]+", output_l_"+kernel_names[i+1]+", mem_offset_"+kernel_names[i+1]+","+str(int(kernel_indexes[i+1])-1)+"));\n\t"
          
    
 #######################################################################   
    
 code+="p"+str(farm_name[0])[1:]+str(farm_name[1])[1:]+"->cleanup_nodes();\n\tw"+str(farm_name[0])[1:]+str(farm_name[1])[1:]+".push_back(p"+str(farm_name[0])[1:]+str(farm_name[1])[1:]+");\n\t"
 with open(host_file, 'a') as output_file:   
            output_file.write(code) 
            
              

    #return unique_entries_list
    
############################################################################################   
######################### write farm which has one workers##################################  
############################################################################################   
def one_pipe_no_yfarm(host_file, dev_id, farm_name, kernel_name, kernel_index, new_farm, src, dst):
 code="\n\t//*****Y Farm Nodes are : "+str(farm_name[:-1])+", no. of pipe: 1"+", Kernel Name : "+kernel_name+", Kernel index : "+kernel_index+"*****\n\t"

    
 code+="p"+re.sub(r'\s+', '', str(src))+re.sub(r'\s+', '', str(dst))+".add_stage(new FNodeTask(devices["+dev_id+"], kernel_"+kernel_name+"s["+str(int(kernel_index)-1)+"], chain));\n\t"
 code+="p"+re.sub(r'\s+', '', str(src))+re.sub(r'\s+', '', str(dst))+".add_stage(new drain(input_l_"+kernel_name+", output_l_"+kernel_name+", "+str(int(kernel_index)-1)+"));\n\t"
 code+="//p"+re.sub(r'\s+', '', str(src))+re.sub(r'\s+', '', str(dst))+".cleanup_nodes();\n\t"
 with open(host_file, 'a') as output_file:   
            output_file.write(code) 
            
              

    #return unique_entries_list
    
############################################################################################
############################################################################################
############################################################################################    
def mult_pipe_no_yfarm(host_file, dev_ids, farm_name, kernel_names, kernel_indexes, new_farm,  src, dst):
 code="\n\t//*Y Farm Nodes are : "+str(farm_name[:-1])+", no. of pipe: "+str(len(kernel_names))+", Kernel Names : "+str(kernel_names)+", Kernel indexes : "+str(kernel_indexes)+" FPGA IDs "+str(dev_ids)+"\n\t"

   
    
 #code+="ff_pipeline  p"+str(farm_name[0])[1:]+str(farm_name[1])[1:]+";\n\t"   

 ####################################################################
 for i in range(len(kernel_names)):
   #if(i==0):
   #    code+="p"+str(farm_name[0])[1:]+str(farm_name[1])[1:]+".add_stage(new generator(n, m, input_l_"+kernel_names[i]+", output_l_"+kernel_names[i]+", mem_offset_"+kernel_names[i]+","+str(int(kernel_indexes[i])-1)+"));\n\t"
       
   code+="p"+re.sub(r'\s+', '', str(src))+re.sub(r'\s+', '', str(dst))+".add_stage(new FNodeTask(devices["+dev_ids[i]+"], kernel_"+kernel_names[i]+"s["+str(int(kernel_indexes[i])-1)+"], chain));\n\t"    
   
   if(i==len(kernel_names)-1):   
      code+="p"+re.sub(r'\s+', '', str(src))+re.sub(r'\s+', '', str(dst))+".add_stage(new drain(input_l_"+kernel_names[i]+", output_l_"+kernel_names[i]+", "+str(int(kernel_indexes[i])-1)+"));\n\t"
   else:
      code+="p"+re.sub(r'\s+', '', str(src))+re.sub(r'\s+', '', str(dst))+".add_stage(new middle(n, input_l_"+kernel_names[i]+", input_l_"+kernel_names[i+1]+", output_l_"+kernel_names[i+1]+", mem_offset_"+kernel_names[i+1]+","+str(int(kernel_indexes[i+1])-1)+"));\n\t"
          
    
 #######################################################################   
    
 code+="//p"+re.sub(r'\s+', '', str(src))+re.sub(r'\s+', '', str(dst))+".cleanup_nodes();\n\t"
 with open(host_file, 'a') as output_file:   
            output_file.write(code) 
            
                
