
import math
import numpy as np


class LED_Mapper:
    def __init__(self):
        self.num_leds = 0
        self.max_tests = 0

        # angle → led → [(x_norm, y_norm)]
        self.angle_data = {}

        # final
        self.led_positions_3d = {}


    def _normalize_coords(self, led_pos):
        x, y = led_pos

        x_norm = (x - self.x_center) / (self.box_width / 2)
        y_norm = (self.y_base - y) / self.box_width  # vertical height

        return x_norm, y_norm
    

    def start_new_angle(self, angle):
        self.angle_data[angle] = {i: [] for i in range(self.num_leds)}


    def consume_detection(self, angle, serial_data, led_pos):
        led, self.num_leds, state, test, self.max_tests = map(int, serial_data.split('-'))

        if state == 1:
            x, y = self._normalize_coords(led_pos)
            self.angle_data[angle][led - 1].append((x, y))


    def compute_3d_positions(self):
        for led in range(self.num_leds):
            projections = []
            heights = []

            for angle, leds in self.angle_data.items():
                if leds[led]:
                    x, y = np.mean(leds[led], axis=0)
                    projections.append((math.radians(angle), x))
                    heights.append(y)

            if len(projections) < 2:
                continue

            # Solve angle using sin projection
            angles, xs = zip(*projections)
            theta = math.atan2(
                sum(x * math.sin(a) for a, x in projections),
                sum(x * math.cos(a) for a, x in projections)
            )

            radius = np.mean([abs(x) for _, x in projections])
            height = np.mean(heights)

            self.led_positions_3d[led] = (
                radius * math.cos(theta),
                height,
                radius * math.sin(theta)
            )

    def save_3d_to_cpp_header(self, filename="led_positions_3d.h"):
        with open(filename, "w") as f:
            f.write("#ifndef LED_POSITIONS_3D_H\n#define LED_POSITIONS_3D_H\n\n")
            f.write("struct Vec3 { float x, y, z; };\n")
            f.write(f"const int NUM_LEDS = {self.num_leds};\n")
            f.write("const Vec3 ledPositions[NUM_LEDS] = {\n")

            for i in range(self.num_leds):
                x, y, z = self.led_positions_3d.get(i, (0, 0, 0))
                f.write(f"  {{ {x:.4f}f, {y:.4f}f, {z:.4f}f }},\n")

            f.write("};\n#endif\n")



