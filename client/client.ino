#include <Rainbowduino.h>

long pixels[8 * 8]; // all pixels of the current frame
char c; // the current char from Serial
int parti = 0; // a counter for the current set of data for the pixel
char part[7]; // contains all items for pixel data (len+1 for null char)
int loc = 0; // pixel location offset

void setup() {
  Serial.begin(19200); // establish serial connection
  Rb.init(); // initiate display
}

void loop() {
  if (Serial.available() > 0) { // check if data available
    c = Serial.read(); // read into char
    if (c == 'q') { // terminates the frame, triggers draw
      // reset vars
      loc = 0;
      parti = 0;
      beam(pixels); // display frame
    } else {
      part[parti] = c; // save char to current set of data
      if (parti == 5) { // if data set full (6 char for hex)
        parti = -1; // reset location
        //Serial.write(part); // DEBUG
        char *ptr; // display frame
        pixels[loc] = (long)strtol((char*)part, &ptr, HEX); // convert to hex
        loc++; // progress to next pixel
      }
      parti++; // go to next char in hex
    }
  }
}

void beam(long data[]) {
  Rb.blankDisplay();
  int offset = 0;
  for (int x = 0; x < 8; x++) {
    for (int y = 0; y < 8; y++) {
      Rb.setPixelXY(8-x-1, y, data[offset]);
      offset++;
    }
  }
}

