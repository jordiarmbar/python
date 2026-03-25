import cv2
import math
import mediapipe as mp

class HandDetector:
    def __init__(self):
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(min_detection_confidence=0.7)
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [4, 8, 12, 16, 20] # Pulgar, índice, medio, anular, meñique

    def find_hands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def find_position(self, img):
        self.lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[0]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lmList.append([id, cx, cy])
        return self.lmList

    def fingers_up(self):
        fingers = []
        if len(self.lmList) != 0:
            # Pulgar (eje X)
            if self.lmList[self.tipIds[0]][1] > self.lmList[self.tipIds[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)
            # Resto de dedos (eje Y)
            for id in range(1, 5):
                if self.lmList[self.tipIds[id]][2] < self.lmList[self.tipIds[id] - 2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)
        return fingers

    def find_distance(self, p1, p2):
        if len(self.lmList) != 0:
            x1, y1 = self.lmList[p1][1], self.lmList[p1][2]
            x2, y2 = self.lmList[p2][1], self.lmList[p2][2]
            length = math.hypot(x2 - x1, y2 - y1)
            return length, (x1, y1, x2, y2)
        return 0, (0,0,0,0)