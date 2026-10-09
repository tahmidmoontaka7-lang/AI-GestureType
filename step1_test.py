import cv2
import pyautogui
from cvzone.HandTrackingModule import HandDetector

# ওয়েবক্যাম চালু করার জন্য
cap = cv2.VideoCapture(0)

# হ্যান্ড ডিটেক্টর ইনিশিয়ালিজ (maxHands=1 রাখা হয়েছে)
detector = HandDetector(detectionCon=0.8, maxHands=1)

print("System Control Active... Press 'q' to exit.")

# জেসচার রিপিটেশন কন্ট্রোল ভ্যারিয়েবল
last_gesture = -1

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        continue

    # ক্যামেরা মিরর করা
    frame = cv2.flip(frame, 1)

    # হাত ডিটেক্ট করা
    hands, frame = detector.findHands(frame)

    current_gesture = -1

    # hands যদি খালি না থাকে (অর্থাৎ হাত ডিটেক্ট হয়েছে)
    if hands:
        # hands লিস্টের প্রথম উপাদানটি (index 0) হলো আসল হাতের ডিকশনারি
        hand1 = hands[0]

        # হাতটি ডান নাকি বাম তা বের করা ('Left' অথবা 'Right')
        hand_type = hand1["type"]

        # হাতের ল্যান্ডমার্ক পয়েন্টগুলো নেওয়া
        lm_list = hand1["lmList"]

        up_fingers = []

        # ১. বুড়ো আঙুলের (Thumb) জন্য কাস্টম লজিক
        # ফ্লিপ করা স্ক্রিনে ডান ও বাম হাতের বুড়ো আঙুলের দিক আলাদা হয়
        if hand_type == "Right":
            # ডান হাতের বুড়ো আঙুলের মাথা (point 4) যদি গোড়ার (point 5) ডানপাশে থাকে
            if lm_list[4][0] > lm_list[5][0]:
                up_fingers.append(1)
            else:
                up_fingers.append(0)
        else:
            # বাম হাতের বুড়ো আঙুলের মাথা যদি গোড়ার বামপাশে থাকে
            if lm_list[4][0] < lm_list[5][0]:
                up_fingers.append(1)
            else:
                up_fingers.append(0)

        # ২. বাকি ৪টি আঙুলের লজিক (Y কোঅর্ডিনেট তুলনা)
        finger_tips = [8, 12, 16, 20]
        for tip in finger_tips:
            # আঙুলের মাথা (tip) যদি তার নিচের জয়েন্টের (tip - 2) ওপরে থাকে (Y কম মানে ওপরে)
            if lm_list[tip][1] < lm_list[tip - 2][1]:
                up_fingers.append(1)
            else:
                up_fingers.append(0)

        # মোট কয়টি আঙুল খাড়া আছে
        total_fingers = up_fingers.count(1)
        current_gesture = total_fingers

        # স্ক্রিনে লাইভ সঠিক আঙুলের সংখ্যা দেখানো
        cv2.putText(
            frame,
            f'Fingers: {total_fingers}',
            (20, 70),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 0),
            2
        )

    # জেসচার চেঞ্জ হলে কেবল একবার কীবোর্ড অ্যাকশন হবে
    if current_gesture != last_gesture and current_gesture != -1:
        if current_gesture == 1:
            pyautogui.write('A')
            print("Action: Typed 'A'")
        elif current_gesture == 5:
            pyautogui.press('space')
            print("Action: Pressed 'Space'")
        elif current_gesture == 0:
            pyautogui.press('backspace')
            print("Action: Pressed 'Backspace'")

        last_gesture = current_gesture

    # লাইভ ভিডিও উইন্ডো
    cv2.imshow('AI-GestureType - System Control Test', frame)

    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()


