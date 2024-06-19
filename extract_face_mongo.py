from deepface import DeepFace
from PIL import Image, ImageChops
import numpy as np
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

    # Connect to MongoDB and insert data
    try:
        client = MongoClient("mongodb://localhost:27017/")
        db = client["face_database"]
        collection = db["faces"]
        
        # Insert data into MongoDB
        collection.insert_one(data)
        print("Data stored in MongoDB.")
    except Exception as e:
        print(f"Error storing data in MongoDB: {e}")
    finally:
        client.close()  # Close MongoDB connection

# Function to convert PIL image to base64 string
def pil_image_to_base64(img):
    buffered = io.BytesIO()
    img.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str

# Example usage
def main():
    image_path = r'test_images\Balaji.jpg'  # Replace with your image path
    name = input("Enter name: ")
    age = int(input("Enter age: "))
    gender = input("Enter gender: ")

    try:
        # Detect face in the image
        face_image = detect_face(image_path)
        
        # Save face image as a separate .jpg file
        face_image.save('face_extracted.jpg')  

        # Store original image and face image in MongoDB
        original_image = Image.open(image_path)
        store_in_mongodb(original_image, face_image, name, age, gender)

        print("Process completed successfully.")
    except ValueError as ve:
        print(ve)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
