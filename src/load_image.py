import cv2
import os

# Build a path to data/test.jpg relative to the project, not the terminal
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
image_path = os.path.join(project_root, "data", "test.jpg")

# Load the image
image = cv2.imread(image_path)

# Safety check — did it actually load?
if image is None:
    print("Image not found. Check the path and filename.")
else:
    print("Image loaded! Shape:", image.shape)
    cv2.imshow("Test Image", image)
    cv2.waitKey(0)          # wait until you press a key
    cv2.destroyAllWindows() # close the window