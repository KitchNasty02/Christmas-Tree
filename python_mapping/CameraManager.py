import cv2
import numpy as np

# vars for mouse events
start_point = None
end_point = None
drawing = False
final_box = None

# handles mouse events
def mouse_handler(event, x, y, flags, params):
    global start_point, end_point, drawing, final_box

    if event == cv2.EVENT_LBUTTONDOWN:
        start_point = (x, y)
        drawing = True
        end_point = None
        final_box = None
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        if start_point and end_point:
            final_box = (min(start_point[0], end_point[0]), min(start_point[1], end_point[1]),
                         max(start_point[0], end_point[0]), max(start_point[1], end_point[1]))
    elif event == cv2.EVENT_MOUSEMOVE and drawing:
        end_point = (x, y)



class CameraManager:

    # ---- text stuff ---- #
    FONT = cv2.FONT_HERSHEY_SIMPLEX
    TEXT_COLOR = (255, 0, 255)

    # (b, g, r)
    WHITE = (255, 255, 255)
    RED = (0, 0, 255)
    BLUE = (255, 0, 0)
    
    def __init__(self, cam_index=0, frame_multiplier=2):
        self.cam = cv2.VideoCapture(0)

        frame_width = int(self.cam.get(cv2.CAP_PROP_FRAME_WIDTH)) * frame_multiplier
        frame_height = int(self.cam.get(cv2.CAP_PROP_FRAME_HEIGHT)) * frame_multiplier
        self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
        self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)

        self.prev_gray_frame = None
        self.led_text = ""

        print(f"Camera initialized at {frame_width}x{frame_height}")


    # user draws bounding box and saves it
    def draw_and_set_bounding_box(self):
        global start_point, end_point, drawing, final_box
        window_name = 'Draw Bounding Box - Press ENTER to confirm'
        cv2.namedWindow(window_name)
        cv2.setMouseCallback(window_name, mouse_handler)

        final_box = None
        start_point = None
        end_point = None

        while True:
            ret, frame = self.cam.read()
            if not ret:
                break

            if start_point and end_point:
                cv2.rectangle(frame, start_point, end_point, self.RED, 2)

            cv2.imshow(window_name, frame)

            key = cv2.waitKey(1)
            if key == 13 and final_box: # enter key
                self.bounding_box = final_box
                cv2.destroyAllWindows()
                print(f"Bounding Box: {self.bounding_box}")
                return self.bounding_box
            elif key == ord('q'):
                cv2.destroyAllWindows(window_name)
                return None


    # captures a frame and finds led position
    def capture_test(self):
        ret, frame = self.cam.read()
        if not ret:
            print("Failed to capture image")
            return None, None, "Capture error"
        
        current_led_pos = None
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray_frame = cv2.GaussianBlur(gray_frame, (15, 15), 0)

        if self.prev_gray_frame is not None:
            # get difference in current and previous frame
            diff = cv2.absdiff(gray_frame, self.prev_gray_frame)
            _, thresh = cv2.threshold(diff, 50, 255, cv2.THRESH_BINARY)
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            for cnt in contours:
                if cv2.contourArea(cnt) < 5:
                    continue  # filter out noise
                
                (x, y), radius = cv2.minEnclosingCircle(cnt)
                current_led_pos = (int(x), int(y))
                self.led_text = f"LED chage detected at {current_led_pos}" 

                cv2.circle(frame, current_led_pos, int(radius), self.RED, 2)

        if self.bounding_box:
            point1_x, point1_y, point2_x, point2_y = self.bounding_box
            cv2.rectangle(frame, (point1_x, point1_y), (point2_x, point2_y), self.RED, 1)

        cv2.putText(frame, self.led_text, (5, 20), self.FONT, 0.5, self.RED, 1)
        self.prev_gray_frame = gray_frame.copy()

        return current_led_pos, frame, self.led_text

    
    # release and close camera
    def release(self):
        if self.cam:
            self.cam.release()
        cv2.destroyAllWindows()
        print("Camera released")


