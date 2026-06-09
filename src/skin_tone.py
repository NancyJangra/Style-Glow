import cv2
import os
import mediapipe as mp

# Build the image path
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
image_path = os.path.join(project_root, "data", "test.jpg")

image = cv2.imread(image_path)
h, w, _ = image.shape

# --- Detect the primary face (same logic as before) ---
mp_face = mp.solutions.face_detection
rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

with mp_face.FaceDetection(model_selection=1, min_detection_confidence=0.5) as detector:
    results = detector.process(rgb_image)

if not results.detections:
    print("No face detected.")
    exit()

# Pick the largest face
largest = None
largest_area = 0
for detection in results.detections:
    box = detection.location_data.relative_bounding_box
    area = box.width * box.height
    if area > largest_area:
        largest_area = area
        largest = box

# Convert to pixel coordinates
x = int(largest.xmin * w)
y = int(largest.ymin * h)
box_w = int(largest.width * w)
box_h = int(largest.height * h)

# --- Take a center patch of the face box ---
# We grab the middle 40% of the box (cheeks/nose) to avoid eyes, brows, hair
cx = x + box_w // 2          # center x
cy = y + box_h // 2          # center y
patch_half = int(min(box_w, box_h) * 0.2)  # 20% each side = 40% total

patch = image[cy - patch_half : cy + patch_half,
              cx - patch_half : cx + patch_half]

print("Patch shape:", patch.shape)

import numpy as np
from sklearn.cluster import KMeans

# Reshape patch from (height, width, 3) into a flat list of pixels (N, 3)
pixels = patch.reshape(-1, 3)

# Cluster the pixels into 3 color groups
k = 3
kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
labels = kmeans.fit_predict(pixels)

# Find which cluster has the most pixels (the dominant color)
counts = np.bincount(labels)
dominant_cluster = np.argmax(counts)
dominant_color_bgr = kmeans.cluster_centers_[dominant_cluster]

# OpenCV is BGR — convert to RGB for readability
b, g, r = dominant_color_bgr
print(f"Dominant skin color (RGB): ({int(r)}, {int(g)}, {int(b)})")

# --- Classify undertone from the dominant RGB ---
# r, g, b were already extracted above
r_val = int(r)
g_val = int(g)
b_val = int(b)

# Difference between red and blue tells us warm vs cool
diff = r_val - b_val

if diff > 35:
    undertone = "Warm"
elif diff < 15:
    undertone = "Cool"
else:
    undertone = "Neutral"

print(f"R-B difference: {diff}")
print(f"Undertone: {undertone}")