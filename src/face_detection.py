import cv2
import os
import mediapipe as mp

# Build the image path
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
image_path = os.path.join(project_root, "data", "test.jpg")

# Load the image
image = cv2.imread(image_path)
h, w, _ = image.shape

# Set up MediaPipe face detection
mp_face = mp.solutions.face_detection
rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

with mp_face.FaceDetection(model_selection=1, min_detection_confidence=0.5) as detector:
    results = detector.process(rgb_image)

if not results.detections:
    print("No face detected.")
else:
    print(f"Found {len(results.detections)} face(s). Selecting the largest.")

    # Find the detection with the largest box area
    largest = None
    largest_area = 0

    for detection in results.detections:
        box = detection.location_data.relative_bounding_box
        # Area in relative units (width * height) — enough for comparison
        area = box.width * box.height
        if area > largest_area:
            largest_area = area
            largest = box

    # Convert the largest box to pixel coordinates
    x = int(largest.xmin * w)
    y = int(largest.ymin * h)
    box_w = int(largest.width * w)
    box_h = int(largest.height * h)

    # Draw the box only on the primary face
    cv2.rectangle(image, (x, y), (x + box_w, y + box_h), (0, 255, 0), 2)

    print(f"Primary face box: x={x}, y={y}, w={box_w}, h={box_h}")

    cv2.imshow("Primary Face", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()