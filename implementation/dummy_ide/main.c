
#include "microcontroller_hal.h"
// Define GPIO pins for LEDs

#define LED_ROOM1_PIN GPIO_PIN_1

#define LED_ROOM2_PIN GPIO_PIN_2

#define WARN_LED_PIN GPIO_PIN_3



// Define GPIO ports for LEDs

#define LED_PORT_BASE GPIOB



// Define GPIO pins for sensors

#define TOUCH_SENSOR1_PIN GPIO_PIN_1

#define TOUCH_SENSOR2_PIN GPIO_PIN_2

#define MAGNET_SENSOR1_PIN GPIO_PIN_5

#define MAGNET_SENSOR2_PIN GPIO_PIN_4

#define LDR_PIN GPIO_PIN_6



// Define GPIO ports for sensors

#define SENSOR_PORT_BASE GPIOA



void initialize_gpio_pins(void) {

// Initialize LEDs

	set_input_output_mode(LED_PORT_BASE, LED_ROOM1_PIN, GPIO_MODE_OUTPUT_PP);

	set_input_output_mode(LED_PORT_BASE, LED_ROOM2_PIN, GPIO_MODE_OUTPUT_PP);

	set_input_output_mode(LED_PORT_BASE, WARN_LED_PIN, GPIO_MODE_OUTPUT_PP);



// Initialize sensors

	set_input_output_mode(SENSOR_PORT_BASE, TOUCH_SENSOR1_PIN, GPIO_MODE_INPUT);

	set_input_output_mode(SENSOR_PORT_BASE, TOUCH_SENSOR2_PIN, GPIO_MODE_INPUT);

	set_input_output_mode(SENSOR_PORT_BASE, MAGNET_SENSOR1_PIN, GPIO_MODE_INPUT);

	set_input_output_mode(SENSOR_PORT_BASE, MAGNET_SENSOR2_PIN, GPIO_MODE_INPUT);

	set_input_output_mode(SENSOR_PORT_BASE, LDR_PIN, GPIO_MODE_INPUT);

}



int main(void) {

// Initialize hardware abstraction layer

ENABLE_GPIOA_CLOCK();

ENABLE_GPIOB_CLOCK();

ENABLE_GPIOC_CLOCK();



// Initialize GPIO pins

initialize_gpio_pins();



while (1) {

// Read sensor states

int touch_sensor1_state = hardware_abstraction_layer_function_gpio_read_pin(SENSOR_PORT_BASE, TOUCH_SENSOR1_PIN);

int touch_sensor2_state = hardware_abstraction_layer_function_gpio_read_pin(SENSOR_PORT_BASE, TOUCH_SENSOR2_PIN);

int magnet_sensor1_state = hardware_abstraction_layer_function_gpio_read_pin(SENSOR_PORT_BASE, MAGNET_SENSOR1_PIN);

int magnet_sensor2_state = hardware_abstraction_layer_function_gpio_read_pin(SENSOR_PORT_BASE, MAGNET_SENSOR2_PIN);

int ldr_state = hardware_abstraction_layer_function_gpio_read_pin(SENSOR_PORT_BASE, LDR_PIN);



// Control LEDs based on sensor states

if (ldr_state == 1) {

// Turn on both room LEDs if the light sensor is not high

hardware_abstraction_layer_function_gpio_write_pin(LED_PORT_BASE, LED_ROOM1_PIN, 1);

hardware_abstraction_layer_function_gpio_write_pin(LED_PORT_BASE, LED_ROOM2_PIN, 1);

} else {

hardware_abstraction_layer_function_gpio_write_pin(LED_PORT_BASE, LED_ROOM1_PIN, touch_sensor1_state);

hardware_abstraction_layer_function_gpio_write_pin(LED_PORT_BASE, LED_ROOM2_PIN, touch_sensor2_state);

}



// Blink warning LED if any magnetic sensor is not connected

if (magnet_sensor1_state == 0 || magnet_sensor2_state == 0) {

// Blink warning LED

hardware_abstraction_layer_function_gpio_toggle_pin(LED_PORT_BASE, WARN_LED_PIN);

} else {

hardware_abstraction_layer_function_gpio_write_pin(LED_PORT_BASE, WARN_LED_PIN, 0);

}



// Add a small delay to create a blinking effect

hardware_abstraction_layer_function_delay(50); // Adjust the delay as needed

}

}



