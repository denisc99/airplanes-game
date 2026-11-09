#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#define TCP 5000
int main(int argc, char** argv){
  const char *ip;
  if(argc>1)
    ip=argv[1];
  else ip="127.0.0.1";
  const char *s;
  
  char buf[64];
  struct sockaddr_in sok={0};
  int fd=socket(AF_INET, SOCK_STREAM, 0);
  sok.sin_family=AF_INET;
  sok.sin_port=htons(TCP);
  inet_pton(AF_INET, ip ,&sok.sin_addr);
  if(connect(fd, (struct sockaddr *)&sok, sizeof sok)<0){
    perror("connect");
    return 1;
  
  }
  while(true){
    int x, y;
    char msg[64];

    printf("Input x and y: ");
    if (scanf("%d %d", &x, &y) != 2) {
        int c;
        while ((c = getchar()) != '\n' && c != EOF) 
            if (c == EOF) 
              break;                            
        fprintf(stderr, "bad input, try again\n");
        continue;      
    }

    snprintf(msg, sizeof msg, "SHOT %d %d\n", x, y);
    send(fd, msg, strlen(msg), 0);
    ssize_t n=recv(fd, buf, sizeof buf-1,0);
    if(n<1)
    { perror("recv");
      return 1;
    }
    buf[n]='\0';
    printf("%s", buf);
  
  }
  
  close(fd);
  
  return 0;
}
