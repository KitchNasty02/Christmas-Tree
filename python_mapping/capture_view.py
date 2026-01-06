
from SerialManager import SerialManager
from CameraManager import CameraManager

import cv2
import time

def capture(led_mapper):

    # initialize managers
    camera_manager = CameraManager()
    serial_manager = SerialManager(baud_rate=9600)

    box_coords = camera_manager.draw_and_set_bounding_box()
    if box_coords is None:
        print("No bounding box set, exiting")
        camera_manager.release()
        return
    
    led_mapper.set_bounding_box(box_coords)

    led_mapper.init_mapping()

    is_connected = serial_manager.connect()
    if not is_connected:
        print("Could not connect to serial, continuing without")
    else:
        serial_manager.flush()

    # hold new data from the queue until led detection
    serial_buffer = []


    while True:
        # --- process camera frame (find led) --- #
        current_led_pos, frame, led_text = camera_manager.capture_test()

        # --- process serial data --- #
        data = serial_manager.get_data()
        if data:
            print(f" > {data}")

        # add all queue data into buffer
        while data:
            serial_buffer.append(data)
            data = serial_manager.get_data()

        # if led pos detected and theres a buffered serial message (a pos needs to be stored)
        # associates led detection with the serial data
        if current_led_pos and serial_buffer:
            # remove oldest message from buffer
            buffer_data = serial_buffer.pop(0)

            try:
                # split line into individual parts
                led, num_leds, led_state, test_num, max_tests = [int(x) for x in buffer_data.split('-')]

                if led_mapper.num_leds == 0:
                    led_mapper.num_leds = num_leds
                    led_mapper.max_tests = max_tests

                
                # calculate led position when the data is recieved
                led_mapper.save_led_pos(current_led_pos, led, led_state, test_num)

                if (led == num_leds and test_num == max_tests):
                    print("Mapped all leds, moving on to next view...")
                    break

            except ValueError:
                print(f"Failed to parse serial data: {buffer_data}")


        # render frame
        if frame is not None:
            cv2.imshow('video', frame)
        
        # check if exit key
        if cv2.waitKey(1) == ord('q'):
            break

    
    led_mapper.set_avg_pos_array()
    print(f"Avg pos appended for this view")

    camera_manager.release()
    if is_connected:
        serial_manager.close()


