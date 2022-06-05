#include <stdio.h>
#include <stdlib.h>

int main()
{
    setuid(0);
    system("cat /root/flag.txt");
    return 0;
 }