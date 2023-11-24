#define defualt_dev_id 0
#define max_krnl 4
#define num_devices 2
struct CKT_Struct {
std::string str1;
std::string str2;
int number;
};
       CKT_Struct ckt[6] = {
{"vadd", "in", 2},
{"vadd", "out", 1},
{"vinc", "in", 1},
{"vinc", "out", 1},
{"vmul", "in", 2},
{"vmul", "out", 1}};
#define mem_offset_vadd 0
#define mem_offset_vinc 12
#define mem_offset_vmul 20
std::vector<std::string> kernel_vadds = {
"vadd:{vadd_1}",
"vadd:{vadd_2}",
"vadd:{vadd_3}",
"vadd:{vadd_4}"};
std::vector<std::string> kernel_vincs = {
"vinc:{vinc_1}",
"vinc:{vinc_2}",
"vinc:{vinc_3}",
"vinc:{vinc_4}"};
std::vector<std::string> kernel_vmuls = {
"vmul:{vmul_1}",
"vmul:{vmul_2}",
"vmul:{vmul_3}",
"vmul:{vmul_4}"};
int input_l_vadd=2;
int output_l_vadd=1;
int input_l_vinc=1;
int output_l_vinc=1;
int input_l_vmul=2;
int output_l_vmul=1;
