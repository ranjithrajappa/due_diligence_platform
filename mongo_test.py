from pymongo import MongoClient
from PIL import Image
import io
import base64

# Function to encode an image to base64
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    return encoded_string

# Function to decode base64 to an image and save it
def decode_image(encoded_string, output_path):
    image_data = base64.b64decode(encoded_string)
    with open(output_path, "wb") as image_file:
        image_file.write(image_data)

# Create a MongoClient to the running mongod instance
client = MongoClient('mongodb://localhost:27017/')

# Access a specific database
db = client['myDatabase']

# Access a specific collection
collection = db['myCollection']

# Example image path
image_path = 'Balaji.jpg'  # Replace with your image path
encoded_image = encode_image(image_path)

# Insert a document with the image into the collection
document = {
    "name": "Maddy",
    "age": 30,
    "address": "123 Main St",
    "image": encoded_image
}
result = collection.insert_one(document)

print(f"Inserted document with _id: {result.inserted_id}")

# Fetch the inserted document using the unique _id
fetched_document = collection.find_one({"_id": result.inserted_id})
print(f"Fetched document: {fetched_document}")

# Decode and save the fetched image
if fetched_document and "image" in fetched_document:
    decode_image(fetched_document["image"], 'retrieved_image.jpg')
    print("Image retrieved and saved as 'retrieved_image.jpg'")
else:
    print("No image found in the document.")
