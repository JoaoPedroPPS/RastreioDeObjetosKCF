import cv2
import sys

(major_ver, minor_ver, subminor_ver) = cv2.__version__.split('.')

if __name__ == '__main__':

    tracker_type = 'KCF'

    if int(minor_ver) < 3:
        tracker = cv2.Tracker_create(tracker_type)
    else:
        tracker = cv2.TrackerKCF_create()
        

    video = cv2.VideoCapture("videos\catPiano.mp4")


    if not video.isOpened():
        print("Nao foi possivel abrir o video")
        sys.exit()

    ok, frame = video.read()
    if not ok:
        print('Nao foi possivel ler o video')
        sys.exit()


    bbox = (287, 23, 86, 320)

 
    bbox = cv2.selectROI(frame, False)


    ok = tracker.init(frame, bbox)

    while True:
        
        ok, frame = video.read()
        if not ok:
            break

       
        timer = cv2.getTickCount()

        ok, bbox = tracker.update(frame)

        fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)

        if ok:
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)
        else:
            cv2.putText(frame, "Falha no rastreio detectada", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)


        cv2.putText(frame, tracker_type + " Rastreio", (100, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2)


        cv2.putText(frame, "FPS : " + str(int(fps)), (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2)

        cv2.imshow("Rastreando", frame)


        k = cv2.waitKey(1) & 0xff
        if k == 27:
            break
