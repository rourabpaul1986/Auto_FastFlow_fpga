HOSTCXX = g++ -g
HOSTCXXFLAGS = -std=c++14 -I$(XILINX_VIVADO)/include -I$(XILINX_XRT)/include/ -I .. -I ../../fpga -O3
HOSTLDFLAGS = -L$(XILINX_XRT)/lib/  -pthread -lrt -lstdc++

FFINCLUDE = -I ~/fastflow -DTRACE_FASTFLOW

%:	%.cpp
	$(HOSTCXX) $(HOSTCXXFLAGS) $(HOSTLDFLAGS) $(FFINCLUDE) -o $@ $< /usr/lib/x86_64-linux-gnu/libOpenCL.so -I. 



#1 worker with 2 pipelines 
test_w1p2: w1p2
	./w1p2 ../../kernels/vadd_vinc/vadd_vinc.link.xclbin vadd 0 0 8 4

test_w0p1: w0wNp1
	./w0wNp1 ../../kernels/vadd_vinc/vadd_vinc.link.xclbin vadd 0 0 8 4	

test_wNp1: w0wNp1
	./w0wNp1 ../../kernels/vadd_vinc/vadd_vinc.link.xclbin vadd 4 0 8 4
	
test_w1p1pN: w1wNp1pN
	./w1wNp1pN ../../kernels/vadd_vinc/vadd_vinc.link.xclbin  0 8 4	
test_wNp1pN: w1wNp1pN
	./w1wNp1pN ../../kernels/vadd_vinc/vadd_vinc.link.xclbin  0 8 4	

		
	

clean:
	rm -f *.out test_ftask

cleanall:
	$(RM) -rf sd_host *.o *.xo _x .run .Xil *.xclbin *.ltx *.log *.info *compile_summary* vitis_analyzer* *link_summary* *.o main emconfig.json device_trace_0.csv *.xclbin.package_summary opencl_trace.csv xrt.run_summary summary.csv .ipcache waveform_prefs.json

