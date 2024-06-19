from deepface import DeepFace

def compare_faces(image1_path, image2_path):
    # Perform face verification
    result = DeepFace.verify(img1_path=image1_path, img2_path=image2_path)

    # Return the result
    return result["verified"], result

# Example usage
passport_image_path = 'edward_test.jpg'
driving_license_image_path = 'EdMcahon.jpg'

# Check if the photos belong to the same person
is_verified, result = compare_faces(passport_image_path, driving_license_image_path)

print(f"Are the faces the same? {'Yes' if is_verified else 'No'}")
print("Detailed Result:", result)
