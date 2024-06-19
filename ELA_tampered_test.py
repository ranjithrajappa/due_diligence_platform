from deepface import DeepFace
from PIL import Image, ImageChops, ImageEnhance
import numpy as np
import matplotlib.pyplot as plt
import cv2

def detect_face(image_path):
    # Detect face using DeepFace
    detected_faces = DeepFace.extract_faces(image_path, detector_backend='opencv', enforce_detection=False)
    
    if detected_faces:
        # Get the first detected face
        face_image_array = detected_faces[0]['face']
        return face_image_array
    else:
        raise ValueError("No face detected in the image")

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

def detect_edges(image):
    # Convert to grayscale
    gray_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
    
    # Apply Canny edge detection
    edges = cv2.Canny(gray_image, threshold1=100, threshold2=200)
    
    return edges

def detect_tampering(image_path, ela_threshold=100, edge_threshold=1000):
    # Detect face in the image
    face_image_array = detect_face(image_path)
    
    # Convert the detected face array back to a PIL image
    face_image = Image.fromarray((face_image_array * 255).astype(np.uint8))
    
    # Compute ELA on the detected face region
    ela_diff = compute_ela(face_image)
    
    # Compute edges on the detected face region
    edges = detect_edges(face_image)
    
    # Visualize ELA difference and edges
    plt.subplot(1, 2, 1)
    plt.imshow(ela_diff, cmap='gray')
    plt.title('Error Level Analysis (ELA) on Detected Face')
    plt.axis('off')
    
    plt.subplot(1, 2, 2)
    plt.imshow(edges, cmap='gray')
    plt.title('Edge Detection on Detected Face')
    plt.axis('off')
    
    plt.show()
    
    # Check if ELA difference or edge count exceeds threshold
    ela_tampering_detected = np.max(ela_diff) > ela_threshold
    edge_tampering_detected = np.sum(edges) > edge_threshold
    
    return not (ela_tampering_detected or edge_tampering_detected)

# Example usage
image_path = 'ed_licence.jpg'
is_original = detect_tampering(image_path)

if is_original:
    print("Original image detected.")
else:
    print("Edited image detected.")
