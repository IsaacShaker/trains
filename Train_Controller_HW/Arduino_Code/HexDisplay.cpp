#include "HexDisplay.h"

// Constructor
HexDisplay::HexDisplay(int value, int pinCLK, int pinDIO) 
  : dispValue(value), display(pinCLK, pinDIO) // Initialize display with pins
{
  display.setBrightness(0x0f);  // Set brightness
  display.showNumberDec(dispValue);  // Display initial value
}

void HexDisplay::DisplayInt(int value)
{
    display.showNumberDec(value);
}

void HexDisplay::DisplayFloat(float value)
{
  // Multiply the float by 100 to shift the decimal places (e.g., 43.12 becomes 4312)
    int displayValue = (int)(value * 100);

    // Now we have a 4-digit integer to display
     display.showNumberDecEx(displayValue, 0b01000000, true, 4, 0);  // Show the combined digits without worrying about the decimal point
}