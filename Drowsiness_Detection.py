from scipy.spatial import distance
from imutils import face_utils
import imutils
import dlib
import cv2

import multiprocessing as mp

# Define the function for calculating eye aspect ratio with eucilidean distance
def eye_aspect_ratio(eye):
    # Calculate the distance between the 3 pairs of point.
    A = distance.euclidean(eye[1], eye[5])
    B = distance.euclidean(eye[2], eye[4])
    C = distance.euclidean(eye[0], eye[3])
    # Find the EAR and return to function caller
    return ((A + B) / (2.0 * C))


# Get a function from dlib to be used to detect faces, or 'subjects'
detect = dlib.get_frontal_face_detector()
# Get the .dat file that stores the prediction model used by dlib, and pass it into the function to get a model out.
# Use relative location for the shape predictor file instead of abs. path for consistency across different filesystems.
# Should I use the os.path to get current PWD in order to get the address or just do relative import?
predict_data = dlib.shape_predictor('./shape_predictor_68_face_landmarks.dat')

# Give names to the detected features, 'eyes'
(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_68_IDXS["right_eye"]

# Start the video stream capture process with openCV 2. Open the camera by Index 0
cap = cv2.VideoCapture(0)


# Function to run in child process that deals with just reading the face and not predicting
def get_face(queue, gray_queue, frame_queue):
    while True:
        # Read and store the newly captured image
        ret, frame = cap.read()
        # Redraw the frame if neccessary to capture less data which means less processing power needed.
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Detect faces, after applying the filter for color recognition
        subjects = detect(gray, 0)

        try:
            # Try to get the first/closest face out
            subject = subjects[0]
            # if face detected, meaning that index 0 holds a valid value, then put face into the Queue
            queue.put(subject)
            # Put the grayscale image and the frame into their Respective Queues too
            gray_queue.put(gray)
            frame_queue.put(frame)
        except:
            # Should I still pass in a frame or grayscale into the pipe for the user to see?
            frame_queue.put(frame)

            # If index 0 is null, meaning no face is detected, skip this loop and read another frame
            continue


def prediction_func(queue, gray_queue, frame_queue):
    quit_flag = False
    thresh = 0.22  # Threshold value for the Eye Aspect Ratio.
    count = 0  # Variable used to keep track of the consecutive number of times the 'EAR' is below threshold

    # Infinite loop to read frames from the video output and put into a queue

    # Loop till user press q to set the quit_flag in order to quit the program
    while not quit_flag:

        print('No subject found in da frame')
        print(frame_queue.qsize())

        # Read the pipe, do the below only if image avail in the pipe
        while not queue.empty():

            shape = predict_data(gray_queue.get(), queue.get())
            # Convert the shape data to a NumPy Array
            shape = face_utils.shape_to_np(shape)
            leftEye = shape[lStart:lEnd]
            rightEye = shape[rStart:rEnd]

            ear = (eye_aspect_ratio(leftEye) + eye_aspect_ratio(rightEye)) / 2.0

            # Draw on the frame so that the user can see the eye tracking in real time.
            # Create the contours out before drawing them.
            leftEyeHull = cv2.convexHull(leftEye)
            rightEyeHull = cv2.convexHull(rightEye)

            frame = frame_queue.get()

            # To draw out the contours around the eyes
            cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
            cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)

            print(f"EAR: {ear}")
            if ear < thresh:
                count += 1
                # Number of frames where EAR is below threshold before counted as falling asleep
                if count >= 3:
                    # Alert the user by putting text onto the frame directly.
                    cv2.putText(frame, "**********************ALERT!**********************", (20, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    cv2.putText(frame, "**********************ALERT!**********************", (20, 460),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    # Alert the user by sounding the alarm.
                    # Pass the event via the data
                    # alarm()
            else:
                count = 0  # Reset the count

            # Read the frame from the Queue to display
            cv2.imshow("Frame", frame)

            # if (cv2.waitKey(1) & 0xFF) == ord("q"):
            #     # Set a quit flag
            #     quit_flag = True
            #     break
            if not waitKey():
                quit_flag = True
                break

        # Read the frame from the Queue to display
        cv2.imshow("Frame", frame_queue.get())

        if not waitKey():
            break



def waitKey(time =1):
    if (cv2.waitKey(time) & 0xFF) == ord("q"):
        # Set a quit flag
        quit_flag = True
        return False


def main():
    # Use the 'spawn' method to start a new Process
    mp.set_start_method('spawn')
    
    # Create the Queue objects
    queue = mp.Queue()

    gray_queue = mp.Queue()
    frame_queue = mp.Queue()

    # Spawn a new Process to get the face of the user.
    p = mp.Process(target=get_face, args=(queue, gray_queue, frame_queue,))
    # Start the Process immediately
    p.start()

    # Spawn a new Process to do the prediction and detection of the User's eyes
    prediction_func_p = mp.Process(target=prediction_func, args=(queue, gray_queue, frame_queue,))
    prediction_func_p.start()

    import signal
    def signal_handler(signal, frame):
        print("Program interrupted!")
        # Close the camera and the display window
        cv2.destroyAllWindows()

        # Close and destroy all the Queues
        queue.close()
        gray_queue.close()
        frame_queue.close()
        exit(0)

    # Pass in the signal_handler to run when the INTerrupt signal is received
    signal.signal(signal.SIGINT, signal_handler)


    # Wait for the predicition process to end on Key Press
    prediction_func_p.join()
    
    print('Q is pressed to kill')
    # Note that the above is called but nothing happens, the "async callback is terminated"
    
    cv2.destroyAllWindows()
    print('Window is destroyed')

    queue.close()
    gray_queue.close()
    frame_queue.close()

    print('All the queues are closed')



if __name__ == "__main__":
    main()



# while True:
#     # Read and store the newly captured image
#     ret, frame = cap.read()
#     # Redraw the frame if neccessary to capture less data which means less processing power needed.
#     # frame = imutils.resize(frame, width=450) # is this needed?
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     # Detect faces, after applying the filter for color recognition
#     subjects = detect(gray, 0)
#     # Loop through all the faces detected, if there is more than one
#     for subject in subjects:
#         shape = predict_data(gray, subject)
#         # Convert the shape data to a NumPy Array
#         shape = face_utils.shape_to_np(shape)
#         leftEye = shape[lStart:lEnd]
#         rightEye = shape[rStart:rEnd]

#         # Calculate the EAR for both eyes and store them, to calculate the average EAR
#         leftEAR = eye_aspect_ratio(leftEye)
#         rightEAR = eye_aspect_ratio(rightEye)
#         ear = (leftEAR + rightEAR) / 2.0

#         # Draw on the frame so that the user can see the eye tracking in real time.
#         # Create the contours out before drawing them.
#         leftEyeHull = cv2.convexHull(leftEye)
#         rightEyeHull = cv2.convexHull(rightEye)
#         # To draw out the contours around the eyes
#         cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
#         cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)

#         print(f"EAR: {ear}")
#         if ear < thresh:
#             count += 1
#             # Number of frames where EAR is below threshold before counted as falling asleep
#             if count >= 3:
#                 # Alert the user by putting text onto the frame directly.
#                 cv2.putText(frame, "**********************ALERT!**********************", (20, 30),
#                             cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
#                 cv2.putText(frame, "**********************ALERT!**********************", (20, 460),
#                             cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
#                 # Alert the user by sounding the alarm.
#                 # Pass the event via the data
#                 # alarm()
#         else:
#             count = 0 # Reset the count
#     cv2.imshow("Frame", frame)

#     if (cv2.waitKey(1) & 0xFF) == ord("q"):
#         break

# cv2.destroyAllWindows()
