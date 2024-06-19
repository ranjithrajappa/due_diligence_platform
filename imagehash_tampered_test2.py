from PIL import Image
import imagehash

def detect_tampering_with_hashes(image_path):
    try:
        # Load image
        image = Image.open(image_path)
        
        # Convert image to grayscale
        gray_image = image.convert('L')
        
        # Define regions of interest (ROIs) for comparison
        # Example: Split the image into four quadrants
        width, height = image.size
        roi1 = gray_image.crop((0, 0, width//2, height//2))
        roi2 = gray_image.crop((width//2, 0, width, height//2))
        roi3 = gray_image.crop((0, height//2, width//2, height))
        roi4 = gray_image.crop((width//2, height//2, width, height))
        
        # Compute perceptual hashes for each ROI
        hash1 = imagehash.average_hash(roi1)
        hash2 = imagehash.average_hash(roi2)
        hash3 = imagehash.average_hash(roi3)
        hash4 = imagehash.average_hash(roi4)
        
        # Compare hashes (Hamming distance)
        threshold = 5  # Adjust as needed
        if (hash1 - hash2) > threshold or (hash1 - hash3) > threshold or (hash1 - hash4) > threshold \
            or (hash2 - hash3) > threshold or (hash2 - hash4) > threshold or (hash3 - hash4) > threshold:
            tampering_detected = True
        else:
            tampering_detected = False
        
        return tampering_detected
    
    except Exception as e:
        print(f"Error processing image: {e}")
        return False

# Example usage
image_path = 'ed_pass.jpg'

tampering_detected = detect_tampering_with_hashes(image_path)

if tampering_detected:
    print("Tampering detected within the image.")
else:
    print("No tampering detected within the image.")
