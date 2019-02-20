# Drowsiness Detection OpenCV
Project to detect user's eyes for signs of drowsiness and alert user/driver.


## Applications
This can be used by riders who tend to drive for a longer period of time that may lead to accidents


### Requirements
Python 3.6 or higher is needed.


### Dependencies
1) import cv2
2) import immutils
3) import dlib
4) import scipy


### Description
A computer vision system that can automatically detect driver drowsiness in a real-time video stream and then play an alarm if the driver appears to be drowsy.
Currently working on creating a docker image for this program to deal with the needed dependencies


### Algorithm
Each eye is represented by 6 (x, y)-coordinates, starting at the left-corner of the eye (as if you were looking at the person), and then working clockwise around the eye:.

<img src="readme_resources/eye1.jpg">


### Condition
It checks 20 consecutive frames and if the Eye Aspect ratio is lesst than 0.25, Alert is generated.


#### Formula for Eye Aspect Ratio
<img src="readme_resources/eye2.png">


#### Usage graph
<img src="readme_resources/eye3.jpg">

View article referenced for this project [here](https://www.pyimagesearch.com/2017/05/08/drowsiness-detection-opencv/)


### Execution
To run the code, assuming python refers to python3
```
python main.py
```