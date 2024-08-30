# 0 "implementation\\input\\src\\main.c"
# 0 "<built-in>"
# 0 "<command-line>"
# 1 "implementation\\input\\src\\main.c"

# 1 "implementation\\input\\src\\microcontroller_hal.h" 1

# 1 "implementation\\input\\fake_libc_include/stdint.h" 1



typedef signed char int8_t;
typedef unsigned char uint8_t;
typedef short int16_t;
typedef unsigned short uint16_t;
typedef int int32_t;
typedef unsigned int uint32_t;
typedef long long int64_t;
typedef unsigned long long uint64_t;
# 3 "implementation\\input\\src\\microcontroller_hal.h" 2
# 1 "implementation\\input\\src\\variables.h" 1
# 4 "implementation\\input\\src\\microcontroller_hal.h" 2






void ENABLE_GPIOA_CLOCK(void) {

    const uint32_t RCC_BASE = 1073887232;

    const uint32_t RCC_AHB1ENR_OFFSET = 48;

    const uint32_t GPIOA_EN_BIT = 0;

    volatile uint32_t *RCC_AHB1ENR = (uint32_t *)(RCC_BASE + RCC_AHB1ENR_OFFSET);

    *RCC_AHB1ENR |= (1 << GPIOA_EN_BIT);
}
# 33 "implementation\\input\\src\\microcontroller_hal.h"
void hardware_abstraction_layer_function_gpio_write_pin(uint32_t port_base, uint16_t pin, int value) {

    uint32_t pin_position = 0;
    for (uint16_t temp_pin = pin; temp_pin > 1; temp_pin >>= 1) {
        pin_position++;
    }

    volatile uint32_t *odr = (volatile uint32_t *)(port_base + 20);

    if (value) {
        *odr |= (1 << pin_position);
    } else {
        *odr &= ~(1 << pin_position);
    }
}
# 58 "implementation\\input\\src\\microcontroller_hal.h"
void hardware_abstraction_layer_function_gpio_toggle_pin(uint32_t port_base, uint16_t pin) {

    uint32_t pin_position = 0;
    for (uint16_t temp_pin = pin; temp_pin > 1; temp_pin >>= 1) {
        pin_position++;
    }

    volatile uint32_t *odr = (volatile uint32_t *)(port_base + 20);

    *odr ^= (1 << pin_position);
}
# 80 "implementation\\input\\src\\microcontroller_hal.h"
int hardware_abstraction_layer_function_gpio_read_pin(uint32_t port_base, uint16_t pin) {

    uint32_t pin_position = 0;
    for (uint16_t temp_pin = pin; temp_pin > 1; temp_pin >>= 1) {
        pin_position++;
    }

    volatile uint32_t *idr = (volatile uint32_t *)(port_base + 16);

    return ((*idr & (1 << pin_position)) != 0) ? 1 : 0;
}





void ENABLE_GPIOC_CLOCK(void) {

    const uint32_t RCC_BASE = 1073887232;

    const uint32_t RCC_AHB1ENR_OFFSET = 48;

    const uint32_t GPIOC_EN_BIT = 2;

    volatile uint32_t *RCC_AHB1ENR = (uint32_t *)(RCC_BASE + RCC_AHB1ENR_OFFSET);

    *RCC_AHB1ENR |= (1 << GPIOC_EN_BIT);
}







void set_input_output_mode(uint32_t port_base, uint16_t pin, uint32_t mode) {

    uint32_t pin_position = 0;
    while ((pin >> pin_position) != 1) {
        pin_position++;
    }

    volatile uint32_t *moder = (uint32_t *)(port_base + 0);

    *moder &= ~(3 << (pin_position * 2));

    *moder |= (mode << (pin_position * 2));
}





void ENABLE_GPIOB_CLOCK(void) {

    const uint32_t RCC_BASE = 1073887232;

    const uint32_t RCC_AHB1ENR_OFFSET = 48;

    const uint32_t GPIOB_EN_BIT = 1;

    volatile uint32_t *RCC_AHB1ENR = (uint32_t *)(RCC_BASE + RCC_AHB1ENR_OFFSET);

    *RCC_AHB1ENR |= (1 << GPIOB_EN_BIT);
}
# 3 "implementation\\input\\src\\main.c" 2
# 39 "implementation\\input\\src\\main.c"
void initialize_gpio_pins(void) {



 set_input_output_mode(((uint32_t)1073873920), ((uint16_t)2), ((uint32_t)1));

 set_input_output_mode(((uint32_t)1073873920), ((uint16_t)4), ((uint32_t)1));

 set_input_output_mode(((uint32_t)1073873920), ((uint16_t)8), ((uint32_t)1));





 set_input_output_mode(((uint32_t)1073872896), ((uint16_t)2), 0U);

 set_input_output_mode(((uint32_t)1073872896), ((uint16_t)4), 0U);

 set_input_output_mode(((uint32_t)1073872896), ((uint16_t)32), 0U);

 set_input_output_mode(((uint32_t)1073872896), ((uint16_t)16), 0U);

 set_input_output_mode(((uint32_t)1073872896), ((uint16_t)64), 0U);

}



int main(void) {



ENABLE_GPIOA_CLOCK();

ENABLE_GPIOB_CLOCK();

ENABLE_GPIOC_CLOCK();





initialize_gpio_pins();



while (1) {



int touch_sensor1_state = hardware_abstraction_layer_function_gpio_read_pin(((uint32_t)1073872896), ((uint16_t)2));

int touch_sensor2_state = hardware_abstraction_layer_function_gpio_read_pin(((uint32_t)1073872896), ((uint16_t)4));

int magnet_sensor1_state = hardware_abstraction_layer_function_gpio_read_pin(((uint32_t)1073872896), ((uint16_t)32));

int magnet_sensor2_state = hardware_abstraction_layer_function_gpio_read_pin(((uint32_t)1073872896), ((uint16_t)16));

int ldr_state = hardware_abstraction_layer_function_gpio_read_pin(((uint32_t)1073872896), ((uint16_t)64));





if (ldr_state == 1) {



hardware_abstraction_layer_function_gpio_write_pin(((uint32_t)1073873920), ((uint16_t)2), 1);

hardware_abstraction_layer_function_gpio_write_pin(((uint32_t)1073873920), ((uint16_t)4), 1);

} else {

hardware_abstraction_layer_function_gpio_write_pin(((uint32_t)1073873920), ((uint16_t)2), touch_sensor1_state);

hardware_abstraction_layer_function_gpio_write_pin(((uint32_t)1073873920), ((uint16_t)4), touch_sensor2_state);

}





if (magnet_sensor1_state == 0 || magnet_sensor2_state == 0) {



hardware_abstraction_layer_function_gpio_toggle_pin(((uint32_t)1073873920), ((uint16_t)8));

} else {

hardware_abstraction_layer_function_gpio_write_pin(((uint32_t)1073873920), ((uint16_t)8), 0);

}





hardware_abstraction_layer_function_delay(50);

}

}
