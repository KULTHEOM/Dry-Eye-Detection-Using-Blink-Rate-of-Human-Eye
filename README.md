# Dry eye Detection of humans due to prolonged screen time 

This project implements a real-time eye blink detection system to monitor the blink rate and detect potential symptoms of dry eye syndrome. The system uses computer vision techniques to detect facial landmarks and calculate the Eye Aspect Ratio (EAR) to determine whether an eye blink has occurred.


**Overview**

1) Dry Eye Syndrome (DES) is a common condition that occurs when your tears aren't able to provide adequate lubrication for your eyes. One of the symptoms of DES is reduced blinking frequency. This project aims to detect dry eye syndrome by monitoring the blink rate using a webcam.

**How It Works**
1) Face Detection: The system uses dlib to detect the face in the video stream.
2) Facial Landmarks Detection: After detecting the face, the system identifies specific facial landmarks, particularly around the eyes.
3) Eye Aspect Ratio (EAR) Calculation: The EAR is calculated to determine whether the eyes are closed or open.
4) Blink Detection: If the EAR value falls below a threshold (blink_thresh) for a certain number of frames (tt_frame), it is considered a blink.
5) Dry Eye Detection: If the blink count is below a certain threshold over a set period (e.g., 10 blinks per minute), the system alerts the user with an audio signal.

**Key Features:**
1) Real-time blink detection: Detects blinks using the Eye Aspect Ratio (EAR).
2) Dry eye alert: Notifies the user if their blink rate falls below a set threshold, which may indicate dry eye syndrome.
3) FPS Display: Displays the frames per second (FPS) for performance monitoring.

**Dependencies**

1) Python 3.6+
2) OpenCV
3) dlib
4) imutils
5) scipy

**Blink Detection **

1) ![image](https://github.com/user-attachments/assets/832eab64-792b-46c8-a544-a52d9941da4a)



