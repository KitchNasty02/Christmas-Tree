#include <Arduino.h>
#include <Adafruit_NeoPixel.h>
#include <FastLED.h>

#include "examples.h"
#include "light_mapping.h"
#include "patterns.h"

#define LED_PIN 6
#define NUM_TESTS 3

#define BRIGHTNESS 100
#define LED_TYPE WS2811
#define COLOR_ORDER GRB

CRGB leds[LED_COUNT];

Adafruit_NeoPixel strip(LED_COUNT, LED_PIN, NEO_GRB + NEO_KHZ800);

void setup() {

  Serial.begin(9600);

  // ----- LIGHT MAPPING ----- //
  // strip.begin();
  // strip.show(); // sends new data to the leds
  // strip.setBrightness(25); // 1/5 brightness (max is 255)

  // ----- PATTERNS ----- //
  FastLED.addLeds<LED_TYPE, LED_PIN, COLOR_ORDER>(leds, LED_COUNT);
  FastLED.setBrightness(BRIGHTNESS);

  run_vertical_line_pattern_setup(0);
  
}

void loop() {

  // ----- LIGHT MAPPING ----- //
  // 3 tests per LED (will take average position)
  // 2 sec wait between tests
  // 5 sec wait before next LED
  // light_mapping(3, 2000, 5000); // could lower the numbers for time sake

  //light_mapping(NUM_TESTS, 250, 250);

  rainbow(20);
  //theaterChaseRainbow(200);

  // ----- PATTERNS ----- //
  //run_vertical_line_pattern();

  

}
 






