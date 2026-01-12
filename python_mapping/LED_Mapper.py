import numpy as np
import json


class LED_Mapper:

    MISSING_2D = (-999.0, -999.0)
    MISSING_3D = (-999.0, -999.0, -999.0)


    def __init__(self):
        self.mapping_data = None
        self.final_avg_pos = None
        self.all_view_pos = []      # holds a final_avg_pos for each view
        self.num_leds = 0
        self.max_tests = 0

        self.bounding_box = None
        self.box_width = 0
        self.x_center = 0
        self.y_base = 0


    def init_mapping(self):
        self.mapping_data = {i: [] for i in range(self.num_leds)}


    # sets the bounding box for the tree
    def set_bounding_box(self, box_coords):
        x_min, y_min, x_max, y_max = box_coords

        self.bounding_box = box_coords
        self.box_width = x_max - x_min
        self.x_center = x_min + self.box_width/2
        self.y_base = y_max # max is at the bottom since origin is top left

        print(f"Bounding box set: x_center={self.x_center:.2f}, y_base={self.y_base:.2f}, width={self.box_width:.2f}")


    # normalize the coords
    def _normalize_coords(self, led_pos):
        x, y = led_pos

        x_norm = (x - self.x_center) / (self.box_width/2)
        # scale cam y axis to x-axis scale
        z_norm = (self.y_base - y) / (self.box_width / 2)

        return x_norm, z_norm
    

    # goes through avg pos and makes sure the leds are in within a certain distance of each other
    # 3D distance calculation should include x, y, and z
    # NOT IMPLEMENTED YET, STILL TESTING IN VISUALIZE_LED_POS
    def _fix_outliers_2d(self):
        max_distance = 1 # could update this
        
        for led in range(self.num_leds - 1):
            prev_x, prev_z = self.final_avg_pos[led-1]
            current_x, current_z = self.final_avg_pos[led]
            next_x, next_z = self.final_avg_pos[led+1]

            prev_distance = np.sqrt((current_x - prev_x)**2 + (current_z - prev_z)**2)
            next_distance = np.sqrt((next_x - current_x)**2 + (next_z - current_z)**2)

            # If distance > 1 between previous and next, put position between the two
            if (prev_distance > max_distance and next_distance > max_distance):
                mid_x = (prev_x + next_x) / 2
                mid_z = (prev_z + next_z) / 2
                self.final_avg_pos[led] = (mid_x, mid_z)






    # maps pixels to coordinates -1 to 1 range and stores them
    def save_led_pos(self, led_pos, led, led_state, test_num):
        if led < 0 or led > self.num_leds:
            print(f"LED {led} out of range")
            return
        
        if led_pos is None:
            print(f"[WARNING] No position detected for LED {led}, skipping save")
            return
        
        if self.mapping_data is None:
            self.init_mapping()
        
        x_norm, z_norm = self._normalize_coords(led_pos)
        
        if led in self.mapping_data:
            self.mapping_data[led].append((x_norm, z_norm))
        else:
            self.mapping_data[led] = [(x_norm, z_norm)]
    
        print(f"Stored pos ({x_norm}, {z_norm}) for led {led}")


    # calc average position for each led
    def set_avg_pos_array(self):
        avg = {}
        for led in sorted(self.mapping_data.keys()):
            positions = np.array(self.mapping_data[led])

            if positions.size > 0:
                avg[led] = np.mean(positions.astype(float), axis=0)
            else:  
                print(f"No positions found for LED {led}")
                avg[led] = self.MISSING_2D

        self.final_avg_pos = avg
        self.all_view_pos.append(self.final_avg_pos)
    


    # saves avg pos data as cpp header file for arduino
    def save_2d_avg_pos_to_cpp_header(self, filename=r"arduino_platformio\include\led_positions.h"):    #MAKE PATH INTO ARDUINO FILE??
        if self.final_avg_pos is None:
            print("No final positions to save")
            return
        
        with open(filename, 'w') as f:
            f.write("#ifndef LED_POSITIONS_H\n")
            f.write("#define LED_POSITIONS_H\n\n")
            
            # Define a struct for position data
            f.write("struct Position { float x, z; };\n\n")
            
            # Create a C++ array of Position structs
            f.write(f"const int NUM_LEDS = {self.num_leds};\n")
            f.write("const Position ledPositions[NUM_LEDS] = {\n")
            
            for led in range(self.num_leds):
                # Retrieve the position, or use a placeholder if not found
                position = self.final_avg_pos[led]
                x, z = position
                f.write(f"  {{ {x:.6f}f, {z:.6f}f }},\n")
            
            f.write("};\n\n")
            f.write("#endif // LED_POSITIONS_H\n")

        print(f"Saved final positions to {filename}")


    
    def compute_3d_positions(self):
        if len(self.all_view_pos) != 4:
            print("[Error] need 4 views to compute 3D positions")
            return None
        
        front, right, back, left = self.all_view_pos
        positions_3d = {}

        for led in range(self.num_leds):
            xs = []
            ys = []
            zs = []

            # front view (x)
            if led in front:
                x, z = front[led]
                if x != -999.0:
                    xs.append(x)
                    zs.append(z)

            # back view (invert x)
            if led in back:
                x, z = back[led]
                if x != -999.0:
                    xs.append(-x)
                    zs.append(z)

            # right view (y)
            if led in right:
                x, z = right[led]
                if x != -999.0:
                    ys.append(x)
                    zs.append(z)

            # left view (invert y)
            if led in left:
                x, z = left[led]
                if x != -999.0:
                    ys.append(-x)
                    zs.append(z)
                    
            if xs and ys and zs:
                positions_3d[led] = (
                    float(np.mean(xs)),
                    float(np.mean(ys)),
                    float(np.mean(zs))
                )
            else:
                positions_3d[led] = self.MISSING_3D

        return positions_3d



    # saves avg pos data as cpp header file for arduino
    def save_3d_avg_pos_to_cpp_header(self, filename=r"arduino_platformio\include\led_positions_3D.h"):
        
        positions_3d = self.compute_3d_positions()
        
        if positions_3d is None:
            return
        
        with open(filename, 'w') as f:
            f.write("#ifndef LED_POSITIONS_3D_H\n")
            f.write("#define LED_POSITIONS_3D_H\n\n")
            
            f.write("struct Position3D { float x, y, z; };\n\n")
            f.write(f"const int NUM_LEDS = {self.num_leds};\n")
            f.write("const Position3D ledPositions[NUM_LEDS] = {\n")
            
            for led in range(self.num_leds):
                x, y, z = positions_3d[led]
                f.write(f"  {{ {x:.6f}f, {y:.6f}f, {z:.6f}f }},\n")
            
            f.write("};\n\n")
            f.write("#endif // LED_POSITIONS_3D_H\n")

        print(f"Saved final positions to {filename}")




