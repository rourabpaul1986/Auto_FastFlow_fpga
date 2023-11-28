# proc_flow1.csv

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

# circuit.csv
The list of available circuits.
The 1st column: name of the cus.
The 2nd column: name of the ports.
The 3rd column: numbe of ports.
The 4th column: strating memory slot (HMB slot number in this case)
