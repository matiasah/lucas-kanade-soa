import cv2 as cv
import numpy as np
import time
from flask import Blueprint, render_template, jsonify, send_file, request
from werkzeug.datastructures import ImmutableMultiDict

mod = Blueprint('LK', __name__)


@mod.route('/lucas-kanade', methods=['POST'])
def optical_flow():
    
    video = request.files['video']

    video.save("uploads/" + video.filename)        

    start = time.time()

    # Parameters for Shi-Tomasi corner detection
    feature_params = dict(maxCorners = 300, qualityLevel = 0.1, minDistance = 2, blockSize = 7)

    # Parameters for Lucas-Kanade optical flow
    lk_params = dict(winSize = (15,15), maxLevel = 5, criteria = (cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 0.03))

    path = "uploads/" + video.filename
    # The video feed is read in as a VideoCapture object
    cap = cv.VideoCapture(path)

    # Variable for color to draw optical flow track
    color = (0, 0, 255)

    # ret = a boolean return value from getting the frame, first_frame = the first frame in the entire video sequence
    ret, first_frame = cap.read()

    # Converts frame to grayscale because we only need the luminance channel for detecting edges - less computationally expensive
    prev_gray = cv.cvtColor(first_frame, cv.COLOR_BGR2GRAY)

    # Finds the strongest corners in the first frame by Shi-Tomasi method - we will track the optical flow for these corners
    # https://docs.opencv.org/3.0-beta/modules/imgproc/doc/feature_detection.html#goodfeaturestotrack
    prev = cv.goodFeaturesToTrack(prev_gray, mask = None, **feature_params)

    # Creates an image filled with zero intensities with the same dimensions as the frame - for later drawing purposes
    mask = np.zeros_like(first_frame)

    count_frames = 0

    # Tamaño del video
    size = np.array(prev_gray).shape
    size = ( size[1], size[0] )
    pathOut = "output/" + video.filename
    fps = 30
    
    fourcc = cv.VideoWriter_fourcc(*"MJPG")
    out = cv.VideoWriter(pathOut, fourcc, 30.0, size, True)

    while(cap.isOpened()):    

        count_frames += 1

        if (count_frames > 60):
            prev = cv.goodFeaturesToTrack(prev_gray, mask = None, **feature_params)
            count_frames = 0
            mask = np.zeros_like(first_frame)

        # ret = a boolean return value from getting the frame, frame = the current frame being projected in the video
        ret, frame = cap.read()    

        try:    
            # Converts each frame to grayscale - we previously only converted the first frame to grayscale
            gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        
            # Calculates sparse optical flow by Lucas-Kanade method
            # https://docs.opencv.org/3.0-beta/modules/video/doc/motion_analysis_and_object_tracking.html#calcopticalflowpyrlk
            next, status, error = cv.calcOpticalFlowPyrLK(prev_gray, gray, prev, None, **lk_params)

            ## Cuando desaparecen todos los puntos del frame
            if next is None:        
                prev = cv.goodFeaturesToTrack(prev_gray, mask = None, **feature_params)
                next, status, error = cv.calcOpticalFlowPyrLK(prev_gray, gray, prev, None, **lk_params)        

        except Exception:
            print("Bye")
            break
        # Selects good feature points for previous position
        good_old = prev[status == 1]

        # Selects good feature points for next position
        good_new = next[status == 1]

        # Draws the optical flow tracks
        for i, (new, old) in enumerate(zip(good_new, good_old)):

            # Returns a contiguous flattened array as (x, y) coordinates for new point
            a, b = new.ravel()

            # Returns a contiguous flattened array as (x, y) coordinates for old point
            c, d = old.ravel()

            ## Calcular la velocidad para emitir una alerta
            desplazamiento = np.array((a,b)) - np.array((c,d))
            if( desplazamiento[0] > 2 and desplazamiento[1] > 2):
                print("Hay movimiento!!!")

            # Draws line between new and old position with green color and 2 thickness
            #mask = cv.line(mask, (a, b), (c, d), color, 2)

            # Draws filled circle (thickness of -1) at new position with green color and radius of 3
            frame = cv.circle(frame, (a, b), 5, color, -1)        

        # Overlays the optical flow tracks on the original frame
        output = cv.add(frame, mask)

        out.write(output)

        # Updates previous frame
        prev_gray = gray.copy()

        # Updates previous good feature points
        prev = good_new.reshape(-1, 1, 2)        

        # Frames are read by intervals of 10 milliseconds. The programs breaks out of the while loop when the user presses the 'q' key
        if cv.waitKey(10) & 0xFF == ord('q'):
            break

    end = time.time()
    
    out.release()
    return send_file("output/" + video.filename, attachment_filename='video.mp4')