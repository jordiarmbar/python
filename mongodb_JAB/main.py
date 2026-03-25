import cv2
from HandTrackingModule import HandDetector
from VolumeHandControl import VolumeController
from dao.mongodb_dao import MongoDBDAO
from models.session import Session
from models.volume_event import VolumeEvent


def main():

    cap = cv2.VideoCapture(0)
    detector = HandDetector()
    vol_ctrl = VolumeController()
    db = MongoDBDAO()


    current_session = Session()

    volBar = 400
    volPer = 0
    last_vol = vol_ctrl.get_current_volume()

    while True:
        success, img = cap.read()
        if not success:
            break

        img = detector.find_hands(img)
        lmList = detector.find_position(img)

        if len(lmList) != 0:

            length, coords = detector.find_distance(4, 8)


            fingers = detector.fingers_up()
            pinky_down = fingers[4] == 0


            if pinky_down:
                volBar, volPer = vol_ctrl.set_volume(length)


                if abs(last_vol - vol_ctrl.get_current_volume()) > 1.0:
                    event = VolumeEvent.create_event(last_vol, vol_ctrl.get_current_volume(), length)
                    db.insert_volume_event(event)
                    last_vol = vol_ctrl.get_current_volume()

                cv2.circle(img, (coords[2], coords[3]), 15, (0, 255, 0), cv2.FILLED)


        cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 3)
        cv2.rectangle(img, (50, int(volBar)), (85, 400), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, f'{int(volPer)} %', (40, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 3)


        db_status = "DB: OK" if db.is_connected() else "DB: --"
        color = (0, 255, 0) if db.is_connected() else (0, 0, 255)
        cv2.putText(img, db_status, (450, 50), cv2.FONT_HERSHEY_COMPLEX, 1, color, 2)


        cv2.imshow("Hand Volume Control", img)


        if cv2.waitKey(1) & 0xFF == ord('q') or cv2.getWindowProperty("Hand Volume Control", cv2.WND_PROP_VISIBLE) < 1:
            break


    session_data = current_session.end_session()
    db.insert_session(session_data)
    print("Sesión guardada y finalizada.")

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()