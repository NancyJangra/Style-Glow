import cv2
import os
import math
import mediapipe as mp

# Build the image path
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
image_path = os.path.join(project_root, "data", "body.jpg")

image = cv2.imread(image_path)

# Set up MediaPipe Pose
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

with mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.5) as pose:
    results = pose.process(rgb_image)

if not results.pose_landmarks:
    print("No body detected.")
else:
    print("Body detected! Drawing landmarks.")

    # Draw all 33 landmarks and the connections
    mp_drawing.draw_landmarks(
        image,
        results.pose_landmarks,
        mp_pose.POSE_CONNECTIONS
    )

    h, w, _ = image.shape
    lm = results.pose_landmarks.landmark

    # Landmark indices
    L_SHOULDER, R_SHOULDER = 11, 12
    L_HIP, R_HIP = 23, 24

    # Convert normalized landmark coords (0-1) to pixels
    def to_px(landmark):
        return (landmark.x * w, landmark.y * h)

    ls = to_px(lm[L_SHOULDER])
    rs = to_px(lm[R_SHOULDER])
    lh = to_px(lm[L_HIP])
    rh = to_px(lm[R_HIP])

    # Euclidean distance between two points
    def distance(p1, p2):
        return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

    shoulder_width = distance(ls, rs)
    hip_width = distance(lh, rh)

    print(f"Shoulder width (px): {shoulder_width:.1f}")
    print(f"Hip width (px): {hip_width:.1f}")
    print(f"Shoulder/Hip ratio: {shoulder_width / hip_width:.2f}")
    # --- Classify body shape from the ratio ---
    ratio = shoulder_width / hip_width

    if ratio > 1.15:
        body_shape = "Inverted Triangle"
    elif ratio < 0.85:
        body_shape = "Pear / Triangle"
    else:
        body_shape = "Rectangle"

    print(f"Body shape: {body_shape}")

    cv2.imshow("Body Landmarks", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()