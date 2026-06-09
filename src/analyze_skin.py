import cv2
import numpy as np
import mediapipe as mp
from sklearn.cluster import KMeans

mp_face = mp.solutions.face_detection


def analyze_skin(image):
    """Takes a loaded image, returns (undertone, dominant_rgb)."""
    h, w, _ = image.shape
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    with mp_face.FaceDetection(model_selection=1, min_detection_confidence=0.5) as detector:
        results = detector.process(rgb_image)

    if not results.detections:
        return None, None

    # Pick the largest face
    largest = None
    largest_area = 0
    for detection in results.detections:
        box = detection.location_data.relative_bounding_box
        area = box.width * box.height
        if area > largest_area:
            largest_area = area
            largest = box

    x = int(largest.xmin * w)
    y = int(largest.ymin * h)
    box_w = int(largest.width * w)
    box_h = int(largest.height * h)

    # Center patch (cheeks/nose)
    cx = x + box_w // 2
    cy = y + box_h // 2
    patch_half = int(min(box_w, box_h) * 0.2)
    patch = image[cy - patch_half: cy + patch_half,
                  cx - patch_half: cx + patch_half]

    # Dominant color via KMeans
    pixels = patch.reshape(-1, 3)
    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    labels = kmeans.fit_predict(pixels)
    counts = np.bincount(labels)
    dominant_bgr = kmeans.cluster_centers_[np.argmax(counts)]

    b, g, r = int(dominant_bgr[0]), int(dominant_bgr[1]), int(dominant_bgr[2])

    # Undertone
    diff = r - b
    if diff > 35:
        undertone = "Warm"
    elif diff < 15:
        undertone = "Cool"
    else:
        undertone = "Neutral"

    return undertone, (r, g, b)