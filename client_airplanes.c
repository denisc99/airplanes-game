#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#define TCP 5000
int main(){
  const char *s="SHOT 3 4\n";
  char buf[64];
  struct sockaddr_in sok={0};
  int fd=socket(AF_INET, SOCK_STREAM, 0);
  sok.sin_family=AF_INET;
  sok.sin_port=htons(TCP);
  inet_pton(AF_INET, "127.0.0.1",&sok.sin_addr);
  if(connect(fd, (struct sockaddr *)&sok, sizeof sok)<0){
    perror("connect");
    return 1;
  
  }
  send(fd, s, strlen(s) ,0);
  ssize_t n=recv(fd, buf, sizeof buf-1,0);
  if(n<1)
    {perror("recv");
    return 1;
    }
  buf[n]='\0';
  printf("%s\n", buf);
  close(fd);
  
  return 0;
}
