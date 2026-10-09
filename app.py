import math
import threading
import cv2
import pyautogui
from cvzone.HandTrackingModule import HandDetector
from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

detector = HandDetector(detectionCon=0.8, maxHands=1)

# স্মুথ কার্সার মুভমেন্টের জন্য গ্লোবাল ভ্যারিয়েবল
prev_x, prev_y = 0, 0
smoothing_factor = 0.5  # ০.১ থেকে ১.০ (যত কম হবে তত স্মুথ, তবে ল্যাগ বাড়তে পারে)


def webcam_loop():
    global prev_x, prev_y

    cap = cv2.VideoCapture(0)
    cam_width, cam_height = 640, 480
    cap.set(3, cam_width)
    cap.set(4, cam_height)

    last_gesture = -1
    pinch_active = False

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            continue

        # ফ্রেম ফ্লিপ করা (মিরর ইফেক্ট)
        frame = cv2.flip(frame, 1)
        hands, frame = detector.findHands(frame, draw=True)

        current_gesture = -2
        cursor_data = None

        if hands:
            hand1 = hands[0]
            hand_type = hand1["type"]
            lm_list = hand1["lmList"]

            # তর্জনী (Landmark 8) ও বুড়ো আঙুল (Landmark 4)
            index_x, index_y = lm_list[8][0], lm_list[8][1]
            thumb_x, thumb_y = lm_list[4][0], lm_list[4][1]

            # ২ আঙুলের দূরত্ব (Pinch Gesture)
            distance = math.hypot(index_x - thumb_x, index_y - thumb_y)

            # স্ক্রিন নরমালাইজেশন (0-100%)
            raw_cursor_x = int((index_x / cam_width) * 100)
            raw_cursor_y = int((index_y / cam_height) * 100)

            # পজিশন ফিল্টারিং / স্মুথিং
            curr_x = int(prev_x + (raw_cursor_x - prev_x) * smoothing_factor)
            curr_y = int(prev_y + (raw_cursor_y - prev_y) * smoothing_factor)
            prev_x, prev_y = curr_x, curr_y

            is_pinched = False
            if distance < 30:
                if not pinch_active:
                    is_pinched = True
                    pinch_active = True
            else:
                pinch_active = False

            cursor_data = {
                "x": max(0, min(100, curr_x)),
                "y": max(0, min(100, curr_y)),
                "pinch": is_pinched,
            }

            # আঙুল গণনার লজিক (Right/Left Hand সাপোর্টসহ)
            up_fingers = []
            if hand_type == "Right":
                up_fingers.append(1 if lm_list[4][0] < lm_list[3][0] else 0)
            else:
                up_fingers.append(1 if lm_list[4][0] > lm_list[3][0] else 0)

            finger_tips = [8, 12, 16, 20]
            for tip in finger_tips:
                up_fingers.append(
                    1 if lm_list[tip][1] < lm_list[tip - 2][1] else 0
                )

            current_gesture = up_fingers.count(1)

        # ১. কার্সার মুভমেন্ট ও পিঞ্চ ইভেন্ট ফ্রন্টএন্ডে পাঠানো
        if cursor_data:
            socketio.emit("cursor_move", cursor_data)

        # ২. স্পেস ও ব্যাকস্পেস হ্যান্ডলিং
        if current_gesture != last_gesture and current_gesture != -2:
            character = ""
            if current_gesture == 5:
                character = " "
                pyautogui.press("space")
            elif current_gesture == 0:
                character = "backspace"
                pyautogui.press("backspace")

            if character:
                socketio.emit(
                    "gesture_response",
                    {"character": character, "fingers": current_gesture},
                )

            last_gesture = current_gesture
        elif current_gesture == -2:
            last_gesture = -1

        cv2.imshow("AI-GestureType Backend", frame)
        if cv2.waitKey(5) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    t = threading.Thread(target=webcam_loop)
    t.daemon = True
    t.start()

    # Flask SocketIO Server
    socketio.run(app, host="127.0.0.1", port=5000, debug=False)