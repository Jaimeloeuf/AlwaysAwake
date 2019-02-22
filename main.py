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


# Function to run in Daemonic child process that just reads the face and puts data from I/O into the Queues
def get_face(face_queue, gray_queue, frame_queue):
    # Open the camera by Index 0 for the default camera connected and create a video stream capture object from that.
    cap = cv2.VideoCapture(0)

    # Loop/wait until the video capture is opened
    # while not cv2.VideoCapture.isOpened():
    #     print('Waiting for camera to open')
    
    while True:
        # Read and store the newly captured image
        ret, frame = cap.read()
        # Get the grayscale image out from the original image to make it easier for processing
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Detect faces, after applying the filter for color recognition
        subjects = detect(gray, 0)

        try:
            # Try to get the first/closest face out
            subject = subjects[0]
            # if face detected, meaning that index 0 holds a valid value, then put face into the Queue
            face_queue.put(subject)
            # Put the grayscale image and the frame into their Respective Queues too
            gray_queue.put(gray)
            frame_queue.put(frame)
        except:
            # If index 0 is null, indexError will be raised, meaning no face detected.
            # Even if there is no face detected, put frame into Queue to continue displaying video feed
            frame_queue.put(frame)


# Function to run in child process to predict Drowsiness based on the images/faces read from the Queues
def prediction_func(face_queue, gray_queue, frame_queue):
    quit_flag = False
    thresh = 0.22  # Threshold value for the Eye Aspect Ratio.
    count = 0  # Variable used to keep track of the consecutive number of times the 'EAR' is below threshold

    # Infinite loop to read frames from the video output and put into a queue

    # Loop till user press q to set the quit_flag in order to quit the program
    while not quit_flag:
        # Read the pipe, do the below only if image avail in the pipe
        while not face_queue.empty():

            # Get the last face in the face queue
            face = face_queue.get()
            while face_queue.qsize():
                face = face_queue.get()

            gray = gray_queue.get()
            while gray_queue.qsize():
                gray = gray_queue.get()

            shape = predict_data(gray, face)
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
            while frame_queue.qsize():
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

            if (cv2.waitKey(1) & 0xFF) == ord("q"):
                # Set a quit flag
                quit_flag = True
                break

        # Even if there is no face detected, the frame should still be read and displayed
        cv2.imshow("Frame", frame_queue.get())

        if (cv2.waitKey(1) & 0xFF) == ord("q"):
            # Break the loop if user pressed 'q' when no subjects are detected
            break


def main():
    # Use the 'spawn' method to start a new Process
    mp.set_start_method('spawn')
    
    # Create the Queue objects for the different data
    face_queue = mp.Queue()
    gray_queue = mp.Queue()
    frame_queue = mp.Queue()

    # Spawn a new Daemonic Process to get the face of the user, Daemonic to allow auto exit/close upon main Process ending.
    get_face_p = mp.Process(target=get_face, args=(face_queue, gray_queue, frame_queue,), daemon=True)
    # Start the Process immediately after creation
    get_face_p.start()

    # Spawn a new Process to do the prediction and detection of the User's eyes
    prediction_func_p = mp.Process(target=prediction_func, args=(face_queue, gray_queue, frame_queue,))
    # Start the Process immediately after creation
    prediction_func_p.start()


    # The signal handler should not be used.
    import signal
    def signal_handler(signal, frame):
        print("Program interrupted!")
        # Close the camera and the display window
        cv2.destroyAllWindows()

        # Close and destroy all the Queues
        face_queue.close()
        gray_queue.close()
        frame_queue.close()


        # Below no longer needed as the Process is daemonic
        # Kill and Stop the get_face process with a SIGTERM signal
        # get_face_p.terminate()

        exit(0)

    # Pass in the signal_handler to run when the INTerrupt signal is received
    # signal.signal(signal.SIGINT, signal_handler)


    # Wait for the predicition process to end on Key Press
    prediction_func_p.join()
    
    # Destroy all the HighGUI windowws
    cv2.destroyAllWindows()

    # Close all the Queues to release the resources and prevent program corruption
    face_queue.close()
    gray_queue.close()
    frame_queue.close()

   
    # No longer need to kill process like below since the get_face_p Process is now ran as a Daemonic Process

    # Always close all the Queues before terminating the Processes to preven the Queues from corrupting

    # Kill and Stop the get_face process with a SIGTERM signal
    # get_face_p.terminate()
    # get_face_p.join()
    # get_face_p.close()



if __name__ == "__main__":
    # Run the main function if this module used as program entry point
    main()