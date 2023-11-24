import csv
import os
###############################################################################################
defualt_dev_id= 0
max_krnl=4
num_devices=2
arm_length=4 # [fpga, src, krnl, dst]
fpga_column=0 # [fpga column in proc flow]
ckt_file = '../../tests/auto_fast_flow/input_file/circuit.csv'
make_file = 'Makefile1'
###############################################################################################
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
def create_connectivity_files(connectivity_list, max_krnl):
    for element in connectivity_list:
        stripped_element = element.strip('"')
        file_name = f'{stripped_element}_connectivity.ini'
        with open(file_name, 'w') as file:
            # Write content to the file, for example:
            file.write('[connectivity]\n')
            file.write(f'nk={stripped_element}:'+str(max_krnl)+'\n')
            file.write('param2 = value2\n')
            # Add more content if needed


unique_ckts = find_unique_entries(ckt_file, 0)
unique_mem_offset = find_unique_entries(ckt_file, 3)
print(unique_ckts)
print(unique_mem_offset)


create_connectivity_files(unique_ckts, max_krnl)


