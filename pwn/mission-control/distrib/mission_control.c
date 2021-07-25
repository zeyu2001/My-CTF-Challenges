#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define ADMIN_CODE 200

int secret_code = 0;

void give_shell()
{
	gid_t gid = getegid();
	setresgid(gid, gid, gid);
	system("/bin/sh -i");
}

int main(int argc, char **argv)
{
	printf("===== SPACECON MISSION CONTROL =====\n");
	fflush(stdout);

	char buf[128];
	memset(buf, 0, sizeof(buf));
	fgets(buf, 128, stdin);
	
	char to_print[256];
	memset(to_print, 0, sizeof(to_print));
	
	strcpy(to_print, "You said: ");
	strcat(to_print, buf);
	
	printf(to_print);
	printf("Code: %d\n", secret_code);
	
	if (strncmp(buf, "I am not a robot", 16) == 0)
	{	
		printf("Glad to hear that!\n");
	}
	else
	{
		printf("Stop hacking us!\n");
		return 0;
	}
	
	printf("====================================\n");
	fflush(stdout);
	
	if (secret_code == ADMIN_CODE)
	{
		give_shell();
	}
	else
	{
		printf("Sorry, this area is currently disabled.\n");
	}

	return 0;
}
