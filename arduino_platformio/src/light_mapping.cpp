#include <Arduino.h>
#include <Adafruit_NeoPixel.h>
#include "light_mapping.h"

extern Adafruit_NeoPixel strip;

#define WHITE strip.Color(255, 255, 255)
#define OFF strip.Color(0, 0, 0)

/*
format of data sent: LEDINDEX-LEDSTATE-TESTNUM-MAXTESTS
LEDSTATE: 1 for turning on or 0 for turning off
TESTNUM-MAXTETS: current test out of max tests
Ex. 14-1-1-3 -- LED 14 is turned on for the first test out of 3
*/

void light_mapping(int num_tests, int test_wait, int next_LED_wait) {   

    for(uint32_t led = 1; led < strip.numPixels()+1; led++) {
        
        for (int test = 1; test < num_tests+1; test++) {

            strip.setPixelColor(led, WHITE);         
            strip.show();
            // tell vision mapping script led is on
            Serial.println(String(led) + "-" + String(LED_COUNT) + "-1-" + String(test) + "-" + String(num_tests));     
            delay(test_wait);
            
            strip.clear();
            strip.show();
            // tell vision mapping script led is off
            Serial.println(String(led) + "-" + String(LED_COUNT) + "-0-" + String(test) + "-" + String(num_tests));     
            delay(test_wait);         
        }

        delay(next_LED_wait);
                  
    }

}



