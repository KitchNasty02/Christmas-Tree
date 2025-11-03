
#include "patterns.h"
#include "led_positions.h"
//#include "led_pos_regularized.h"


static const CRGB BLUE = CRGB::Blue;
extern CRGB leds[NUM_LEDS];

// x and z bounds, can change or make based on bounding box
float min_z = 1000.0;
float max_z = -1000.0;
float min_x = 1000.0;
float max_x = -1000.0;

const float SWEEP_TIME = 8000; // time for full sweep from min to max z
const float LINE_THICKNESS = 0.4; // how "thick" the led line is
unsigned long lastUpdateTime = 0; // track timebetween updates

Position patternLedPositions[NUM_LEDS] = {};



void rotate_points_origin(int theta_degrees) {

  const float theta_rad = theta_degrees * (PI / 180.0);

  for (int i = 0; i < NUM_LEDS; i++) {
    float x = ledPositions[i].x;
    float z = ledPositions[i].z;
    
    if (x > -999.0 && z > -999.0) {
      patternLedPositions[i].x = x*cos(theta_rad) - z*sin(theta_rad);
      patternLedPositions[i].z = x*sin(theta_rad) + z*cos(theta_rad);
      
      // update min_x, max_x, min_z, max_z as led positions are translated
      if (patternLedPositions[i].x < min_x) 
        min_x = patternLedPositions[i].x;
      if (patternLedPositions[i].x > max_x) 
        max_x = patternLedPositions[i].x;
      if (patternLedPositions[i].z < min_z) 
        min_z = patternLedPositions[i].z;
      if (patternLedPositions[i].z > max_z) 
        max_z = patternLedPositions[i].z;
      
    }
    else {
      patternLedPositions[i].x = ledPositions[i].x;
      patternLedPositions[i].z = ledPositions[i].z;
    }

  }

  Serial.println("x: " + String(min_x) + ", " + String(max_x));
  Serial.println("z: " + String(min_z) + ", " + String(max_z));

}


void run_vertical_line_pattern_setup(int angle_degrees) {
  lastUpdateTime = millis();

  rotate_points_origin(angle_degrees);
}



void run_vertical_line_pattern() {

  unsigned long currentTime = millis();
  // update every 20ms
  if (currentTime - lastUpdateTime < 20) {
    return;
  }
  lastUpdateTime = currentTime;

  // change pos of sweeping line
  unsigned long timeElapsed = currentTime % (long)SWEEP_TIME;
  float sweepProgress = (float)timeElapsed / (float)SWEEP_TIME;
  float currentSweepZ = min_z + sweepProgress * (max_z - min_z);

  // fades the leds for smoother animation (lower number = faster fade)
  for (int i = 0; i < NUM_LEDS; i++) {
    leds[i].nscale8(230); // Fades by a certain percentage each frame
  }

  // iterate through all leds and check if they are within the lines sweep range
  for (int i = 0; i < NUM_LEDS; i++) {
    // skip bad led positions
    if (patternLedPositions[i].z < -900.0) {
      continue;
    }

    float z = patternLedPositions[i].z;
    float distance = abs(z - (currentSweepZ + LINE_THICKNESS / 2.0));

    // ff the LED is within the line, set its brightness based on distance
    if (distance <= LINE_THICKNESS / 2.0) {
      // map the distance to a brightness value for a fading effect
      float brightness_factor = 1.0 - (distance / (LINE_THICKNESS / 2.0));
      uint8_t brightness = (uint8_t)(brightness_factor * 255);
      leds[i] = ColorFromPalette(RainbowColors_p, map(z, min_z, max_z, 255, 0), brightness);
      // leds[i] = CRGB(0, 0, map(z, MIN_Z, MAX_Z, 0, 255));
      // leds[i].fadeLightBy(255 - brightness);

      //leds[i] = BLUE;
      // leds[i].fadeLightBy(255 - brightness);
    }
  }

  // display new led colors
  FastLED.show();

}








