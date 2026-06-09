import cv2
import math
import mediapipe as mp

mp_pose = mp.solutions.pose


def analyze_body(image):
    """Takes a loaded image, returns (body_shape, ratio)."""
    h, w, _ = image.shape
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    with mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.5) as pose:
        results = pose.process(rgb_image)

    if not results.pose_landmarks:
        return None, None

    lm = results.pose_landmarks.landmark

    # Landmark indices
    L_SHOULDER, R_SHOULDER = 11, 12
    L_HIP, R_HIP = 23, 24

    def to_px(landmark):
        return (landmark.x * w, landmark.y * h)

    def distance(p1, p2):
        return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

    shoulder_width = distance(to_px(lm[L_SHOULDER]), to_px(lm[R_SHOULDER]))
    hip_width = distance(to_px(lm[L_HIP]), to_px(lm[R_HIP]))

    # Guard against division by zero
    if hip_width == 0:
        return None, None

    ratio = shoulder_width / hip_width

    if ratio > 1.15:
        body_shape = "Inverted Triangle"
    elif ratio < 0.85:
        body_shape = "Pear / Triangle"
    else:
        body_shape = "Rectangle"

    return body_shape, ratio