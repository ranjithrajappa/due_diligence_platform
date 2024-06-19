from deepface import DeepFace
from PIL import Image, ImageChops, ImageEnhance
import numpy as np
import matplotlib.pyplot as plt
import cv2
import io
import base64
from pymongo import MongoClient
import gridfs

# Function to detect face and return it as a PIL Image object
def detect_face(image_path):
    # Detect face using DeepFace
    detected_faces = DeepFace.extract_faces(image_path, detector_backend='opencv', enforce_detection=False)
    
    if detected_faces:
        # Get the first detected face
        face_image_array = detected_faces[0]['face']
        # Convert face image array to PIL Image
        face_image_pil = Image.fromarray((face_image_array * 255).astype(np.uint8))
        return face_image_pil
    else:
        raise ValueError("No face detected in the image")

# Function to compute Error Level Analysis (ELA) on an image
def compute_ela(image, output_path='ela_face.jpg', quality=90):
    # Save the image at a lower quality to perform ELA
    image.save(output_path, 'JPEG', quality=quality)
    
    # Re-open the saved lower quality image for ELA
    ela_image = Image.open(output_path)
    
    # Compute the absolute difference between the original and the ELA image
    ela_diff = ImageChops.difference(image, ela_image)
    
    # Enhance the difference image to make it more visible
    extrema = ela_diff.getextrema()
    max_diff = max([ex[1] for ex in extrema])
    scale = 255.0 / max_diff if max_diff != 0 else 1
    ela_diff = ela_diff.point(lambda x: x * scale)
    
    ela_diff = np.array(ela_diff.convert('L'))
    
    return ela_diff

# Function to detect edges using Canny edge detection
def detect_edges(image):
    # Convert to grayscale
    gray_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
    
    # Apply Canny edge detection
    edges = cv2.Canny(gray_image, threshold1=100, threshold2=200)
    
    return edges

# Function to store image and face in MongoDB
def store_in_mongodb(original_image, face_image, name, age, gender):
    # Convert images to base64 strings
    original_image_base64 = pil_image_to_base64(original_image)
    face_image_base64 = pil_image_to_base64(face_image)

    # Prepare data to store in MongoDB
    data = {
        "name": name,
        "age": age,
        "gender": gender,
        "original_image": original_image_base64,
        "face_image": face_image_base64
    }

    # Connect to MongoDB
    client = MongoClient("mongodb://localhost:27017/")
    db = client["face_database"]
    fs = gridfs.GridFS(db)

    # Store data in MongoDB
    collection = db["faces"]
    collection.insert_one(data)
    print("Data stored in MongoDB.")

# Function to convert PIL image to base64 string
def pil_image_to_base64(img):
    buffered = io.BytesIO()
    img.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str

# Example usage
def main():
    image_path = 'Balaji.jpg'  # Replace with your image path
    name = input("Enter name: ")
    age = int(input("Enter age: "))
    gender = input("Enter gender: ")

    try:
        # Detect face in the image
        face_image = detect_face(image_path)
        
        # Save face image as a separate .jpg file
        face_image.save('face_Balaji.jpg')

        # Compute ELA on the detected face region (optional)
        # ela_diff = compute_ela(face_image)

        # Compute edges on the detected face region (optional)
        # edges = detect_edges(face_image)

        # Display or further process ELA and edges if needed

        print("Process completed successfully.")
    except ValueError as ve:
        print(ve)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
