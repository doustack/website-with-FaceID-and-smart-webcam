import cv2
import mediapipe as mp
import time
import tkinter as tk


def run_hand_detection():
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=2,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7
    )
    mp_draw = mp.solutions.drawing_utils

    root = tk.Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.destroy()


    win_w, win_h = screen_width - 100, screen_height - 100


    x = (screen_width - win_w) // 2
    y = (screen_height - win_h) // 2

    cap = cv2.VideoCapture(0)


    cv2.namedWindow("Hand Detection", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Hand Detection", win_w, win_h)
    cv2.moveWindow("Hand Detection", x, y)


    close_time = None  
    admin_time = None  

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(img_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks, handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                label = handedness.classification[0].label  
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                landmarks = hand_landmarks.landmark
                finger_tips = [4, 8, 12, 16, 20]
                fingers = []

            
                for i in range(1, 5):
                    if landmarks[finger_tips[i]].y < landmarks[finger_tips[i] - 2].y:
                        fingers.append(1)
                    else:
                        fingers.append(0)

            
                if label == "Right":
                    if landmarks[finger_tips[0]].x < landmarks[finger_tips[0] - 1].x:
                        fingers.append(1)
                    else:
                        fingers.append(0)
                else:
                    if landmarks[finger_tips[0]].x > landmarks[finger_tips[0] - 1].x:
                        fingers.append(1)
                    else:
                        fingers.append(0)

                finger_count = fingers.count(1)

            
                x_min = int(min([lm.x for lm in hand_landmarks.landmark]) * frame.shape[1])
                y_min = int(min([lm.y for lm in hand_landmarks.landmark]) * frame.shape[0])

                cv2.putText(frame, f"{label} Hand", (x_min, y_min - 25), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)

            
                cv2.putText(frame, f"Fingers = {finger_count}", (x_min, y_min - 5), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,165,255), 2)

            
                if label == "Left" and finger_count == 1 and close_time is None:
                    close_time = time.time() + 5  

            
                if label == "Right" and finger_count == 3 and admin_time is None:
                    admin_time = time.time() + 5  

        if admin_time:
            remaining = int(admin_time - time.time())
            if remaining > 0:
                cv2.putText(frame, f"Admin Login in {remaining}s ...", (50, 100),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (150,80,20), 2)
            else:
                return True
                break
            
        if close_time:
            remaining = int(close_time - time.time())
            if remaining > 0:
                cv2.putText(frame, f"Closing in {remaining}s ...", (50, 70),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
            else:
                break  

        cv2.imshow("Hand Detection", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return False

