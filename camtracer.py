import cv2
import mediapipe as mp
import pyautogui
import sys

# Mediapipe eller modülünü yükleme
mp_hands = mp.solutions.hands

# Kamerayı başlatma
cap = cv2.VideoCapture(0)

# Kamera görüntüsünü aynalama
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
cap.set(cv2.CAP_PROP_FPS, 60)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)

# Önceki el konumunu saklamak için değişkenler
prev_index_tip_x, prev_index_tip_y = None, None
prev_thumb_tip_x, prev_thumb_tip_y = None, None

# Sol tıklama durumunu izlemek için bir bayrak
left_clicked = False
righ_clicked = False
double_clicked = False

with mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Görüntüyü yatay olarak aynalama
        frame = cv2.flip(frame, 1)

        # Görüntüyü RGB'ye dönüştürme
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Görüntüyü mediapipe'a işleme
        results = hands.process(rgb_frame)

        # Eğer el tespit edilirse
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # İşaret ve baş parmak noktalarını al
                index_finger = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
                thumb = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
                middle_finger = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
                ring_finger = hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP]

                # El izleme işlevselliği
                # İki parmak arasındaki mesafeyi hesaplama
                distance = ((index_finger.x - thumb.x) ** 2 + (index_finger.y - thumb.y) ** 2) ** 0.5
                distance2 = ((thumb.x - middle_finger.x) ** 2 + (thumb.y - middle_finger.y) ** 2) ** 0.5


                # İki parmak birbirine çok yakınsa
                if distance < 0.04:
                    # Eğer daha önce tıklanmadıysa
                    if not left_clicked:
                        pyautogui.click(button='left')  # Sol tık basma
                        left_clicked = True
                else:
                    left_clicked = False

                #!sağ tık
                if distance2 < 0.05:
                    # Eğer daha önce tıklanmadıysa
                    if not right_clicked:
                        pyautogui.click(button='right')  # Sağ tık basma
                        right_clicked = True
                else:
                    right_clicked = False


                #!çift tık

                if distance < 0.06:
                    # Eğer daha önce çift tıklanmadıysa
                    if not double_clicked:
                        pyautogui.doubleClick()  # Çift tıklama yapma
                        double_clicked = True
                else:
                    double_clicked = False



                # El izleme işlevselliği
                # Fare hareketlerini hesaplama
                if prev_index_tip_x is not None and prev_index_tip_y is not None:
                    mouse_movement_x = int((index_finger.x - prev_index_tip_x) * 1000)
                    mouse_movement_y = int((index_finger.y - prev_index_tip_y) * 1000)

                    # Fareyi hareket ettirme
                    pyautogui.moveRel(mouse_movement_x, mouse_movement_y)

                # El kapanma durumunu kontrol etme
                if index_finger.y < thumb.y:  # İşaret parmağı, baş parmağın altındaysa
                    hand_closed = False
                else:
                    hand_closed = True

                # El tamamen kapanırsa programı sonlandırma
                if hand_closed:
                    cap.release()
                    cv2.destroyAllWindows()
                    sys.exit()

                # Önceki parmak konumunu güncelleme
                prev_index_tip_x, prev_index_tip_y = index_finger.x, index_finger.y

        # Görüntüyü gösterme
        cv2.imshow("Hand Tracking", frame)

        # Çıkış için 'q' tuşuna basma kontrolü
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# Kamera ve pencereleri serbest bırakma
cap.release()
cv2.destroyAllWindows()

# Uygulamayı kapatma
sys.exit()
