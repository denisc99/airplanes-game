#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#define TCP 5000
#define N 10

static void show_board(const char *title, const char *cells) {
    printf("%s\n   ", title);
    for (int x = 0; x < N; x++) printf("%d ", x);
    printf("\n");
    for (int y = 0; y < N; y++) {
        printf("%d  ", y);
        for (int x = 0; x < N; x++) printf("%c ", cells[y * N + x]);
        printf("\n");                       
    }
}

static int read_line(int fd, char *out, size_t max) {
    size_t n = 0; char c;
    while (n + 1 < max) {
        if (recv(fd, &c, 1, 0) <= 0) return -1;      
        if (c == '\n') break;
        out[n++] = c;
    }
    out[n] = '\0';
    return (int)n;
}


static int ask_ints(const char *prompt, int *v, int count) {
    char line[64];
    for (;;) {
        printf("%s", prompt);
        if (!fgets(line, sizeof line, stdin)) return -1;
        int ok = (count == 2) ? sscanf(line, "%d %d", &v[0], &v[1]) == 2
                              : sscanf(line, "%d %d %d", &v[0], &v[1], &v[2]) == 3;
        if (ok) return 0;
        puts("bad input, try again");
    }
}

int main(int argc, char **argv) {
    const char *ip = argc > 1 ? argv[1] : "127.0.0.1";

    struct sockaddr_in sok = {0};
    int fd = socket(AF_INET, SOCK_STREAM, 0);
    sok.sin_family = AF_INET;
    sok.sin_port = htons(TCP);
    inet_pton(AF_INET, ip, &sok.sin_addr);
    if (connect(fd, (struct sockaddr *)&sok, sizeof sok) < 0) {
        perror("connect");
        return 1;
    }

    char line[128], msg[64];
    int v[3];
    while (read_line(fd, line, sizeof line) >= 0) {
        if (strncmp(line, "PLACE_PLANE", 11) == 0) {
            printf("[server] %s\n", line);
            if (ask_ints("x y orientation (0-up,1-down,2-left,3-right): ", v, 3) < 0) break;
            snprintf(msg, sizeof msg, "PLACE %d %d %d\n", v[0], v[1], v[2]);
            send(fd, msg, strlen(msg), 0);
        } else if (strcmp(line, "YOUR_TURN") == 0) {
            printf("[server] %s\n", line);
            if (ask_ints("x y", v, 2) < 0) break;
            snprintf(msg, sizeof msg, "SHOT %d %d \n", v[0], v[1]);
            send(fd, msg, strlen(msg), 0);
            
        }
        else if (strncmp(line, "BOARD OWN ", 10) == 0 && strlen(line) >= 10 + N * N) {
            show_board("Your board:", line + 10);
      } else if (strncmp(line, "BOARD ENEMY ", 12) == 0 && strlen(line) >= 12 + N * N) {
            show_board("Enemy board:", line + 12);
        }else {
            printf("[server] %s\n", line);
            if (strncmp(line, "GAME_OVER", 9) == 0) break;
        }
    }
    close(fd);
    return 0;
}
