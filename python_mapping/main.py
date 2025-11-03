
from SerialManager import SerialManager
from CameraManager import CameraManager
from LED_Mapper import LED_Mapper

import cv2



def main():

    # initialize managers
    led_mapper = LED_Mapper()
    camera_manager = CameraManager()

    box_coords = camera_manager.draw_and_set_bounding_box()
    if box_coords is None:
        print("No bounding box set, exiting")
        camera_manager.release()
        return
    
    led_mapper.set_bounding_box(box_coords)
    
    serial_manager = SerialManager(baud_rate=9600)
    is_connected = serial_manager.connect()
    if not is_connected:
        print("Could not connect to serial, continuing without")


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
                led, led_mapper.num_leds, led_state, test_num, led_mapper.max_tests = [int(x) for x in buffer_data.split('-')]
                
                # calculate led position when the data is recieved
                led_mapper.save_led_pos(current_led_pos, led, led_state, test_num)
            except ValueError:
                print(f"Failed to parse serial data: {buffer_data}")


        # render frame
        if frame is not None:
            cv2.imshow('video', frame)
        
        # check if exit key
        if cv2.waitKey(1) == ord('q'):
            break

    
    avg = led_mapper.get_avg_pos_array()
    print(f"Final avg pos: {avg}")

    led_mapper.save_2d_avg_pos_to_cpp_header()

    camera_manager.release()
    if is_connected:
        serial_manager.close()




if __name__ == '__main__':
    main()