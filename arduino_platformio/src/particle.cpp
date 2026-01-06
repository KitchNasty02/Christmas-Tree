#include "particle.h"
#include "led_positions_3D.h"

#define BOX_SIZE      0.35f  
#define SPEED_X       0.008f
#define SPEED_Y       0.008f
#define SPEED_Z       0.005f
#define UPDATE_MS     20


extern CRGB leds[NUM_LEDS];


float boxX = 0.0f;
float boxY = 0.0f;

float velX = SPEED_X;
float velY = SPEED_Y;
float velZ = SPEED_Z;
float speedFactor = 1.0f;

// gets computed in setup
float minZ =  999.0f;
float maxZ = -999.0f;
float boxZ = 0.0f; // will start halfway up


unsigned long lastUpdateTimeParticle = 0;


void run_particle_setup() {
    // compute z bounds
    for (int i = 0; i < NUM_LEDS; i++) {
        if (ledPositions[i].z > -900.0f) {
            minZ = min(minZ, ledPositions[i].z);
            maxZ = max(maxZ, ledPositions[i].z);
        }
    }

    boxZ = (minZ + maxZ) * 0.5f;
    
}



void run_particle() {

    unsigned long currentTime = millis();
    if (currentTime - lastUpdateTimeParticle < UPDATE_MS) return;
    lastUpdateTimeParticle = currentTime;

    // fade previous frame
    for (int i = 0; i < NUM_LEDS; i++) {
        leds[i].nscale8(220);
    }

    // normalize particle vertical position between minZ and maxZ
    float boxZNorm = (boxZ - minZ) / (maxZ - minZ);
    boxZNorm = constrain(boxZNorm, 0.0f, 1.0f);

    // slows down particle as it goes higher
    float speedFactor = 1.0f - 0.5f * boxZNorm;

    // optional: slightly slow horizontal motion too
    float horizSpeedFactor = 1.0f - 0.3f * boxZNorm;


    // move box
    boxX += velX * horizSpeedFactor;
    boxY += velY * horizSpeedFactor;
    boxZ += velZ * speedFactor;

    // bounce off X walls
    if (boxX - BOX_SIZE < -1.0f || boxX + BOX_SIZE > 1.0f) {
        velX *= -1;
        boxX = constrain(boxX, -1.0f + BOX_SIZE, 1.0f - BOX_SIZE);
    }

    // bounce off Y walls
    if (boxY - BOX_SIZE < -1.0f || boxY + BOX_SIZE > 1.0f) {
        velY *= -1;
        boxY = constrain(boxY, -1.0f + BOX_SIZE, 1.0f - BOX_SIZE);
    }

    // bounce off Z floor / ceiling
    if (boxZ - BOX_SIZE < minZ || boxZ + BOX_SIZE > maxZ) {
        velZ *= -1;
        // boxZ = constrain(boxZ, minZ + BOX_SIZE, maxZ - BOX_SIZE);
        boxZ = constrain(boxZ, minZ, maxZ);
    }

    // light LEDs inside the box
    for (int i = 0; i < NUM_LEDS; i++) {
        Position3D pos = ledPositions[i];
        if (pos.z < -900.0f) continue;

        float dx = pos.x - boxX;
        float dy = pos.y - boxY;
        float dz = pos.z - boxZ;

        float dist = sqrt(dx*dx + dy*dy + dz*dz);

        // Normalize the LED's vertical position between minZ and maxZ
        float zNorm = (pos.z - minZ) / (maxZ - minZ);
        zNorm = constrain(zNorm, 0.0f, 1.0f);

        // make the radius bigger near the top so sparse LEDs get hit
        float radius = BOX_SIZE * (1.0f + zNorm * 1.5f);  // tweak 1.5 to taste

        if (dist <= radius) {

            float brightnessFactor = 1.0f - (dist / radius);
            brightnessFactor = constrain(brightnessFactor, 0.3f, 1.0f);

            uint8_t brightness = brightnessFactor * 255;

            // color can depend on height or time
            // leds[i] = CHSV(
            //     map(boxZ * 100, 0, maxZ * 100, 0, 160),
            //     255,
            //     brightness
            // );

            // slowly change based on time
            // larger divisor = slower transition
            uint8_t hue = (currentTime / 100) % 256;
            leds[i] = CHSV(hue, 255, brightness);

            // all one color
            // leds[i] = CRGB::Blue;
            // leds[i].fadeLightBy(255 - brightness);
        }
    }
}



