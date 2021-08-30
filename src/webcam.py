import cv2
import imutils
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array


class camera():

    def camera():
        face_detector = cv2.CascadeClassifier('openCV/data/haarcascades/haarcascade_frontalface_default.xml')
        model = load_model('best_model.h5')

        EMOTIONS = ['Angry','Happy','Neutral','Sad']
        capture = cv2.VideoCapture(0)

        img = ()

        while True:
            ret, frame = capture.read()

            rects = face_detector.detectMultiScale(
                frame,scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30,30),
                flags=cv2.CASCADE_SCALE_IMAGE)

            if len(rects) > 0:
                rect = sorted(rects, reverse=True,
                            key=lambda x:(x[2]-x[0])*(x[3]-x[1]))[0]
                (fX, fY, fW, fH) = rect
                roi =  frame[fY:fY+fH,fX:fX+fW]
                
                #used to match the same dimensions as the model         
                roi = cv2.resize(roi,(48,48))
                roi = roi.astype("float32") / 255.0
                roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
                roi = img_to_array(roi)
                roi = np.expand_dims(roi,axis=0)

                #gives emotion prediction on video
                predicts = model.predict(roi)[0]
                label = EMOTIONS[predicts.argmax()]

                if label == 'Angry':
                    color = (0,0,255)
                elif label == 'Happy':
                    color = (0,255,255)
                elif label == 'Sad':
                    color = (129, 76, 15)
                elif label == 'Neutral':
                    color = (146, 135, 152)

                cv2.putText(frame,label,(fX,fY-10), 
                            cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),2, cv2.LINE_AA)

                cv2.rectangle(frame,(fX,fY),(fX+fW,fY+fH), 
                            color,4,cv2.LINE_AA)
            cv2.imshow('Emotion Detection', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                image = frame
                break

        capture.release()
        cv2.destroyAllWindows()
        return str(label)
