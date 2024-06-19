from deepface import DeepFace
import cv2
from PIL import Image
import imagehash

def verify_faces(image1_path, image2_path):
    # Perform face verification
    result = DeepFace.verify(img1_path=image1_path, img2_path=image2_path)
    
    # Print the detailed result
    print("Face Verification Result:", result)
    
    # Check for image tampering in both images using image hashing
    tampering_detected_1 = detect_image_tampering(image1_path)
    tampering_detected_2 = detect_image_tampering(image2_path)
    
    # Return combined tampering detection result
    return result['verified'], tampering_detected_1, tampering_detected_2

def detect_image_tampering(image_path):
    # Load image
    image = Image.open(image_path)
    
    # Compute image hash
    image_hash = imagehash.average_hash(image)
    
    # Define thresholds for hamming distance (adjust as needed)
    threshold = 5
    
    # Check tampering by comparing with itself (should be identical)
    tampering_detected = False
    if image_hash != imagehash.average_hash(image):
        tampering_detected = True
    
    return tampering_detected

# Example usage
image1_path = 'ed_licence.jpg'
image2_path = 'Balaji.jpg'

# Verify faces and detect tampering in both images
faces_verified, tampering_detected_1, tampering_detected_2 = verify_faces(image1_path, image2_path)

# Interpret the results
if faces_verified and not tampering_detected_1 and not tampering_detected_2:
    print("The faces belong to the same person and no tampering detected in either image.")
elif faces_verified and (tampering_detected_1 or tampering_detected_2):
    print("The faces belong to the same person, but tampering detected in one or both images.")
else:
    print("The faces do not belong to the same person or both images are tampered.")
