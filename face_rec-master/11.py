import cv2


cap = cv2.VideoCapture(0)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter("./open7.avi" , fourcc, 20.0, (width,height),True)

while cap.isOpened():
    ret,frame = cap.read()
    out.write(frame)
    cv2.imshow('blink',frame)
    if cv2.waitKey(5)==27:
        break

cv2.imshow("cv2",frame)
cap.release()
out.release()
cv2.destroyAllWindows()

























