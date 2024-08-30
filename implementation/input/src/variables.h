//variables 
#include <stdint.h>

// Define the GPIO mode for input
#define GPIO_MODE_INPUT 0x00U // 0x00U is the value for input mode in STM32F407



// Define the base address for GPIOA port
#define GPIOA ((uint32_t)0x40020000)



// Define GPIO_PIN_4 for STM32F407 board
#define GPIO_PIN_4 ((uint16_t)0x0010) // GPIO pin 4 is represented by the 5th bit (0x0010) in the GPIO port register



// Define GPIOB base address for STM32F407 board
#define GPIOB ((uint32_t)0x40020400)



// Define GPIO_PIN_2 for STM32F407 board
#define GPIO_PIN_2 ((uint16_t)0x0004) // Pin 2 is represented by the 3rd bit (0x0004) in the GPIO port register



// Define GPIO_PIN_5 for STM32F407 board
#define GPIO_PIN_5 ((uint16_t)0x0020) // GPIO pin 5 is represented by the bit mask 0x0020



// Define the GPIO mode for output push-pull
#define GPIO_MODE_OUTPUT_PP ((uint32_t)0x00000001) // 0x00000001 represents the mode for output push-pull



// Define GPIO_PIN_3 for STM32F407 board
#define GPIO_PIN_3 ((uint16_t)0x0008) // GPIO pin 3 is represented by the 4th bit (0x0008)



// Define GPIO_PIN_6 for STM32F407 board
#define GPIO_PIN_6 ((uint16_t)0x0040) // GPIO pin 6 is represented by the bit mask 0x0040



// Define GPIO_PIN_1 for STM32F407 board
#define GPIO_PIN_1 ((uint16_t)0x0002) // GPIO pin 1 is represented by the bit mask 0x0002

