#include <memory>
#include <iostream>
#include <sstream>
#include <string>
#include <ff/ff.hpp>
#include "fnodetask.hpp"
#include "node.cpp"


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
    //////////////////port size calculations/////////////////////////////          
    int input_l_vadd=port_size ("vadd", "in");
    int output_l_vadd=port_size ("vadd", "out");
    int input_l_vinc=port_size ("vinc", "in");
    int output_l_vinc=port_size ("vinc", "out");
    std::cout << "input vadd length : " << input_l_vadd << "\n";
    std::cout << "output vadd length : " << output_l_vadd << "\n";
    std::cout << "input vinc length : " << input_l_vinc << "\n";
    std::cout << "output vinc length : " << output_l_vinc << "\n";
    

     ///////////////////////////////////////////////////////////////////
    std::vector<FDevice> devices; 
    for (int i = 0; i < num_devices; i++) {
           FDevice device(bitstream, i);
           devices.push_back(device);
   }
        // The following code implements a farm with nWorkers workers,
        // each worker is a pipeline with 3 stages like the one above.
        int worker=3;
        ff_farm farm;
        farm.add_emitter(new fake_emitter(worker));
        
        std::vector<ff_node *> w;
        

         ff_pipeline * p = new ff_pipeline();
         //********* n vinc ************************
         /*p->add_stage(new generator(n, m, input_l_vinc, output_l_vinc, mem_offset_vinc, i));
         p->add_stage(new FNodeTask(devices[j], kernel_vincs[i], chain));
         p->add_stage(new drain(input_l_vinc, output_l_vinc, i));*/
         //********* farm 0 pipe 1 vadd ************************
         p->add_stage(new generator(n, m, input_l_vadd, output_l_vadd, mem_offset_vadd, 0));
         p->add_stage(new FNodeTask(devices[0], kernel_vadds[0], chain));
         p->add_stage(new drain(input_l_vadd, output_l_vadd, 0));
         p->cleanup_nodes();
         w.push_back(p);
         //********* farm 0 pipe 1 vadd ************************ 
         p = new ff_pipeline();
         p->add_stage(new generator(n, m, input_l_vadd, output_l_vadd, mem_offset_vadd, 1));
         p->add_stage(new FNodeTask(devices[0], kernel_vadds[1], chain));
         p->add_stage(new drain(input_l_vadd, output_l_vadd, 1));
         p->cleanup_nodes();
         w.push_back(p);
        
        //********* farm 0 pipe 2 :vinc->vinc ************************   
        /*p = new ff_pipeline();   	  
        p->add_stage(new generator(n, m, input_l_vinc, output_l_vinc, mem_offset_vinc,0));
        p->add_stage(new FNodeTask(devices[0], kernel_vincs[0], chain));
        p->add_stage(new middle(n, input_l_vinc, input_l_vinc, output_l_vinc, mem_offset_vinc, 1));
        p->add_stage(new FNodeTask(devices[0], kernel_vincs[1], chain));
        p->add_stage(new drain(input_l_vinc, output_l_vinc));
        p->cleanup_nodes();
        w.push_back(p);*/
        
        //********* farm 0 pipe 2 :vadd->vinc ************************   
        p = new ff_pipeline();   	  
        p->add_stage(new generator(n, m, input_l_vadd, output_l_vadd, mem_offset_vadd,2));
        p->add_stage(new FNodeTask(devices[0], kernel_vadds[2], chain));
        p->add_stage(new middle(n, input_l_vadd, input_l_vinc, output_l_vinc, mem_offset_vinc, 1));
        p->add_stage(new FNodeTask(devices[0], kernel_vincs[1], chain));
        p->add_stage(new drain(input_l_vinc, output_l_vinc));
        p->cleanup_nodes();
        w.push_back(p);

        farm.add_workers(w);
        farm.remove_collector();
        farm.cleanup_workers();


        auto start = get_time();
        farm.run_and_wait_end();
        auto end = get_time();

        std::cout << "  Time : " + std::to_string(time_diff_ms(start, end)) + " ms\n";
        std::cout << "ffTime : " + std::to_string(farm.ffTime()) + " ms\n";
        // farm.ffStats(std::cout);
        
    

    return 0;
}
