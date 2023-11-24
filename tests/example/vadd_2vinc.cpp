#include <memory>
#include <iostream>
#include <sstream>
#include <string>
#include <ff/ff.hpp>
#include "fnodetask.hpp"
#include "param.h"

using namespace ff;
int length = sizeof(ckt) / sizeof(ckt[0]);



int port_size (std::string kernel_name, std::string port_type)
{
 int port_length=-1;
    for (int i = 0; i < length; ++i){
     if (ckt[i].str1==kernel_name && ckt[i].str2==port_type){
       port_length=ckt[i].number;
       break;
       }
     }
   return port_length;  
}
// This function helps the generation of a new task.
// It allocates the memory for the task, fills the input arrays with some data
// and returns the task.
// The FTask object is a wrapper around the task that contains the input and
// output arrays, the scalar values and the information about the memory banks
// used by the task.
// The order of parameters is crucial and must be in the same order as the
// signature of the kernel function.
FTask * new_task(int n, int i_l, int o_l, int mem_offset, int kernel_id)
{
    const int MAX_VAL = 1024;
    //std::cout << "kernel name : " << kernel_name << "\n";

    std::cout << "input length : " << i_l << "\n";
    std::cout << "output length : " << o_l << "\n";
    std::cout << "kernel ID : " << kernel_id << "\n";
    std::cout << "mem_offset : " << mem_offset << "\n";
    std::cout << "------------------ "  << "\n";
    size_t size_in_bytes = n * sizeof(int);
    int ret = 0;
  
    int* in[i_l];  
    int* out[o_l];
    //int * a = nullptr;
    //int * b = nullptr;
    for (int i = 0; i < i_l; ++i) {
        in[i] = nullptr;
    }
    //int * c = nullptr;
    for (int i = 0; i < o_l; ++i) {
        out[i] = nullptr;
    }
    int * s = nullptr;

    //ret |= posix_memalign((void **)&in[0], 4096, size_in_bytes);
    //ret |= posix_memalign((void **)&in[1], 4096, size_in_bytes);
    for (int i = 0; i < i_l; ++i) ret |= posix_memalign((void **)&in[i], 4096, size_in_bytes);
    
    //ret |= posix_memalign((void **)&c, 4096, size_in_bytes);
    for (int i = 0; i < o_l; ++i) ret |= posix_memalign((void **)&out[i], 4096, size_in_bytes);
    s = (int *) malloc(sizeof(int));

    if (ret != 0) {
        std::cerr << "ERROR: failed to allocate aligned memory!\n";
        exit(-1);
    }

    //for (int i = 0; i < n; ++i) in[0][i] = i; // rand() % MAX_VAL;
    //for (int i = 0; i < n; ++i) in[1][i] = i; // rand() % MAX_VAL;
    for (int i = 0; i < i_l; ++i) for (int j = 0; j < n; ++j) in[i][j] = j; // rand() % MAX_VAL;
    *s = n;

    FTask * task = new FTask();
    
    //task->add_input(in[0],  size_in_bytes, bank_in1(kernel_id));
    //task->add_input(in[1],  size_in_bytes, bank_in2(kernel_id));
    for (int i = 0; i < i_l; ++i) 
    task->add_input(in[i],  size_in_bytes, (kernel_id*(i_l+o_l))+i+mem_offset );
     for (int i = 0; i < o_l; ++i) 
    task->add_output(out[i], size_in_bytes, (kernel_id*(i_l+o_l))+i+i_l+mem_offset);
    //task->add_output(out[0], size_in_bytes, bank_out(kernel_id));
    task->add_scalar(s, sizeof(int));

    return task;
}

// This ff_node is used in the farm implementation to start the execution of
// the workes (pipeline containing the FPGA kernels).
struct fake_emitter : public ff_node {
    int n;  // number of generators

    fake_emitter(int n) : n(n) {}

    void * svc(void * t)
    {
        for (int i = 0; i < n; ++i) {
            ff_send_out((int *)(0xBEEF), i);
        }
        return EOS;
    }
};

// This function helps the generation of a new task for the "VINC" kernel.
FTask * new_task_middle(int n, int i_l, int o_l, int mem_offset, int kernel_id, int * cc)
{
    const int MAX_VAL = 1024;
    std::cout << "input length middle: " << i_l << "\n";
    std::cout << "output length middle: " << o_l << "\n";
    std::cout << "kernel ID middle    : " << kernel_id << "\n";
    std::cout << "mem_offset middle   : " << mem_offset << "\n";
    std::cout << "------------------ "  << "\n";
    size_t size_in_bytes = n * sizeof(int);
    int ret = 0;
    //(*cc)++;
    //int * a = cc;
    //int * b = cc;
    int* in[i_l];  
    int* out[o_l];
    for (int i = 0; i < i_l; ++i) {
        in[i] = cc;
    }
    //int * c = nullptr;
    for (int i = 0; i < o_l; ++i) {
        out[i] = nullptr;
    }
    
    int * s = nullptr;

    //ret |= posix_memalign((void **)&c, 4096, size_in_bytes);
    for (int i = 0; i < o_l; ++i) ret |= posix_memalign((void **)&out[i], 4096, size_in_bytes);
    s = (int *) malloc(sizeof(int));

    if (ret != 0) {
        std::cerr << "ERROR: failed to allocate aligned memory!\n";
        exit(-1);
    }
    *s = n;

    FTask * task = new FTask();
    //task->add_input(a,  size_in_bytes, bank_in1(kernel_id));
    //task->add_input(b,  size_in_bytes, bank_in2(kernel_id));
    //task->add_output(c, size_in_bytes, bank_out(kernel_id));
       for (int i = 0; i < i_l; ++i) 
    task->add_input(in[i],  size_in_bytes, (kernel_id*(i_l+o_l))+i+mem_offset );
     for (int i = 0; i < o_l; ++i) 
    task->add_output(out[i], size_in_bytes, (kernel_id*(i_l+o_l))+i+i_l+mem_offset);
    task->add_scalar(s, sizeof(int));

    return task;
}
// This ff_node generates the tasks.
struct generator : public ff_node {

    int n;    // size of the vectors
    int m;    // tasks in the stream
    int i_l;
    int o_l;
    int mem_offset;
    int index;

    generator(int n, int m, int i_l, int o_l, int mem_offset, int index = 0)
    : n(n)
    , m(m)
    , i_l(i_l)
    , o_l(o_l)
    , mem_offset(mem_offset)
    , index(index)
    {}

    void * svc(void * t)
    {
        for(int i = 0; i < m; i++) {
            // std::cout << "generator " + std::to_string(index) + ": generating task " + std::to_string(i) + "\n";
            FTask * task = new_task(n, i_l, o_l, mem_offset, index);
            ff_send_out((void *) task);
            
        }
        return EOS;
    }
};


// This ff_node receivese the result of "VADD" tasks and generate the "VINC" tasks.
class middle : public ff_node {
public:

    int n;
    int i_l;
    int prev_i_l;
    int o_l;
    int mem_offset;
    int index;
    int i;
    std::vector<FTask *> tasks;

    middle(int n,  int prev_i_l, int i_l, int o_l, int mem_offset, int index)
    : n(n)
    , prev_i_l(prev_i_l)
    , i_l(i_l)
    , o_l(o_l)
    , mem_offset(mem_offset)
    , index(index)
    , i(0)
    {}

    void * svc(void * t)
    {
    
        if (t) {
             std::cout << "middle " + std::to_string(index) + ": receiving task " + std::to_string(i) + "\n";
            FTask * task = (FTask *) t;
            
            //int * c = (int *)task->outputs[0].ptr;
            int* out[o_l];
            for(int i=0; i<o_l; i++) 
             out[i] = (int *)(task->outputs[i].ptr);

    
            /*for(int i=0; i<task->outputs[0].size/sizeof(int); i++) 
            std::cout << "Sum i : " << c[i] << " "<< std::endl;
            std::cout << "\n "<< std::endl;*/
            /*for(int i=0; i<o_l; i++) {
             int *currentOutput = out[i];
             for(int j=0; j<task->outputs[0].size/sizeof(int); j++) 
              std::cout << "Sum : " << currentOutput[j] << " "<< std::endl;
              std::cout << "\n "<< std::endl;
            }*/
            
            //free(task->inputs[0].ptr);
            //free(task->inputs[1].ptr);
            //task->outputs[0].ptr = nullptr;
            for(int i=0; i<prev_i_l; i++) 
              free(task->inputs[i].ptr);
              
            for(int i=0; i<o_l; i++) 
             task->outputs[i].ptr = nullptr;
            free(task->scalars[0].ptr);
            tasks.push_back(task);
            //(*c)++;
            for(int i=0; i<o_l; i++) {
            FTask * newTask = new_task_middle(n, i_l, o_l, mem_offset, index, out[i]);
            ff_send_out(newTask);
            }
            i++;
        }
        return(GO_ON);
    }

    void svc_end()
    {
        for (auto * t : tasks) {
            delete t;
        }
    }
};
// This ff_node receives the tasks and frees the memory at the end.
struct drain : public ff_node {
    int i_l;
    int o_l;
    int index;
    int i;

    std::vector<FTask *> tasks;

    drain(int i_l, int o_l, int index = 0)
    : i_l(i_l)
    , o_l(o_l)
    , index(index)
    , i(0)
    {}
    

    void * svc(void * t)
    {
        if (t) {
            FTask * task = (FTask *) t;
            //std::cout << "drain " + std::to_string(index) + ": receiving task " + std::to_string(i++) + "\n";
            //int * a = (int *)(task->inputs[0].ptr);
            //int * b = (int *)(task->inputs[1].ptr);
            //int * c = (int *)(task->outputs[0].ptr);
              
           //int* in[i_l];  
           int* out[o_l];
           
           //for(int i=0; i<i_l; i++) 
           //  in[i] = (int *)(task->inputs[i].ptr);
           
           for(int i=0; i<o_l; i++) 
             out[i] = (int *)(task->outputs[i].ptr);
             
            /*for(int i=0; i<task->inputs[0].size/sizeof(int); i++) 
            std::cout << "Data at a: " << a[i] << " "<< std::endl;
            std::cout << "\n "<< std::endl;*/
            //std::cout << "input vinc length : " << i_l << "\n";
            //std::cout << "output vinc length : " << o_l << "\n";
            
            for(int i=0; i<o_l; i++) {
             int *currentOutput = out[i];
             for(int j=0; j<task->outputs[0].size/sizeof(int); j++) 
              std::cout << "Sum : " << currentOutput[j] << " "<< std::endl;
              std::cout << "\n "<< std::endl;
            }
            //////////confusion///////////////////
            free(task->inputs[0].ptr);
            //free(task->inputs[1].ptr);
            //////////////////////////////////////
            //for(int i=0; i<i_l; i++) 
            //  free(task->inputs[i].ptr);
            
            for(int i=0; i<o_l; i++) 
              free(task->outputs[i].ptr);  
            //free(task->outputs[0].ptr);
            free(task->scalars[0].ptr);
            tasks.push_back(task);
        }
        return(GO_ON);
    }

    void svc_end()
    {
        for (auto * t : tasks) {
            delete t;
        }
    }
};

int main(int argc, char * argv[])
{
    std::string bitstream   = "vadd.xclbin";
    std::string kernel_name = "vadd";
    int nWorkers   = 2;
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
                << " " << kernel_name
                << " " << nWorkers
                << " " << (chain ? "1" : "0")
                << " $((1 << 10))"
                << " $((1 << 6))"
                << "\n"
                << std::endl;
        return 0;
    }

    int argi = 1;
    if (argc > argi) bitstream   = std::string(argv[argi++]);
    if (argc > argi) kernel_name = std::string(argv[argi++]);
    if (argc > argi) nWorkers    = atoi(argv[argi++]);
    if (argc > argi) chain       = atoi(argv[argi++]) > 0;
    if (argc > argi) n           = atoi(argv[argi++]);
    if (argc > argi) m           = atoi(argv[argi++]);

    if (nWorkers < 0) nWorkers = 0;
    if (nWorkers > num_devices*max_krnl) nWorkers = num_devices*max_krnl;

    size_t size_in_bytes = n * sizeof(int);
    size_t size_in_kb = size_in_bytes / 1024;
    std::cout << "Executing " << kernel_name << " with " << bitstream + "\n";
    std::cout << "Generating " << (m * nWorkers) << " tasks in total and using " << nWorkers << " workers!\n";
    std::cout << "Task (" << size_in_kb << " KB, " << size_in_kb << " KB) -> (" << size_in_kb << " KB)" << "\n\n";
    std::cout << "nWokers = " << nWorkers << "\n"
              << "  chain = " << chain    << "\n"
              << "      n = " << n        << "\n"
              << "      m = " << m        << "\n"
              << std::endl;
    //////////////////port size calculations/////////////////////////////          
    int input_l_vadd=port_size ("vadd", "in");
    int output_l_vadd=port_size ("vadd", "out");
    int input_l_vinc=port_size ("vinc", "in");
    int output_l_vinc=port_size ("vinc", "out");
    std::cout << "input vadd length  : " << input_l_vadd << "\n";
    std::cout << "output vadd length : " << output_l_vadd << "\n";
    std::cout << "input vinc length  : " << input_l_vinc << "\n";
    std::cout << "output vinc length : " << output_l_vinc << "\n";
    

	///////////////////////////////////////////////////////////////////
    int req_fpga=((nWorkers-1)/max_krnl)+1;
    std::cout << "Required FPGA(s) : " << req_fpga << "\n";
    if (req_fpga>num_devices)
       req_fpga=num_devices;
    if (nWorkers == 0) {
        FDevice device(bitstream, defualt_dev_id);
        // The following code implements a pipeline with 3 stages:
        // 1. generator: generates m tasks
        // 2. FNodeTask: executes the "VADD" kernel on the FPGA
        // 3. drain: receives the tasks and frees the memory
        ff_pipeline p;
        //p.add_stage(new generator(n, m, input_l_vinc, output_l_vinc, mem_offset_vinc,0));
       // p.add_stage(new FNodeTask(device, kernel_vincs[0], chain));
        //*****************vadd->vinc*******************
        p.add_stage(new generator(n, m, input_l_vadd, output_l_vadd, mem_offset_vadd));
        p.add_stage(new FNodeTask(device, kernel_vadds[0], chain));  
          
        p.add_stage(new middle(n, input_l_vadd, input_l_vinc, output_l_vinc, mem_offset_vinc, 1));
        p.add_stage(new FNodeTask(device, kernel_vincs[1], chain));
        p.add_stage(new drain(input_l_vinc, output_l_vinc));
        //*****************vinc->vinc*******************
       // p.add_stage(new generator(n, m, input_l_vinc, output_l_vinc, mem_offset_vinc));
       // p.add_stage(new FNodeTask(device, kernel_vincs[0], chain));  
          
       // p.add_stage(new middle(n, input_l_vadd, input_l_vinc, output_l_vinc, mem_offset_vinc, 1));
       // p.add_stage(new FNodeTask(device, kernel_vincs[1], chain));
       //p.add_stage(new drain(input_l_vinc, output_l_vinc));
        //p.add_stage(new middle(n, input_l_vinc, input_l_vadd, output_l_vadd, mem_offset_vadd, 1));
       // p.add_stage(new FNodeTask(device, kernel_vadds[1],chain));
        //p.add_stage(new drain(input_l_vinc, output_l_vadd));
        
        p.cleanup_nodes();
        p.run_and_wait_end();
        std::cout << "ffTime: " << std::to_string(p.ffTime()) + " ms\n";
    } else {
          std::vector<FDevice> devices; 

         for (int i = 0; i < req_fpga; i++) {
           FDevice device(bitstream, i);
           devices.push_back(device);
         }
        // The following code implements a farm with nWorkers workers,
        // each worker is a pipeline with 3 stages like the one above.
        ff_farm farm;
        farm.add_emitter(new fake_emitter(nWorkers));
        int worker=nWorkers;
        std::vector<ff_node *> w;
        
        for (int j = 0; j < req_fpga; j++) {
        	worker=worker/max_krnl;
        	if (worker!=0) worker=max_krnl;
       		else worker=nWorkers%max_krnl;
          	 
      		for (int i = 0; i < worker; ++i) {
           	 	 ff_pipeline * p = new ff_pipeline();
           		 p->add_stage(new generator(n, m, input_l_vinc, output_l_vinc, mem_offset_vinc, i));
           		 p->add_stage(new FNodeTask(devices[j], kernel_vincs[i], chain));
           		 p->add_stage(new drain(input_l_vinc, output_l_vinc, i));
           		 p->cleanup_nodes();
           		 w.push_back(p);
        	}
       		worker=nWorkers- max_krnl;
        }
        farm.add_workers(w);
        farm.remove_collector();
        farm.cleanup_workers();


        auto start = get_time();
        farm.run_and_wait_end();
        auto end = get_time();

        std::cout << "  Time: " + std::to_string(time_diff_ms(start, end)) + " ms\n";
        std::cout << "ffTime: " + std::to_string(farm.ffTime()) + " ms\n";
        // farm.ffStats(std::cout);
        
    }

    return 0;
}
