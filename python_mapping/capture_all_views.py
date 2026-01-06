from LED_Mapper import LED_Mapper
from capture_view import capture

led_mapper = LED_Mapper()
led_mapper.mapping_data = None

NUM_VIEWS = 4

for i in range(NUM_VIEWS):
    print(f"Capturing View {i+1}")
    capture(led_mapper)

# convert and save to 3D coordinates after all views are finished
led_mapper.save_3d_avg_pos_to_cpp_header()
print("3D mapping saved.")
