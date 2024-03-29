from ultralytics import YOLO
import cv2
import math
import time
import requests

# Start webcam

cap = cv2.VideoCapture(0)
cap.set(3, 1800)
cap.set(4, 480)

# Model
model = YOLO("yolo-Weights/yolov8n.pt")

# Timing and counting
detect_interval = 10  # Detect every 10 seconds
detection_duration = 3  # Duration of detection in seconds
last_detection_time = time.time()

# ...

while True:
    success, img = cap.read()
    results = model(img, stream=True)

    # Process coordinates

    for r in results:
        boxes = r.boxes
        for box in boxes:
            cls = int(box.cls[0])  # Get the class ID
            if cls == 0:  # Check if the class ID is 0 (typically 'person')
                # Bounding box coordinates
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

                # Draw the bounding box
                cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

                # Confidence level
                confidence = math.ceil((box.conf[0] * 100)) / 100

                # Display class name (in this case, 'person')
                cv2.putText(img, "person", (x1, y1), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)


    current_time = time.time()

    # Perform detection every 10 seconds
    if current_time - last_detection_time >= detect_interval:
        people_count = []
        detection_start_time = time.time()

        # Detect for 3 seconds
        while time.time() - detection_start_time < detection_duration:
            success, img = cap.read()
            results = model(img, stream=True)

            person_detected = 0
            for r in results:
                boxes = r.boxes
                for box in boxes:
                    if int(box.cls[0]) == 0:  # Class ID for 'person'
                        person_detected += 1
             
            people_count.append(person_detected)

            # Show the webcam image

        # Calculate and print the average number of people detected
        if people_count:
            average_people = math.floor(sum(people_count) / len(people_count))
            print(f"Average number of people detected: {average_people}")
        last_detection_time = current_time

        r = requests.put("https://teknologi-5f750-default-rtdb.firebaseio.com/queueNumber.json", json=average_people)

    # Show the webcam image outside the detection period
    else:
        cv2.imshow('Webcam', img)
        if cv2.waitKey(1) == ord('q'):
            break

# Release resources outside the loop
cap.release()
cv2.destroyAllWindows()


