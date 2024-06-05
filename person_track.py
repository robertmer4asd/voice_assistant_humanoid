import numpy as np
import cv2
import time
from Adafruit_PCA9685 import PCA9685

# Initialize PCA9685 for servo control
try:
    pwm = PCA9685(address=0x41, busnum=1)
    pwm.set_pwm_freq(50)  # Set the PWM frequency to 50 Hz
except Exception as e:
    print(f"Error initializing PCA9685: {e}")

# Servo settings
servo_channel = 0
servo_channel_face = 1
servo_min = 150  # Min pulse length out of 4096
servo_max = 600  # Max pulse length out of 4096
current_angle = 0  # Track current angle to avoid unnecessary movements
current_angle_face = 80  # Start from 80 degrees
locked_angle = None  # Variable to lock the angle when a person is detected
face_detected = False  # Flag to indicate if a face is detected

def set_servo_angle(channel, angle):
    global current_angle, current_angle_face
    if channel == servo_channel:
        if angle != current_angle:
            try:
                pulse_length = int((angle / 180.0) * (servo_max - servo_min) + servo_min)
                pwm.set_pwm(channel, 0, pulse_length)
                current_angle = angle
                print(f"Servo {channel} angle set to: {angle}")
            except Exception as e:
                print(f"Error setting servo {channel} angle: {e}")
    elif channel == servo_channel_face:
        if angle != current_angle_face:
            try:
                pulse_length = int((angle / 180.0) * (servo_max - servo_min) + servo_min)
                pwm.set_pwm(channel, 0, pulse_length)
                current_angle_face = angle
                print(f"Servo {channel} angle set to: {angle}")
            except Exception as e:
                print(f"Error setting servo {channel} angle: {e}")

# Load pre-trained model and class labels
prototxt_path = 'deploy.prototxt'
model_path = 'MobileNetSSD_deploy.caffemodel'
min_confidence = 0.2

classes = ['background', 'aeroplane', 'bicycle', 'bird', 'boat', 'bottle', 'bus', 'car', 'cat', 'chair',
           'cow', 'diningtable', 'dog', 'horse', 'motorbike', 'person', 'pottedplant', 'sheep', 'sofa', 'train',
           'tvmonitor']
np.random.seed(34732)
colors = np.random.uniform(0, 255, size=(len(classes), 3))

net = cv2.dnn.readNetFromCaffe(prototxt_path, model_path)

# Load face detection model
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Initialize video capture
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open video stream or file")
    exit()

# Reduce frame size to improve performance
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Flag to control servo sweeping
sweeping = False

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture image")
        break

    frame = cv2.flip(frame, 1)  # Horizontal flip to mirror the image
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    height, width = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)
    net.setInput(blob)
    detections = net.forward()

    screen_center_x = width // 2
    center_threshold = 15
    person_detected_flag = False
    person_box = None  # Variable to store the bounding box of the detected person

    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        class_index = int(detections[0, 0, i, 1])
        class_name = classes[class_index]
        print(f"Class: {class_name}, Confidence: {confidence}")

        if confidence > min_confidence and class_name == 'person':
            person_detected_flag = True
            print("Person detected, stopping servo.")
            locked_angle = current_angle  # Lock the angle when a person is detected

            # Get the bounding box coordinates
            box = detections[0, 0, i, 3:7] * np.array([width, height, width, height])
            person_box = box.astype("int")
            (startX, startY, endX, endY) = person_box
            break

    if locked_angle is not None and not face_detected:
        # Set the servo to the locked angle if a person is detected
        set_servo_angle(servo_channel, locked_angle)

        # Check for faces within the bounding box of the person
        person_roi = gray[startY:endY, startX:endX]
        faces = face_cascade.detectMultiScale(person_roi, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        if len(faces) == 0:
            # No faces detected, move the face searching servo
            if current_angle_face > 0:
                for angle in range(current_angle_face, -1, -1):
                    set_servo_angle(servo_channel_face, angle)
                    time.sleep(0.05)
                    _, frame = cap.read()
                    frame = cv2.flip(frame, 1)
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    person_roi = gray[startY:endY, startX:endX]
                    faces = face_cascade.detectMultiScale(person_roi, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
                    if len(faces) > 0:
                        face_detected = True
                        break
            if len(faces) == 0:
                for angle in range(0, 81):
                    set_servo_angle(servo_channel_face, angle)
                    time.sleep(0.05)
                    _, frame = cap.read()
                    frame = cv2.flip(frame, 1)
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    person_roi = gray[startY:endY, startX:endX]
                    faces = face_cascade.detectMultiScale(person_roi, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
                    if len(faces) > 0:
                        face_detected = True
                        break
        else:
            print(f"Faces detected: {len(faces)}")
            face_detected = True
    else:
        if not person_detected_flag and not face_detected:
            if not sweeping:
                sweeping = True
                for angle in range(0, 41, 1):
                    set_servo_angle(servo_channel, angle)
                    time.sleep(0.05)
                    _, frame = cap.read()
                    frame = cv2.flip(frame, 1)
                    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)
                    net.setInput(blob)
                    detections = net.forward()
                    for i in range(detections.shape[2]):
                        confidence = detections[0, 0, i, 2]
                        class_index = int(detections[0, 0, i, 1])
                        class_name = classes[class_index]
                        print(f"Class: {class_name}, Confidence: {confidence}")
                        if confidence > min_confidence and class_name == 'person':
                            person_detected_flag = True
                            locked_angle = current_angle  # Lock the angle when a person is detected
                            sweeping = False
                            break
                    if person_detected_flag:
                        break
                if not person_detected_flag:
                    for angle in range(40, -1, -1):
                        set_servo_angle(servo_channel, angle)
                        time.sleep(0.05)
                        _, frame = cap.read()
                        frame = cv2.flip(frame, 1)
                        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)
                        net.setInput(blob)
                        detections = net.forward()
                        for i in range(detections.shape[2]):
                            confidence = detections[0, 0, i, 2]
                            class_index = int(detections[0, 0, i, 1])
                            class_name = classes[class_index]
                            print(f"Class: {class_name}, Confidence: {confidence}")
                            if confidence > min_confidence and class_name == 'person':
                                person_detected_flag = True
                                locked_angle = current_angle  # Lock the angle when a person is detected
                                sweeping = False
                                break
                        if person_detected_flag:
                            break

    # Draw the bounding box if a person is detected
    if person_box is not None:
        (startX, startY, endX, endY) = person_box
        # Draw a wider purple bounding box
        cv2.rectangle(frame, (startX, startY), (endX, endY), (255, 0, 255), 4)
        # Put text with confidence score and coordinates
        text = f"Person: {confidence:.2f} ({startX}, {startY})-({endX}, {endY})"
        cv2.putText(frame, text, (startX, startY - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 2)

    # Draw face bounding boxes
    if face_detected:
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (startX + x, startY + y), (startX + x + w, startY + y + h), (0, 255, 0), 2)

    cv2.imshow("Detected Objects", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
