
#include <stdio.h>
#include <unistd.h>
#include "inc/pirobo.h"


int main() {

    init_drivers();

    printf("Motor-Check...\n");
    for(float i=0;i<1;i+=0.1) {
        set_motors(i,0);
        usleep(100000);
    }
    for(float i=1;i>-1;i-=0.1) {
        set_motors(i,0);
        usleep(100000);
    }
    for(float i=-1;i<0;i+=0.1) {
        set_motors(i,0);
        usleep(100000);
    }
    for(float i=0;i<1;i+=0.1) {
        set_motors(0,i);
        usleep(100000);
    }
    for(float i=1;i>-1;i-=0.1) {
        set_motors(0,i);
        usleep(100000);
    }
    for(float i=-1;i<0;i+=0.1) {
        set_motors(0,i);
        usleep(100000);
    }
    set_motors(0,0);

    printf("Servo-Check...\n");
    set_servos(0.4,0.5);
    sleep(1);
    set_servos(0.6,0.5);
    sleep(1);
    set_servos(0.5,0.4);
    sleep(1);
    set_servos(0.5,0.6);
    sleep(1);
    set_servos(0.5,0.5);

    unsigned int data[5];
    get_linevalues(data);
    printf("Line-Data: %d, %d\n", data[0], data[4]);


    return 0;

}
