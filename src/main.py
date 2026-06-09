import cv2
import os
from analyze_skin import analyze_skin
from analyze_body import analyze_body
from recommender import recommend

# Build image paths
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)

face_image_path = os.path.join(project_root, "data", "test.jpg")
body_image_path = os.path.join(project_root, "data", "body.jpg")

# --- Load images ---
face_image = cv2.imread(face_image_path)
body_image = cv2.imread(body_image_path)

if face_image is None or body_image is None:
    print("Could not load images. Check data/test.jpg and data/body.jpg")
    exit()

# --- Run analysis ---
print("Analyzing skin tone...")
undertone, rgb = analyze_skin(face_image)

print("Analyzing body shape...")
body_shape, ratio = analyze_body(body_image)

# --- Handle failures ---
if undertone is None:
    print("No face detected — cannot determine undertone.")
    exit()
if body_shape is None:
    print("No body detected — cannot determine body shape.")
    exit()

# --- Get recommendations ---
colors, cuts = recommend(undertone, body_shape)

# --- Print the final report ---
print("\n" + "=" * 45)
print("        YOUR STYLE RECOMMENDATIONS")
print("=" * 45)
print(f"\nSkin RGB           : {rgb}")
print(f"Detected undertone : {undertone}")
print(f"Detected body shape: {body_shape} (ratio {ratio:.2f})")

print(f"\n--- Colors that suit you ({undertone}) ---")
for item in colors:
    print(f"  • {item}")

print(f"\n--- Cuts & silhouettes for you ({body_shape}) ---")
for item in cuts:
    print(f"  • {item}")

print("\n" + "=" * 45)