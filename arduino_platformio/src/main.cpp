#include <Arduino.h>
#include <FastLED.h>

#include "examples.h"
#include "light_mapping.h"
#include "patterns.h"
#include "particle.h"
#include "trail.h"

#define LED_PIN 6
#define NUM_TESTS 3

#define BRIGHTNESS 100
#define LED_TYPE WS2811
#define COLOR_ORDER GRB


CRGB leds[LED_COUNT];


void setup() {

  Serial.begin(9600);

  // ----- LIGHT MAPPING ----- //
  // strip.begin();
  // strip.show(); // sends new data to the leds
  // strip.setBrightness(25); // 1/5 brightness (max is 255)

  // ----- PATTERNS ----- //
  FastLED.addLeds<LED_TYPE, LED_PIN, COLOR_ORDER>(leds, LED_COUNT);
  FastLED.setBrightness(BRIGHTNESS);
  FastLED.clear();
  FastLED.show();

  // run_vertical_line_pattern_setup(0);

  run_particle_setup();

  // run_trail_setup();
  
}

void loop() {

  // ----- LIGHT MAPPING ----- //
  // 3 tests per LED (will take average position)
  // 2 sec wait between tests
  // 5 sec wait before next LED
  // light_mapping(1, 100, 100); // could lower the numbers for time sake

  // light_mapping(3, 250, 250);

  // rainbow(20);
  //theaterChaseRainbow(200);

  // ----- PATTERNS ----- //
  run_vertical_line_pattern();

  // run_circular_pattern();
  // FastLED.show();


  run_particle();

  //  run_trail();

  FastLED.show();
  

}
 






