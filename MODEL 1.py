
import cv2
import dlib
import time
from imutils import face_utils
from scipy.spatial import distance as dist
import time
import winsound
from flask import Flask, Response, stream_with_context

app = Flask(__name__)
cam = cv2.VideoCapture(0)
#------------Variables---------#
blink_thresh=0.5
tt_frame = 3
count=0
TOTAL=0


#------#
detector = dlib.get_frontal_face_detector()
lm_model = dlib.shape_predictor("C:/Users/OM/Desktop/Dry eye detection/Eye-Blink-Detector/Model/shape_predictor_68_face_landmarks.dat")

#--Eye ids ---#
(L_start, L_end) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
# print(L_start,L_end)
(R_start, R_end) = face_utils.FACIAL_LANDMARKS_IDXS['right_eye']

ptime = 0


def EAR_cal(eye):
    #----verticle-#
    v1 = dist.euclidean(eye[1],eye[5])
    v2 = dist.euclidean(eye[2],eye[4])

    #-------horizontal----#
    h1 = dist.euclidean(eye[0],eye[3])

    ear = (v1+v2)/h1
    return ear

start_time = time.time()

while 1 :

    if cam.get(cv2.CAP_PROP_POS_FRAMES) == cam.get(cv2.CAP_PROP_FRAME_COUNT) :
        cam.set(cv2.CAP_PROP_POS_FRAMES,0)

    _,frame = cam.read()
    img_gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    #--------fps --------#
    ctime = time.time()
    fps = 1/(ctime-ptime)
    ptime= ctime
    cv2.putText(
        frame,
        f'FPS:{int(fps)}',
        (50,50),
        cv2.FONT_HERSHEY_DUPLEX,
        1,
        (0,0,100),
        1
    )
    #-----facedetection----#
    faces = detector(img_gray)

    for face in faces:
        x1 = face.left()
        y1 = face.top()
        x2 = face.right()
        y2= face.bottom()
        cv2.rectangle(frame,(x1,y1),(x2,y2),(200),2)

        #---------Landmarks------#
        shapes = lm_model(img_gray,face)
        shape = face_utils.shape_to_np(shapes)

        #-----Eye landmarks---#
        lefteye = shape[L_start:L_end]
        righteye = shape[R_start:R_end]

        for Lpt,rpt in zip(lefteye,righteye):
            cv2.circle(frame,Lpt,2,(200,200,0),2)
            cv2.circle(frame, rpt, 2, (200, 200, 0), 2)

        left_EAR = EAR_cal(lefteye)
        right_EAR= EAR_cal(righteye)

        avg =(left_EAR+right_EAR)/2
        # print(avg)
        if avg<blink_thresh :
            count+=1

        else :
            if count>tt_frame:
                TOTAL += 1
            
            count=0
            cv2.putText(frame, "Blinks: {}".format(TOTAL), (10, 30),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            # cv2.putText(frame, "EAR: {:.2f}".format(avg), (300, 30),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

           
            elapsed_time = time.time() - start_time
            cv2.putText(frame, f'Time: {int(elapsed_time)}s', (900, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

          
            if elapsed_time >= 60:
                if TOTAL <=10:
                    cv2.putText(frame,"DRY EYE DETECTED",(10,60),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    winsound.Beep(1000, 10000) 

                    
                TOTAL = 0
                start_time = time.time()

    frame = cv2.resize(frame,(1080,640))

    cv2.imshow("Video" ,frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()