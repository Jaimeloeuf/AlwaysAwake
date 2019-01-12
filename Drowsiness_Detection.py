from scipy.spatial import distance
from imutils import face_utils
import imutils
import dlib
import cv2

# Define the function for calculating eye aspect ratio with eucilidean distance
def eye_aspect_ratio(eye):
    # Calculate the distance between the 3 pairs of point.
    A = distance.euclidean(eye[1], eye[5])
    B = distance.euclidean(eye[2], eye[4])
    C = distance.euclidean(eye[0], eye[3])
    # Find the EAR and return to function caller
    return ((A + B) / (2.0 * C))


thresh = 0.22 # Threshold value for the Eye Aspect Ratio.
blink = 2 # Number of frames where EAR is below threshold before counted as a blink
frame_check = 3 # Number of frames where EAR is below threshold before counted as falling asleep
count = 0 # Global variable used to keep track of the consecutive number of times the 'EAR' is below threshold

# Get a function from dlib to be used to detect faces, or 'subjects'
detect = dlib.get_frontal_face_detector()
# Get the .dat file that stores the prediction model used by dlib, and pass it into the function to get a model out.
predict_data = dlib.shape_predictor(r"C:\Users\user\Documents\Projects\Drowsiness_Detection\shape_predictor_68_face_landmarks.dat")

# Give names to the detected features, 'eyes'
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS["right_eye"]

# Start the video stream capture process with openCV 2
cap = cv2.VideoCapture(0)

while True:
    # Read and store the newly captured image
    ret, frame = cap.read()
    # Redraw the frame if neccessary to capture less data which means less processing power needed.
    # frame = imutils.resize(frame, width=450) # is this needed?
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Detect faces, after applying the filter for color recognition
    subjects = detect(gray, 0)
    # Loop through all the faces detected, if there is more than one
    for subject in subjects:
        shape = predict_data(gray, subject)
        # Convert the shape data to a NumPy Array
        shape = face_utils.shape_to_np(shape)
        leftEye = shape[lStart:lEnd]
        rightEye = shape[rStart:rEnd]

        # Calculate the EAR for both eyes and store them, to calculate the average EAR
        leftEAR = eye_aspect_ratio(leftEye)
        rightEAR = eye_aspect_ratio(rightEye)
        ear = (leftEAR + rightEAR) / 2.0

        # Draw on the frame so that the user can see the eye tracking in real time.
        # Create the contours out before drawing them.
        leftEyeHull = cv2.convexHull(leftEye)
        rightEyeHull = cv2.convexHull(rightEye)
        # To draw out the contours around the eyes
        cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
        cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)

        print("EAR: ", ear)
        if ear < thresh:
            print("EAR Below threshold ", ear)
            count += 1
            print(count)
            if count >= blink:
                print("---------------Blinked!---------------")
            if count >= frame_check:
                # Alert the user by putting text onto the frame directly.
                cv2.putText(frame, "**********************ALERT!**********************", (20, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                cv2.putText(frame, "**********************ALERT!**********************", (20, 460),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        else:
            count = 0 # Reset the count
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
cv2.destroyAllWindows()
cap.stop() # Might not be needed, but still used to kill the process to stop the stream
