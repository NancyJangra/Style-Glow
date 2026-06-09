import cv2
import numpy as np
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

from analyze_skin import analyze_skin
from analyze_body import analyze_body
from recommender import recommend

app = FastAPI()

# Allow the frontend (running on a different address) to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # we'll tighten this before deploying
    allow_methods=["*"],
    allow_headers=["*"],
)


def read_image(upload_bytes):
    """Convert uploaded file bytes into an OpenCV image."""
    arr = np.frombuffer(upload_bytes, np.uint8)
    image = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    return image


@app.get("/")
def home():
    return {"status": "Dress Recommender API is running"}


@app.post("/analyze")
async def analyze(face: UploadFile = File(...), body: UploadFile = File(...)):
    # Read both uploaded images
    face_image = read_image(await face.read())
    body_image = read_image(await body.read())

    if face_image is None or body_image is None:
        return {"error": "Could not read one or both images."}

    # Run analysis
    undertone, rgb = analyze_skin(face_image)
    body_shape, ratio = analyze_body(body_image)

    if undertone is None:
        return {"error": "No face detected in the face photo."}
    if body_shape is None:
        return {"error": "No body detected in the body photo."}

    # Get recommendations
    colors, cuts, makeup = recommend(undertone, body_shape)

    # Return everything as JSON
    return {
        "undertone": undertone,
        "rgb": rgb,
        "body_shape": body_shape,
        "ratio": round(ratio, 2),
        "colors": colors,
        "cuts": cuts,
        "undertone": undertone,
        "rgb": rgb,
        "body_shape": body_shape,
        "ratio": round(ratio, 2),
        "colors": colors,
        "cuts": cuts,
        "makeup": makeup,
    }
    