volatile int key_w_state;
volatile int key_a_state;
volatile int key_s_state;
volatile int key_d_state;
volatile int key_i_state;
volatile int key_j_state;
volatile int key_k_state;
volatile int key_l_state;
volatile int key_0_state;
volatile int key_1_state;
volatile int key_2_state;
volatile int key_3_state;
volatile int key_4_state;
volatile int key_5_state;
volatile int key_6_state;
volatile int key_7_state;
volatile int key_8_state;
volatile int key_9_state;

volatile int touch_x_state;
volatile int touch_y_state;

void init_drivers(void);
void set_motors(float l, float r);
void set_servos(float pan, float tilt);
void get_linevalues(unsigned int *data);
