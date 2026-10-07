# FlightLLM Test Demo

This demo is for testing FlightLLM implementation on the Xilinx Alveo U280 FPGA.
Our submission can be divided into two parts.

1. Performance profile (see `profile/README.md` for details): It is used to compare the performance of the GPU baseline with the simulation performance of the VHK158 FPGA and calculate the speedup ratio, which can verify Figure 11 in the paper (Throughput Speedup of LLaMA2-7B). The performance results of the VHK158 are based on the software run and no hardware is involved. 

2. FPGA on-board testing (see `fpga_implementation/README.md` for details): It is a hardware on-board test on the U280 FPGA to measure the correctness and performance of the paper design. The performance can verify Figure 1 in the paper (55 token/s).

The RTL implementation of this paper is the Intellectual Property (IP) of Infinigence-AI, thus no open-source verilog code can be provided. Instead, we provide the pre-generated bitstream on the U280 FPGA, the pre-compiled cases and the host file. We can assist the evaluators to generate different test cases in the environment at Infinigence-AI. The generated test cases can then be migrated to the evaluator's local environment with the pre-generated bitstream for further evaluation.
