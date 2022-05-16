#include <stdio.h>
#include <stdlib.h>
#include <stddef.h>

size_t strlen(const char* str)
{
	const char* p = str;
	while(*p)
		p++;
	return p - str;
}

int main(void)
{
	char vector[16];
	int length;
	
	length = strlen(vector);
	
	return EXIT_SUCCESS;
}