#include "trail.h"
#include "led_positions_3D.h"


#define NUM_NEIGHBORS 3
#define NUM_TRAILS 2    // how many different trails are going at once
#define TRAIL_LENGTH 4  // how many leds are lit in the trial
#define UPDATE_MS 20
#define TIME_SCALE 1.0f // 1 = normal, 0.5 = half speed -- any speed that is not 1 is causing flickering

extern CRGB leds[NUM_LEDS];

int neighbors[NUM_LEDS][NUM_NEIGHBORS];

struct Trail {
    int currentLED;
    uint8_t hue;
    uint8_t hueSpeed;
    int history[TRAIL_LENGTH]; // keeps track of the last N leds
};

Trail trails[NUM_TRAILS];

bool didMoveThisFrame = false;
unsigned long lastUpdateTimeTrail = 0;


void run_trail_setup() {
    // compute neighbors
    for (int i = 0; i < NUM_LEDS; i++) {

        struct {float dist; int idx;} closest[NUM_NEIGHBORS] = {};

        for (int j = 0; j < NUM_NEIGHBORS; j++) {
            closest[j].dist = 9999.0f;
        }

        for (int j = 0; j < NUM_LEDS; j++) {
            if (i == j) continue;
            float dx = ledPositions[i].x - ledPositions[j].x;
            float dy = ledPositions[i].y - ledPositions[j].y;
            float dz = ledPositions[i].z - ledPositions[j].z;
            float d = sqrt(dx*dx + dy*dy + dz*dz);

            for (int k = 0; k < NUM_NEIGHBORS; k++) {
                if (d < closest[k].dist) {
                    // shift down
                    for (int l = NUM_NEIGHBORS - 1; l > k; l--) {
                        closest[l] = closest[l-1];
                    }
                    closest[k].dist = d;
                    closest[k].idx = j;
                    break;
                }
            }
        }

        for (int k = 0; k < NUM_NEIGHBORS; k++) {
            neighbors[i][k] = closest[k].idx;
        }
    }

    // init trails
    for (int t = 0; t < NUM_TRAILS; t++) {
        trails[t].currentLED = random(NUM_LEDS);    // start at a random led
        trails[t].hue = random8();  // set to a random hue
        trails[t].hueSpeed = (random(1, 4) * 2) - 1; // only odd speeds
        // trails[t].color = CHSV(0, 0, 100); // white
        
        // init history
        for (int i = 0; i < TRAIL_LENGTH; i++) {
            trails[t].history[i] = trails[t].currentLED;  // start with same led
        }
    }
}


void run_trail() {

    unsigned long currentTime = millis();
    if (currentTime - lastUpdateTimeTrail < UPDATE_MS) return;
    lastUpdateTimeTrail = currentTime;

    // fade everything a little to keep older leds dim
    for (int i = 0; i < NUM_LEDS; i++) {
        leds[i].fadeToBlackBy(75);  // bigger makes it fade faster
    }

    didMoveThisFrame = false;

    if (random(100) < (TIME_SCALE * 100)) {

        didMoveThisFrame = true;

        for (int t = 0; t < NUM_TRAILS; t++) {

            if (random(100) < 25) {   // 25% chance to move
                int nextLED = neighbors[trails[t].currentLED][random(NUM_NEIGHBORS)];
                trails[t].currentLED = nextLED;

                // shift history
                for (int i = TRAIL_LENGTH - 1; i > 0; i--) {
                    trails[t].history[i] = trails[t].history[i - 1];
                }
                trails[t].history[0] = nextLED;
            }


            // update led if led moved
            if (didMoveThisFrame) {            
                for (int i = 0; i < TRAIL_LENGTH; i++) {
                    // float factor = 1.0f - i / float(TRAIL_LENGTH);  // head brightest
                    leds[trails[t].history[i]] += CHSV(trails[t].hue, 255, 255);
                    // leds[trails[t].history[i]].fadeLightBy(255 * (1.0f - factor)); // optional extra fade
                }
            }


            // update hues
            // trails[t].hue += trails[t].hueSpeed;
        }
    }

}



