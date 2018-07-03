#include "pirobo.h"
#include <stdio.h>
#include <string.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <pthread.h>

// all socket code from https://www.binarytides.com/server-client-example-c-sockets-linux/


void *keyboard_server(void *threadid) {

  int socket_desc, client_sock, c, read_size;
  struct sockaddr_in server, client;
  char client_message[2000];
   
  // Create socket
  socket_desc = socket(AF_INET, SOCK_STREAM, 0);
  if(socket_desc == -1) {
    printf("Keyboard init error: could not create socket\n");
  }
  int option = 1;
  setsockopt(socket_desc, SOL_SOCKET, SO_REUSEADDR, &option, sizeof(option));
   
  // Prepare the sockaddr_in structure
  server.sin_family = AF_INET;
  server.sin_addr.s_addr = INADDR_ANY;
  server.sin_port = htons(56000+2);
   
  // Bind
  if(bind(socket_desc,(struct sockaddr *)&server, sizeof(server)) < 0) {
    printf("Keyboard init error: could not bind socket\n");
  }
   
  // Listen
  listen(socket_desc, 3);
  c = sizeof(struct sockaddr_in);
  
  while(1) {
  
    // accept connection from an incoming client
    client_sock = accept(socket_desc, (struct sockaddr *)&client, (socklen_t*)&c);
    if (client_sock < 0) {
      printf("Keyboard init error: could not accept connection\n");
      close(client_sock);
    }
     
    // receive a message from client
    while((read_size = recv(client_sock, client_message, 2000, 0)) > 0) {
      // update flags
      key_w_state = (client_message[0] == '1');
      key_a_state = (client_message[1] == '1');
      key_s_state = (client_message[2] == '1');
      key_d_state = (client_message[3] == '1');
      key_i_state = (client_message[4] == '1');
      key_j_state = (client_message[5] == '1');
      key_k_state = (client_message[6] == '1');
      key_l_state = (client_message[7] == '1');
      key_0_state = (client_message[8] == '1');
      key_1_state = (client_message[9] == '1');
      key_2_state = (client_message[10] == '1');
      key_3_state = (client_message[11] == '1');
      key_4_state = (client_message[12] == '1');
      key_5_state = (client_message[13] == '1');
      key_6_state = (client_message[14] == '1');
      key_7_state = (client_message[15] == '1');
      key_8_state = (client_message[16] == '1');
      key_9_state = (client_message[17] == '1');
    }
    
    
    // close connection  
    close(client_sock);

  }
  
  // cleanup   
  close(socket_desc);
  pthread_exit(NULL);
  
}


int driver_msg(char *msg, char *answer) {

  int read_size = 0;
  int sock;
  struct sockaddr_in server;

  sock = socket(AF_INET, SOCK_STREAM, 0);
  if(sock == -1) {
    printf("Message Error: Could not create socket\n");
    return -1;
  }

  server.sin_addr.s_addr = inet_addr("127.0.0.1");
  server.sin_family = AF_INET;
  server.sin_port = htons(56000+10);

  if(connect(sock, (struct sockaddr *)&server, sizeof(server)) < 0) {
    printf("Message Error: Could not connect\n");
    return -1;
  }

  if(send(sock, msg, strlen(msg), 0) < 0) {
    printf("Message Error: Could not send\n");
    return -1;
  }

  if(answer != NULL) {
    read_size = recv(sock, answer, 1024, 0);
  }

  close(sock);
  
  return read_size;

}


void set_motors(float l, float r) {

  char message[1000];

  if(l >= 1) l = 1;
  else if(l <= -1) l = -1;
  if(r >= 1) r = 1;
  else if(r <= -1) r = -1;
  sprintf(message, "motor %f %f", l, r);
  
  driver_msg(message, NULL);

}


void set_servos(float pan, float tilt) {

  char message[1000];

  if(pan >= 1) pan = 1;
  else if(pan <= 0) pan = 0;
  if(tilt >= 1) tilt = 1;
  else if(tilt <= 0) tilt = 0;
  sprintf(message, "servo %f %f", pan, tilt);
  
  driver_msg(message, NULL);

}


void get_linevalues(unsigned int *data) {

  char answer[1024];

  driver_msg("line", answer);
  sscanf(answer, "%d %d %d %d %d", data, data+1, data+2, data+3, data+4); 

}


void init_drivers(void) {

  //
  // Init keyboad
  //
  key_w_state = 0;
  key_a_state = 0;
  key_s_state = 0;
  key_d_state = 0;
  key_i_state = 0;
  key_j_state = 0;
  key_k_state = 0;
  key_l_state = 0;
  key_0_state = 0;
  key_1_state = 0;
  key_2_state = 0;
  key_3_state = 0;
  key_4_state = 0;
  key_5_state = 0;
  key_6_state = 0;
  key_7_state = 0;
  key_8_state = 0;
  key_9_state = 0;

  pthread_t thread;
  pthread_create(&thread, NULL, keyboard_server, NULL);

}
