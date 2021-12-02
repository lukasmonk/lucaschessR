#include "protos.h"

#ifdef WIN32
int is_bmi2()
{
    int info[4];
    __cpuidex(info, 0x00000007, 0);
    return (info[1] & ((int)1 <<  8)) != 0;
}
#else
#include <stdint.h>
int is_bmi2()
{
    __builtin_cpu_init ();
    return __builtin_cpu_supports("bmi2");
}
#endif

