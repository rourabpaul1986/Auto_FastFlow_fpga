# Auto_FastFlow_fpga
Experimental [`FastFlow`](https://github.com/fastflow/fastflow) node called `FNodeTask` to offload computation of `Vitis HLS` kernels on Alveo FPGAs.
The `FNodeTask` can be used in any place where you need an `ff_node`/`ff_node_t`.
It offloads tasks to pre-compiled kernels on an Alveo FPGA

## Input Files
The `auto_fast_flow` program is capable to execute farms and pipes of different process flows in multiple FPGAs. The Auto_FastFlow_fpga program take 2 input files
```
#1. ./input_file/process_flow.csv
#2. ./input_file/circuit.csv
```
process flows is described in ./input_file/process_flow.csv. 
The available computation units are mentioned in ./input_file/circuit.csv.


-----------
### circuit.csv

The list of available circuits.
The 1st column: name of the cus.
The 2nd column: name of the ports.
The 3rd column: numbe of ports.
The 4th column: strating memory slot (HMB slot number in this case)
### proc_flow.csv
This project has 3 examples of proc_flow.csv :proc_flow1.csv, proc_flow2.csv and proc_flow3.csv 
#### proc_flow1.csv
The content inside proc_flow1.csv is
```bash
fpga, src, krnl, dst
0, 0, vadd_1, 1
1, 0, vadd_2, 1
0, 2, vadd_3, 3, 0, 3, vinc_1, 4, 0, 4, vmul_1, 5
```
The process flow example mentioned in /input_file/proc_flow1.csv
has 2 farms:

###### FARM 01
1. The first farm has 2 workers which src and dst nodes names are `0` and `1` (mentioned in 2 and 4th column of 2nd and 3rd lines).
2. Both of these 2 workers execute vector addition (vadd) conputation unit (cu). The name of the kernels placed in these cus are vadd_1 and vadd_2.
3. The vadd_1 is implemented in FPGA0 (mentioned in 1st column of line 3) and vadd_2 is implemented in FPGA1 (mentioned in 1st column of line 3).
##### FARM25
1. This farm has 1 worker which src and dst nodes names are `2` and `5` (mentioned in 2 and 8th column of 4th lines).
2. This worker executes vector addition (vadd),  vector incerment (vinc) and vector multiplication (vmul) conputation unit (cu) in 3 consective pipeline stages (Though each cu has internal pipeline stages). The name of the kernels placed in these cus are vadd_3 and vinc_1 and vmul1.
3. The vadd_3 and vinc_1 and vmul1 are implemented in in FPGA0 (mentioned in 1st column of line 4).
```bash
   |--vadd_1[FPGA0]--|
   |                 |
  (0)               (1)   
   |                 |
   |--vadd_2[FPGA1]--|
  
   (2)--vadd_3[FPGA0]--(3)--vinc_1[FPGA0]--(4)--vmul_1[FPGA0]--(5)
```
#### proc_flow2.csv
The content inside proc_flow2.csv is
```bash
fpga, src, krnl, dst
0, 0, vadd_1, 1
1, 0, vadd_2, 1
0, 0, vadd_3, 2, 0, 2, vinc_1, 3, 0, 3, vmul_1, 1
```
The process flow example mentioned in /input_file/proc_flow2.csv has 1 farms (FARM01) started form 0th node end ended in 1st node. This FRAM01 has 3 woorkers. The 1st workers has vadd_1, 2nd worker has vadd_2 and 3rd worker has 3 pipes with 3 karnels : vadd_3, vinc_1 and vmul_1.
```bash
   |----------------------vadd_1[FPGA0]------------------------|
   |                                                           |
  (0)---------------------vadd_2[FPGA1]-----------------------(1)   
   |                                                           |
   |--vadd_3[FPGA0]--(2)--vinc_1[FPGA0]--(3)--vmul_1[FPGA0]----|
```

#### proc_flow3.csv
The content inside proc_flow3.csv is
```bash
fpga, src, krnl, dst
1, 0, vadd_1, 1
0, 2, vadd_2, 6, 0, 6, vadd_3, 3, 0, 2, vmul_1, 3, 0, 3, vinc_1, 4, 0, 4, vinc_2, 5, 0, 5, vinc_3, 7
```
The process flow example mentioned in /input_file/proc_flow3.csv has 2 farms : FARM01 and FARM23. The FRAM23 has 2 woorkers. The 1st workers has 2 kernels in two consecutive pipse :vadd_1 and vadd_2. The 2nd worker has 1 kernel vmul_1. This two workers combinely connected with another worker which starting node is 3 and ending node is 7. This worker has 3 pipes with 3 karnels : vinc_1, vinc_2 and vinc_3.
```bash
   (0)-----------vadd_1[FPGA1]--------------(1)
                                                                
   |---vadd_2[FPGA0]---(6)---vadd_3[FPGA0]---|
  (2)                                       (3)---vinc_1[FPGA0]---(4)---vinc_2[FPGA0]---(5)---vinc_3[FPGA0]---(7) 
   |---------------vmul_1[FPGA0]-------------|
```

-----------

## Compile xclbin
This example project consist of two xclbins
1. vadd4_vinc4.xclbin : This hardware file has 4 vector addtion (vadd) and 4 vector increment (vinc). All the input and output port of vadd and vinc are connected with dedicated HBM slots to get maximum data speed. The practical data speed of each HBM slot is ~ 16GBps 
2. vadd4_vinc4_vmul4.xclbin : This hardware file has 4 vectir addtion (vadd),  4 vector increment (vinc) and 4 vector multiplication (vmul). All the input and output port of vadd and vinc are connected with dedicated HBM slots to get maximum data speed.
   
```bash
cd kernels/
make all TARGET=hw # sw_emu or hw_emu
```
The above mentioned command takes 3 connectivity.ini file named as vadd_connectivity.ini,vinc_connectivity.ini and vmul_connectivity.ini files. These ini files are used to mentionmemory connections with multiple computation units.
## Compile host
```bash
cd auto_fast_flow
python3 main.py
# the main.py has 3 responsibility
#1 . takes 2 files as input 1)input_files/proc_flow.csv and 2)input_files/circuit.csv
#2 . generates host.cpp to run in host computer
#3 . compile host.cpp and generate output host
#4 . run host
```
Usage:
        ./[outputfile] [file.xclbin] [chain_tasks] [vec_elems] [vec_nums]
Example:
        ./host ../kernels/vadd4_vinc4_vmul4.link.xclbin  0 8 4
```
```
## Clone 
Please include lfs in clone command 
```bash
git lfs clone  https://github.com/rourabpaul1986/Auto_FastFlow_fpga.git
```
You can also compile and run host programs as follows:


