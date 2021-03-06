#include "mex.h"
void mexFunction(int nlhs,mxArray *plhs[],int nrhs,const mxArray *prhs[])
{
    int a = mxGetScalar(prhs[0]);
    printf("a = %d\r\n",a);
}