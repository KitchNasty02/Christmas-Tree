from SerialManager import SerialManager
from CameraManager import CameraManager
from LED_Mapper import LED_Mapper

import cv2

ANGLES = [0, 90, 180, 270]


def run_mapping_for_angle(angle, led_mapper):
    print(f"\n=== Mapping angle {angle}° ===")

    camera = CameraManager()
    box_coords = camera.draw_and_set_bounding_box()
    if box_coords is None:
        camera.release()
        return False

    led_mapper.set_bounding_box(box_coords)

    serial_manager = SerialManager(baud_rate=9600)
    if not serial_manager.connect():
        print("Serial connection failed")
        camera.release()
        return False

    serial_buffer = []

    while True:
        led_pos, frame, _ = camera.capture_test()

        data = serial_manager.get_data()
        while data:
            serial_buffer.append(data)
            data = serial_manager.get_data()

        if led_pos and serial_buffer:
            msg = serial_buffer.pop(0)
            try:
                led, num_leds, led_state, test_num, max_tests = map(int, msg.split('-'))
                led_mapper.save_led_pos(
                    led=led,
                    angle=angle,
                    pixel_pos=led_pos,
                    led_state=led_state,
                    test_num=test_num
                )
            except ValueError:
                print("Bad serial:", msg)

        if frame is not None:
            cv2.imshow(f"Angle {angle}", frame)

        if cv2.waitKey(1) == ord('q'):
            break

    camera.release()
    serial_manager.close()
    return True


def main():
    led_mapper = LED_Mapper()

    for angle in ANGLES:
        print(f"\nRotate tree to {angle}° and press ENTER")
        input()

        ok = run_mapping_for_angle(angle, led_mapper)
        if not ok:
            print("Mapping aborted")
            return

    # ---- Final 3D fusion ---- #
    led_mapper.compute_3d_positions()
    led_mapper.save_3d_positions_to_cpp()

    print("\n3D LED mapping complete")


if __name__ == "__main__":
    main()
