/*******************************************************************************
Description:

    This example uses the load/compute/store coding style which is generally
    the most efficient for implementing kernels using HLS. The load and store
    functions are responsible for moving data in and out of the kernel as
    efficiently as possible. The core functionality is decomposed across one
    of more compute functions. Whenever possible, the compute function should
    pass data through HLS streams and should contain a single set of nested loops.

    HLS stream objects are used to pass data between producer and consumer
    functions. Stream read and write operations have a blocking behavior which
    allows consumers and producers to synchronize with each other automatically.

    The dataflow pragma instructs the compiler to enable task-level pipelining.
    This is required for to load/compute/store functions to execute in a parallel
    and pipelined manner. Here the kernel loads, computes and stores NUM_WORDS 
    integer values per clock cycle and is implemented as below:
                                     _____________
Input Vector from Global Memory --->|             |
                             __     |  load_input |
                            |  |<---|_____________|
                  in_stream |  |     _____________ 
                            |__|--->|             |
                                    | compute_inc |      __
                                    |_____________|---->|  |
                                     ______________     |  | out_stream
                                    |              |<---|__|
                                    | store_result |
                                    |______________|-----> Output result to Global Memory

*******************************************************************************/

#include <stdint.h>
#include <hls_stream.h>

#define DATA_SIZE 4096

// TRIPCOUNT identifier
const int c_size = DATA_SIZE;

static void load_input(uint32_t* in, hls::stream<uint32_t>& inStream, int size) {
mem_rd:
    for (int i = 0; i < size; i++) {
#pragma HLS LOOP_TRIPCOUNT min = c_size max = c_size
        inStream << in[i];
    }
}

static void compute_inc(hls::stream<uint32_t>& in_stream,
                        hls::stream<uint32_t>& out_stream,
                        int size) {
execute:
    for (int i = 0; i < size; i++) {
#pragma HLS LOOP_TRIPCOUNT min = c_size max = c_size
        out_stream << (in_stream.read() + 1);
    }
}

static void store_result(uint32_t* out, hls::stream<uint32_t>& out_stream, int size) {
mem_wr:
    for (int i = 0; i < size; i++) {
#pragma HLS LOOP_TRIPCOUNT min = c_size max = c_size
        out[i] = out_stream.read();
    }
}

extern "C" {

/*
    Vector Increment Kernel

    Arguments:
        in  (input)  --> Input vector
        out  (output) --> Output vector
        size (input)  --> Number of elements in vector
*/

void vinc(uint32_t* in, uint32_t* out, int size) {
#pragma HLS INTERFACE m_axi port = in bundle = gmem0
#pragma HLS INTERFACE m_axi port = out bundle = gmem0

    static hls::stream<uint32_t> in_stream("input_stream");
    static hls::stream<uint32_t> out_stream("output_stream");

#pragma HLS dataflow
    // dataflow pragma instruct compiler to run following three APIs in parallel
    load_input(in, in_stream, size);
    compute_inc(in_stream, out_stream, size);
    store_result(out, out_stream, size);
}
}
