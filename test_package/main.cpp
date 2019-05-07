#include <cstdio>
#include <blosc.h>

int main(int argc, char *argv[])
{
    blosc_init();
    blosc_destroy();
    puts("Test successful\n");
    return 0;
}

