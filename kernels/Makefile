# Options for TARGET: sw_emu, hw_emu and hw
TARGET ?= sw_emu
DEVICE ?= u50
PLATFORM ?= xilinx_$(DEVICE)_gen3x16_xdma_5_202210_1

PLATFORM_REPO_PATHS ?= /opt/xilinx/platforms
PFM := $(PLATFORM_REPO_PATHS)/$(PLATFORM)/$(PLATFORM).xpfm
VPP_FLAGS += --save-temps 

VPP = v++
VPPINCLUDES := -I. 
VPPFLAGS := --platform $(PFM) -t $(TARGET) -s -g
VPPCONNECT := --config connectivity.ini

# VADD
K_VADD_NAME := vadd
K_VADD_FILE := ../kernels_src/vadd/vadd.cpp
K_VADD_XO := vadd.xo
K_VADD_CONNECT := --config vadd_connectivity.ini

# VINC
K_VINC_NAME := vinc
K_VINC_FILE := ../kernels_src/vinc/vinc.cpp
K_VINC_XO := vinc.xo
K_VINC_CONNECT := --config vinc_connectivity.ini


# VMUL
K_VMUL_NAME := vmul
K_VMUL_FILE := ../kernels_src/vmul/vmul.cpp
K_VMUL_XO := vmul.xo
K_VMUL_CONNECT := --config vmul_connectivity.ini

KERNEL_NAME := proc_flow
KERNEL_LINK_XCLBIN := $(KERNEL_NAME).link.xclbin
KERNEL_XCLBIN := $(KERNEL_NAME).xclbin

$(K_VADD_XO): $(K_VADD_FILE)
	$(VPP) --kernel $(K_VADD_NAME) $(VPPFLAGS) $(K_VADD_CONNECT) $(VPPINCLUDES) -c -o $@ $<

$(K_VINC_XO): $(K_VINC_FILE)
	$(VPP) --kernel $(K_VINC_NAME) $(VPPFLAGS) $(K_VINC_CONNECT) $(VPPINCLUDES) -c -o $@ $<

$(K_VMUL_XO): $(K_VMUL_FILE)
	$(VPP) --kernel $(K_VMUL_NAME) $(VPPFLAGS) $(K_VMUL_CONNECT) $(VPPINCLUDES) -c -o $@ $<	


$(KERNEL_XCLBIN): $(K_VADD_XO) $(K_VINC_XO) $(K_VMUL_XO)
	$(VPP) -l  $(VPPFLAGS) $(K_VADD_CONNECT) $(K_VINC_CONNECT) $(K_VMUL_CONNECT) $(VPP_LINK_FLAGS) -o $(KERNEL_LINK_XCLBIN) $(+)
	$(VPP) -p $(KERNEL_LINK_XCLBIN)  $(VPPFLAGS) $(K_VADD_CONNECT) $(K_VINC_CONNECT) $(K_VMUL_CONNECT) -o $(KERNEL_XCLBIN) 

emconfig:emconfig.json
emconfig.json:
	emconfigutil --platform $(PLATFORM)


all: emconfig $(KERNEL_XCLBIN)
#all: emconfig $(K_VADD_XO) $(K_VINC_XO) $(K_VMUL_XO)
clean:
	$(RM) -rf _x .run .Xil *.ltx *.log *.info *compile_summary* vitis_analyzer* *link_summary* *.o main

cleanall:
	$(RM) -rf sd_host *.o *.xo _x .run .Xil *.xclbin *.ltx *.log *.info *compile_summary* vitis_analyzer* *link_summary* *.o main emconfig.json device_trace_0.csv *.xclbin.package_summary opencl_trace.csv xrt.run_summary summary.csv .ipcache waveform_prefs.json
	
#v++ -l -t hw --platform xilinx_u50_gen3x16_xdma_5_202210_1 --config vadd_connectivity.ini --config vinc_connectivity.ini -o ./vadd_vinc.xclbin vadd.xo vinc.xo
