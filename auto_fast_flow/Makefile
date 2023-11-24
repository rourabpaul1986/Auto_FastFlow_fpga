HOSTCXX = g++ -g
HOSTCXXFLAGS = -std=c++14 -I$(XILINX_VIVADO)/include -I$(XILINX_XRT)/include/ -I .. -I ../fpga -O3
HOSTLDFLAGS = -L$(XILINX_XRT)/lib/  -pthread -lrt -lstdc++

FFINCLUDE = -I ~/fastflow -DTRACE_FASTFLOW

%:	%.cpp
	$(HOSTCXX) $(HOSTCXXFLAGS) $(HOSTLDFLAGS) $(FFINCLUDE) -o $@ $< /usr/lib/x86_64-linux-gnu/libOpenCL.so -I. 




test_host: host
	./host ../kernels/vadd4_vinc4_vmul4.xclbin  0 8 4		
test_4: test4
	./test4 ../kernels/vadd4_vinc4_vmul4.xclbin  0 8 4	

clean:
	rm -f *.out test_ftask

cleanall:
	$(RM) -rf sd_host *.o *.xo _x .run .Xil *.xclbin *.ltx *.log *.info *compile_summary* vitis_analyzer* *link_summary* *.o main emconfig.json device_trace_0.csv *.xclbin.package_summary opencl_trace.csv xrt.run_summary summary.csv .ipcache waveform_prefs.json

