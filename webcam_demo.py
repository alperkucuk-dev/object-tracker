import cv2

cap = cv2.VideoCapture(0)

ret, frame = cap.read()
print(frame.shape)
print(frame[0, 0]) # value of left top pixel

while True:

    ret, frame = cap.read()

    if not ret:
        print("Frame couldn't be read")
        break

    cv2.imshow("Webcam", frame)

    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()

