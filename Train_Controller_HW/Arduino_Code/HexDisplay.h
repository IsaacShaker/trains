#ifndef HEXDISPLAY_H
#define HEXDISPLAY_H

#include <Arduino.h>
#include <TM1637Display.h>

class HexDisplay
{
  private:
    int dispValue;
    TM1637Display display;

  public:
    HexDisplay(int value, int pinCLK, int pinDIO);
    void DisplayInt(int value);
    void DisplayFloat(float value);
};

#endif
