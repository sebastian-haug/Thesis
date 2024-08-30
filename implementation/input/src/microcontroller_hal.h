//microcontroller_h.h 
#include <stdint.h> 
#include "variables.h"
// Function to enable the clock for GPIOC
/**
 * @brief  Enables the clock for GPIOA port.
 * @param  None
 * @retval None
 */
void ENABLE_GPIOA_CLOCK(void) {
    // Define the base address for RCC (Reset and Clock Control)
    const uint32_t RCC_BASE = 0x40023800;
    // Define the offset for AHB1ENR (AHB1 peripheral clock enable register)
    const uint32_t RCC_AHB1ENR_OFFSET = 0x30;
    // Define the bit position for GPIOA clock enable in AHB1ENR
    const uint32_t GPIOA_EN_BIT = 0;
    // Calculate the address of RCC_AHB1ENR
    volatile uint32_t *RCC_AHB1ENR = (uint32_t *)(RCC_BASE + RCC_AHB1ENR_OFFSET);
    // Enable the clock for GPIOA by setting the corresponding bit in RCC_AHB1ENR
    *RCC_AHB1ENR |= (1 << GPIOA_EN_BIT);
}
/**
 * @brief  Writes a value to a specified GPIO pin.
 * 
 * This function writes a value (0 or 1) to a specified GPIO pin by directly manipulating the
 * Output Data Register (ODR) of the specified GPIO port. It ensures atomic
 * and reliable operations using bitwise operations.
 * 
 * @param port_base The base address of the GPIO port (e.g., GPIOA, GPIOB).
 * @param pin The pin number to write to (e.g., GPIO_PIN_1, GPIO_PIN_2).
 * @param value The value to write to the pin (0 or 1).
 */
void hardware_abstraction_layer_function_gpio_write_pin(uint32_t port_base, uint16_t pin, int value) {
    // Calculate the bit position of the pin
    uint32_t pin_position = 0;
    for (uint16_t temp_pin = pin; temp_pin > 1; temp_pin >>= 1) {
        pin_position++;
    }
    // Pointer to the Output Data Register (ODR) of the specified port
    volatile uint32_t *odr = (volatile uint32_t *)(port_base + 0x14);
    // Set or clear the pin by using bitwise operations
    if (value) {
        *odr |= (1 << pin_position);  // Set the pin
    } else {
        *odr &= ~(1 << pin_position); // Clear the pin
    }
}
/**
 * @brief  Toggles the state of a specified GPIO pin.
 * 
 * This function toggles the state of a specified GPIO pin by directly accessing the
 * Output Data Register (ODR) of the specified GPIO port. It ensures atomic
 * and reliable operations using bitwise operations.
 * 
 * @param port_base The base address of the GPIO port (e.g., GPIOA, GPIOB).
 * @param pin The pin number to toggle (e.g., GPIO_PIN_1, GPIO_PIN_2).
 */
void hardware_abstraction_layer_function_gpio_toggle_pin(uint32_t port_base, uint16_t pin) {
    // Calculate the bit position of the pin
    uint32_t pin_position = 0;
    for (uint16_t temp_pin = pin; temp_pin > 1; temp_pin >>= 1) {
        pin_position++;
    }
    // Pointer to the Output Data Register (ODR) of the specified port
    volatile uint32_t *odr = (volatile uint32_t *)(port_base + 0x14);
    // Toggle the pin by using bitwise operations
    *odr ^= (1 << pin_position);
}
/**
 * @brief  Reads the state of a specified GPIO pin.
 * 
 * This function reads the state of a specified GPIO pin by directly accessing the
 * Input Data Register (IDR) of the specified GPIO port. It ensures atomic
 * and reliable operations using bitwise operations.
 * 
 * @param port_base The base address of the GPIO port (e.g., GPIOA, GPIOB).
 * @param pin The pin number to read (e.g., GPIO_PIN_1, GPIO_PIN_2).
 * @return int The state of the pin (0 or 1).
 */
int hardware_abstraction_layer_function_gpio_read_pin(uint32_t port_base, uint16_t pin) {
    // Calculate the bit position of the pin
    uint32_t pin_position = 0;
    for (uint16_t temp_pin = pin; temp_pin > 1; temp_pin >>= 1) {
        pin_position++;
    }
    // Pointer to the Input Data Register (IDR) of the specified port
    volatile uint32_t *idr = (volatile uint32_t *)(port_base + 0x10);
    // Read the pin state by using bitwise operations
    return ((*idr & (1 << pin_position)) != 0) ? 1 : 0;
}
/**
 * @brief  Enables the clock for GPIOC port.
 * @param  None
 * @retval None
 */
void ENABLE_GPIOC_CLOCK(void) {
    // Define the base address for RCC (Reset and Clock Control)
    const uint32_t RCC_BASE = 0x40023800;
    // Define the offset for AHB1ENR (AHB1 peripheral clock enable register)
    const uint32_t RCC_AHB1ENR_OFFSET = 0x30;
    // Define the bit position for GPIOC clock enable in AHB1ENR
    const uint32_t GPIOC_EN_BIT = 2;
    // Calculate the address of RCC_AHB1ENR
    volatile uint32_t *RCC_AHB1ENR = (uint32_t *)(RCC_BASE + RCC_AHB1ENR_OFFSET);
    // Enable the clock for GPIOC by setting the corresponding bit in RCC_AHB1ENR
    *RCC_AHB1ENR |= (1 << GPIOC_EN_BIT);
}
/**
 * @brief  Configures the mode of a GPIO pin.
 * @param  port_base: Base address of the GPIO port.
 * @param  pin: GPIO pin number (e.g., GPIO_PIN_1, GPIO_PIN_2).
 * @param  mode: Mode to be set for the GPIO pin (e.g., GPIO_MODE_OUTPUT_PP, GPIO_MODE_INPUT).
 * @retval None
 */
void set_input_output_mode(uint32_t port_base, uint16_t pin, uint32_t mode) {
    // Calculate the pin position
    uint32_t pin_position = 0;
    while ((pin >> pin_position) != 1) {
        pin_position++;
    }
    // Calculate the register address for the mode configuration
    volatile uint32_t *moder = (uint32_t *)(port_base + 0x00); // GPIOx_MODER offset is 0x00
    // Clear the previous mode for the pin
    *moder &= ~(0x3 << (pin_position * 2));
    // Set the new mode for the pin
    *moder |= (mode << (pin_position * 2));
}
/**
 * @brief  Enables the clock for GPIOB port.
 * @param  None
 * @retval None
 */
void ENABLE_GPIOB_CLOCK(void) {
    // Define the base address for RCC (Reset and Clock Control)
    const uint32_t RCC_BASE = 0x40023800;
    // Define the offset for AHB1ENR (AHB1 peripheral clock enable register)
    const uint32_t RCC_AHB1ENR_OFFSET = 0x30;
    // Define the bit position for GPIOB clock enable in AHB1ENR
    const uint32_t GPIOB_EN_BIT = 1;
    // Calculate the address of RCC_AHB1ENR
    volatile uint32_t *RCC_AHB1ENR = (uint32_t *)(RCC_BASE + RCC_AHB1ENR_OFFSET);
    // Enable the clock for GPIOB by setting the corresponding bit in RCC_AHB1ENR
    *RCC_AHB1ENR |= (1 << GPIOB_EN_BIT);
}


/**
 * @brief  Delays execution for a specified number of milliseconds.
 * @param  delay_ms: The number of milliseconds to delay.
 * @return None
 */
void hardware_abstraction_layer_function_delay(uint32_t delay_ms) {
    // Assuming a system clock of 16 MHz and SysTick configured to 1 ms tick
    volatile uint32_t count;
    for (uint32_t i = 0; i < delay_ms; i++) {
        // Each iteration of this loop takes approximately 1 ms
        count = 16000; // Number of cycles for 1 ms delay at 16 MHz
        while (count--) {
            // Busy wait
        }
    }
}

