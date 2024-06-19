from deepface import DeepFace
from PIL import Image
from io import BytesIO
from pymongo import MongoClient
from bson import Binary
import numpy as np

# Function to connect to MongoDB
def connect_to_mongodb():
    client = MongoClient('localhost', 27017)
    db = client['face_recognition']
    collection = db['id_photos']
    return collection

# Function to extract photo from ID image using DeepFace and store in MongoDB
def extract_photo_and_store(id_image_path, collection):
    # Load the ID image as a PIL image
    id_image = Image.open(id_image_path)

    # Use DeepFace to extract and align faces
    extracted_faces = DeepFace.extract_faces(img_path=id_image_path, detector_backend='opencv', enforce_detection=False)

    # Check if any faces were detected
    if len(extracted_faces) == 0:
        raise ValueError("No face detected in the provided image.")

    # Assuming only one face is extracted, take the first one
    detected_face = extracted_faces[0]

    # Extract the aligned face image from the dictionary returned by extract_faces
    detected_face_img = detected_face['image']

    # Convert aligned face to PIL image
    detected_face_pil = Image.fromarray(detected_face_img)

    # Convert PIL image to binary format to store in MongoDB
    img_byte_arr = BytesIO()
    detected_face_pil.save(img_byte_arr, format='JPEG')
    img_byte_arr = img_byte_arr.getvalue()

    # Extract facial embeddings (vector representation)
    embeddings = DeepFace.represent(detected_face_pil, model_name='Facenet')

    # Convert embeddings (numpy array) to binary format
    embeddings_binary = Binary(embeddings.tostring())

    # Insert the photo and embeddings into MongoDB
    photo_data = {'photo': Binary(img_byte_arr), 'embeddings': embeddings_binary}
    insert_result = collection.insert_one(photo_data)
    photo_id = insert_result.inserted_id

    print(f'Inserted photo with ID: {photo_id}')

    return photo_id

if __name__ == "__main__":
    # Connect to MongoDB
    collection = connect_to_mongodb()

    # Example ID image path (update with your own path)
    id_image_path = 'path_to_your_id_image.jpg'

    try:
        # Extract photo from ID image and store in MongoDB
        photo_id = extract_photo_and_store(id_image_path, collection)
        print(f'Photo with ID {photo_id} stored in MongoDB')

    except ValueError as ve:
        print(f'Error: {ve}')
