from __future__ import print_function
import cv2 as cv
from .eye_status import *
import random
import face_recognition
import os

os.environ["TF_KERAS"] = '1'


def detectAndDisplay(frame, face_detector, eyes_detector, model, Capture, frames, left_eye_dectector,
                     right_eye_dectector):
    frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    frame_gray = cv.equalizeHist(frame_gray)
    tmp = ''
    # -- Detect faces
    faces = face_detector.detectMultiScale(frame_gray, minNeighbors=10)
    for (x, y, w, h) in faces:
        left = frame[y:y + h, x + int(w / 2):x + w]
        right = frame[y:y + h, x:x + int(w / 2)]
        left_gray = frame_gray[y:y + h, x + int(w / 2):x + w]
        right_gray = frame_gray[y:y + h, x:x + int(w / 2)]
        eye_state = [2, 2]
        eye_num = 0
        left_pos = ()
        right_pos = ()
        # center = (x + w//2, y + h//2)
        # frame = cv.ellipse(frame, center, (w//2, h//2), 0, 0, 360, (255, 0, 255), 4)
        # -- In each face, detect eyes
        left_eye = left_eye_dectector.detectMultiScale(left_gray, minNeighbors=5)
        for (x2, y2, w2, h2) in left_eye:
            eye_num += 1
            # eye_center = (x + x2 + w2//2 + w//2, y + y2 + h2//2)
            left_eye_frame = left[y2:y2 + h2, x2:x2 + w2]
            left_pos = (x + x2 + int(w / 2), y + y2, w2, h2)
            # cv.imshow('left',left[y2:y2+h2,x2:x2+w2])
            pred = predict(left_eye_frame, model)
            if pred == 'open':
                eye_state[0] = 1
            elif pred == 'closed':
                eye_state[0] = 0
            # radius = int(round((w2 + h2)*0.25))
            # # frame = cv.circle(frame, eye_center, radius, (255, 0, 0 ), 4)
        right_eyes = right_eye_dectector.detectMultiScale(right_gray, minNeighbors=5)
        for (x2, y2, w2, h2) in right_eyes:
            eye_num += 1
            right_eye_frame = right[y2:y2 + h2, x2:x2 + w2]
            # cv.imshow('right',right_eye_frame)
            right_pos = (x + x2, y + y2, w2, h2)
            # eye_center = (x + x2 + w2 // 2, y + y2 + h2 // 2)
            # radius = int(round((w2 + h2) * 0.25))
            # frame = cv.circle(frame, eye_center, radius, (255, 0, 0), 4)
            pred = predict(right_eye_frame, model)
            if pred == 'open':
                eye_state[1] = 1
            elif pred == 'closed':
                eye_state[1] = 0
        if eye_num == 2:
            frames.append(frame)
            if eye_state[0] == 0 and eye_state[1] == 0:
                tmp += '0'
            else:
                tmp += '1'
            for i in range(4):
                if Capture.isOpened():
                    _, frame = Capture.read()
                    if frame is None:
                        break
                    frames.append(frame)
                    l_eyes = left_eye_dectector.detectMultiScale(frame, minNeighbors=5)
                    r_eyes = right_eye_dectector.detectMultiScale(frame, minNeighbors=5)
                    if len(left_pos) != 0 and len(right_pos) != 0:
                        left_pred = predict(
                            frame[left_pos[1]:left_pos[1] + left_pos[3], left_pos[0]:left_pos[0] + left_pos[2]], model)
                        right_pred = predict(
                            frame[right_pos[1]:right_pos[1] + right_pos[3], right_pos[0]:right_pos[0] + right_pos[2]],
                            model)
                        print(left_pred,right_pred)
                        # cv.imshow('right',
                        #          frame[right_pos[1]:right_pos[1]+right_pos[3],right_pos[0]:right_pos[0]+right_pos[2]])
                        if left_pred == "closed" or right_pred == "closed":
                            tmp += '0'
                        else:
                            tmp += '1'
                    else:
                        tmp += '1'
            print(tmp)
            if isBlinking(tmp):
                return True
    return False

    # cv.imshow('Capture - Face detection', frame)


def isBlinking(history):
    """ @history: A string containing the history of eyes status
         where a '1' means that the eyes were closed and '0' open.
        @maxFrames: The maximal number of successive frames where an eye is closed """
    patterns = ['010', '101', '1001', '10001', '0110']
    for pattern in patterns:
        if pattern in history:
            return True
    return False


def initial():
    # load pre-trained model
    pth = 'D:\Desk\Face_check\\face_rec-master\\'
    face_cascPath = pth + 'haarcascade_frontalface_alt.xml'
    open_eye_cascPath = pth + 'haarcascade_eye_tree_eyeglasses.xml'
    left_eye_cascPath = pth + 'haarcascade_lefteye_2splits.xml'
    right_eye_cascPath = pth + 'haarcascade_righteye_2splits.xml'
    # initialize the detector
    face_detector = cv.CascadeClassifier(face_cascPath)
    eyes_detector = cv.CascadeClassifier(open_eye_cascPath)
    left_eye_dectector = cv.CascadeClassifier(left_eye_cascPath)
    right_eye_dectector = cv.CascadeClassifier(right_eye_cascPath)
    # used to dectect blink motion
    # load eyes state detector model
    model = load_model()
    return (face_detector, eyes_detector, model, left_eye_dectector, right_eye_dectector)


def run(video_path, img_path):
    face_detector, eyes_detector, model, left_eye_detector, right_eye_detector = initial()
    result = False
    frames = []
    # -- 2. Read the video stream
    cap = cv.VideoCapture(video_path)
    if not cap.isOpened:
        print('--(!)Error opening video capture')
        exit(0)
    ret = [False]
    while cap.isOpened():
        ret, frame = cap.read()
        if frame is None:
            print('--(!) No captured frame -- Break!')
            break
        result = detectAndDisplay(frame, face_detector, eyes_detector, model, cap, frames, left_eye_detector,
                                  right_eye_detector)
        if result:
            ret = test(frames, img_path)
            break

        if cv.waitKey(10) == 27:
            break
    if type(ret)==list:
        ret = ret[0]
    print(ret)
    return ret



def test(frames,img_path):
    count = 0
    img_test = img_path
    imgTest = face_recognition.load_image_file(img_test)
    imgTest = cv.cvtColor(imgTest, cv.COLOR_BGR2RGB)
    encoding_test = face_recognition.face_encodings(imgTest)[0]
    num = min(len(frames), 10)
    for i in range(min(len(frames), 10)):
        frame = frames[i]
        frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        encoding_frame = face_recognition.face_encodings(frame)
        if len(encoding_frame) > 0:
            encoding_frame = encoding_frame[0]
            result = face_recognition.compare_faces([encoding_test], encoding_frame, tolerance=0.5)[0]
            if result:
                count += 1
        else:
            num -= 1
    print(count / num)
    if count / num >= 0.8:
        return True
    return False

#
# res,frames = run()
# if(res):
#     print(test(frames))
# else:
#     print("验证失败")
