#include <memory>
#include <iostream>
#include <sstream>
#include <string>
#include <ff/ff.hpp>
#include "fnodetask.hpp"
#include "node.cpp"
/* 
-----vadd--
           |--vinc----vinc
-----vmul--           
           
*/
int main(int argc, char * argv[])
{
    std::string bitstream   = "vadd.xclbin";
    bool chain     = false;
    int n          = 1 << 10;
    int m          = 1 << 6;

    if (argc == 1) {
        std::cout << "This program shows the usage of FNodeTask executing a VectorAdd (vadd) kernel containing multiple Compute Units (CUs)." << std::endl;
        std::cout << "\nUsage:\n"
                << "\t" << argv[0] << " file.xclbin [kernel_name] [num_workers] [chain_tasks] [vec_elems] [vec_nums]\n"
                << "\nExample:\n"
                << "\t" << argv[0]
                << " " << bitstream
                << " " << (chain ? "1" : "0")
                << " $((1 << 10))"
                << " $((1 << 6))"
                << "\n"
                << std::endl;
        return 0;
    }

    int argi = 1;
    if (argc > argi) bitstream   = std::string(argv[argi++]);
    if (argc > argi) chain       = atoi(argv[argi++]) > 0;
    if (argc > argi) n           = atoi(argv[argi++]);
    if (argc > argi) m           = atoi(argv[argi++]);

    

    size_t size_in_bytes = n * sizeof(int);
    size_t size_in_kb = size_in_bytes / 1024;
    std::cout << "Executing  with " << bitstream + "\n";
    //std::cout << "Generating " << (m * nWorkers) << " tasks in total and using " << nWorkers << " workers!\n";
    std::cout << "Task (" << size_in_kb << " KB, " << size_in_kb << " KB) -> (" << size_in_kb << " KB)" << "\n\n";
    std::cout << "  chain = " << chain    << "\n"
              << "      n = " << n        << "\n"
              << "      m = " << m        << "\n"
              << std::endl;
	std::vector<FDevice> devices;
	for (int i = 0; i < 2; i++) {
		FDevice device(bitstream, i);
		devices.push_back(device);
	}
	//*******************start of dynamic portion of the code **********************************//*************************************************************************
	//***********start Farm Nodes ID : 01, No. of Worker :2**********
	//****************************************************************************
	ff_pipeline  pipe;
	ff_farm farm01;
	farm01.add_emitter(new fake_emitter(2));
	
	std::vector<ff_node *> w01;
	
	ff_pipeline * p01;
	farm01.add_collector(NULL); 
	//*****Farm Nodes are : (' 0', ' 1'), no. of pipe: 1, Kernel Name : vadd, Kernel index : 1 FPGA ID 0*****
	p01 = new ff_pipeline();
	p01->add_stage(new generator(n, m, input_l_vadd, output_l_vadd, mem_offset_vadd,0));
	p01->add_stage(new FNodeTask(devices[0], kernel_vadds[0], chain));
	p01->add_stage(new middle(n, input_l_vadd, input_l_vinc, output_l_vinc, mem_offset_vinc,1));
	p01->cleanup_nodes();
	w01.push_back(p01);
	
	//*****Farm Nodes are : (' 0', ' 1'), no. of pipe: 1, Kernel Name : vadd, Kernel index : 2 FPGA ID 1*****
	p01 = new ff_pipeline();
	p01->add_stage(new generator(n, m, input_l_vmul, output_l_vmul, mem_offset_vmul,0));
	p01->add_stage(new FNodeTask(devices[0], kernel_vmuls[0], chain));
	p01->add_stage(new middle(n, input_l_vmul, input_l_vinc, output_l_vinc, mem_offset_vinc,1));
	p01->cleanup_nodes();
	w01.push_back(p01);
	
	
	farm01.add_workers(w01);
	
	//farm01.remove_collector();
	farm01.cleanup_workers();
	pipe.add_stage(&farm01);
	
	//*****end of Farm Nodes ID : 01******
	
	
	pipe.add_stage(new FNodeTask(devices[0], kernel_vincs[1], chain));
        pipe.add_stage(new middle(n, input_l_vinc, input_l_vinc, output_l_vinc, mem_offset_vinc,2));
        pipe.add_stage(new FNodeTask(devices[0], kernel_vincs[2], chain));
	pipe.add_stage(new drain(input_l_vinc, output_l_vinc, 2));
	//pipe.cleanup_nodes();
	//*************************************************************************
	//***********start NoFarm Nodes ID : 25, No. of Worker :1**********
	//****************************************************************************
	auto start01 = get_time();
	pipe.run_and_wait_end();
	auto end01 = get_time();
	std::cout << "  Time : " + std::to_string(time_diff_ms(start01, end01)) + " ms";
	//*****end of Farm Nodes ID : 25******
	
	//pipe.cleanup_nodes();
	        
        //*******************end of dynamic portion of the code **********************************
       

        
    

    return 0;
}
