# circuit.csv

The list of available circuits.
The 1st column: name of the cus.
The 2nd column: name of the ports.
The 3rd column: numbe of ports.
The 4th column: strating memory slot (HMB slot number in this case)

# proc_flow1.csv
The content inside proc_flow1.csv is
```bash
fpga, src, krnl, dst
0, 0, vadd_1, 1
1, 0, vadd_2, 1
0, 2, vadd_3, 3, 0, 3, vinc_1, 4, 0, 4, vmul_1, 5
```
The process flow example mentioned in /input_file/proc_flow1.csv
has 2 farms:

## FARM 01
1. The first farm has 2 workers which src and dst nodes names are `0` and `1` (mentioned in 2 and 4th column of 2nd and 3rd lines).
2. Both of these 2 workers execute vector addition (vadd) conputation unit (cu). The name of the kernels placed in these cus are vadd_1 and vadd_2.
3. The vadd_1 is implemented in FPGA0 (mentioned in 1st column of line 3) and vadd_2 is implemented in FPGA1 (mentioned in 1st column of line 3).
## FARM25
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
# proc_flow2.csv
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

# proc_flow3.csv
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
