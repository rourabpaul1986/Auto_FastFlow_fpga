import csv
import pandas as pd

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
    
    
def write_param_file(param_path, ckt_file, defualt_dev_id, max_krnl,num_devices, port_l):
    print("***********************************************")
    unique_ckts = find_unique_entries(ckt_file, 0)        #position of ckt name is 0
    unique_mem_offsets = find_unique_entries(ckt_file, 3) #position of mem_set is 3
    print("***********************************************")
    print("circuits available in xclbin are "+str(unique_ckts))
    print("***********************************************")
    text="#define defualt_dev_id "+str(defualt_dev_id)+"\n"
    text+="#define max_krnl "+str(max_krnl)+"\n"
    text+="#define num_devices "+str(num_devices)+"\n"
    text+="struct CKT_Struct {\nstd::string str1;\nstd::string str2;\nint number;\n};\n       CKT_Struct ckt["+str(len(unique_ckts)*2)+"] = {\n"  
   
   
    ckt=""
   
    file = open(ckt_file, "r")
    line = list(csv.reader(file, delimiter=","))
    #print(line)
    for i in range(0, len(line)):
      ckt+="{"
      for j in range(0, len(line[0])-1):
       if(j==len(line[0])-2) & (i!=len(line)-1):
        ckt=ckt+str(line[i][j])+"},\n"
       elif(j==len(line[0])-2) & (i==len(line)-1):
        ckt=ckt+str(line[i][j])+"}"
       else:
        ckt=ckt+"\""+str(line[i][j])+"\", "
      
    file.close()
    #print(ckt)
    text+=ckt+"};\n"
   
   
    for j in range(0, len(unique_ckts)):
      text+="#define mem_offset_"+unique_ckts[j][1:-1]+" "+unique_mem_offsets[j]+"\n"
     
    for j in range(0, len(unique_ckts)):
     text+="std::vector<std::string> kernel_"+unique_ckts[j][1:-1]+"s = {\n"
     for i in range(1, max_krnl + 1):
      if i< max_krnl :
       text+= "\""+unique_ckts[j][1:-1]+":{"+unique_ckts[j][1:-1]+"_"+str(i)+"}\",\n"
      else:
       text+= "\""+unique_ckts[j][1:-1]+":{"+unique_ckts[j][1:-1]+"_"+str(i)+"}\"};\n"

    try:
        with open(param_path, 'w') as file:
            file.write(text)
            file.write(port_l)
        print(f"Text has been written to {param_path}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
       
       
       
       
def find_unique_entries(csv_file_path, column_index):
    # Initialize an empty list to store unique entries
    unique_entries_list = []
   
    # Initialize an empty set to keep track of seen entries
    unique_entries = set()
   
    # Open the CSV file for reading
    with open(csv_file_path, 'r') as file:
        # Read the CSV line by line
        for line in file:
            # Split each line into columns (assuming they are separated by commas)
            columns = line.strip().split(',')
           
            # Extract the entry from the specified column
            if column_index < len(columns):
                entry = columns[column_index].strip()
               
                # Check if the entry is unique
                if entry not in unique_entries:
                    unique_entries.add(entry)
                    unique_entries_list.append(entry)

    return unique_entries_list
    
    
def fetch_port(csv_file):
 file = open(csv_file, "r")
 line = list(csv.reader(file, delimiter=","))
 port_l=""
 for i in range(0, len(line)):
  port_l+="int "+line[i][1]+"put_l_"+line[i][0]+"="+line[i][2]+";\n"  

 return port_l
 

    
def get_req_fpgas(csv_file, column_name):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file)
    
    # Check if the specified column exists in the DataFrame
    if column_name not in df.columns:
        return f"Column '{column_name}' not found in the CSV file."

    # Get unique entries from the specified column
    unique_entries = df[column_name].unique()

    return unique_entries.tolist()    
    
def get_device(host_file, num_devices):
  code="\tstd::vector<FDevice> devices;\n\t"
  code+="for (int i = 0; i < "+str(num_devices)+"; i++) {\n\t"
  code+="\tFDevice device(bitstream, i);\n\t"
  code+="\tdevices.push_back(device);\n\t}\n\t"
  code+="//*******************start of dynamic portion of the code **********************************"
  with open(host_file, 'a') as output_file:   
             output_file.write(code) 
def pipeORfarm(row, arm_length): 
         farm=0 
         #print(row)
         for i in range(0, len(row)//arm_length-1):
              #print(i)
              #print(row[j*4+5])
              if(row[i*4+3])!=(row[i*4+5]):
               farm=1 # all dst node(s) of arm(s) not connected to src node(s) of next arm(s)
               break               
         return farm    
