# include <stdio.h>
# include "string.h"

int countPrice(signed int *strarry);
int main()
{
    signed int * inutarry = {5, -4, 1, -3, 1};
    countPrice(inutarry);
    printf("输出");
    return 0;
    while(1);
}

int countPrice(signed int *strarry)
{
    for(int i=0;i<sizeof(strarry);i++)
    {
        printf("%d\n",strarry[i]);

    }
    return 0;
}