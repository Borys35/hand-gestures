# Music controls using hand gestures

If you want to try it, just clone the repo, open your favourite music player and run the program!

## Prerequirements
You need python installed on your machine and install all dependencies used in main.py.

## Capturing a camera
I use DroidCam to capture my camera, so the code looks like this:
```
# capture video
url = 'http://192.168.100.62:4747/video'
cap = cv.VideoCapture(url)
```
If you have default/built-in webcam, you can use this code instead
```
# capture video
url = ''  # this line can be deleted
cap = cv.VideoCapture(0)
```
