#include <Arduino.h>
#include <FastLED.h>
#include "light_mapping.h"



#define WHITE CRGB::White
#define OFF   CRGB::Black

extern CRGB leds[LED_COUNT];


void light_mapping(int num_tests, int test_wait, int next_LED_wait) {   

    // FastLED is 0-based, your protocol is 1-based
    for (uint16_t led = 0; led < LED_COUNT; led++) {
        
        for (int test = 1; test <= num_tests; test++) {

            leds[led] = WHITE;
            FastLED.show();

            // tell vision mapping script LED is on
            Serial.println(
                String(led + 1) + "-" +
                String(LED_COUNT) + "-1-" +
                String(test) + "-" +
                String(num_tests)
            );

            delay(test_wait);

            leds[led] = OFF;
            FastLED.show();

            // tell vision mapping script LED is off
            Serial.println(
                String(led + 1) + "-" +
                String(LED_COUNT) + "-0-" +
                String(test) + "-" +
                String(num_tests)
            );

            delay(test_wait);         
        }

        delay(next_LED_wait);
    }
}
