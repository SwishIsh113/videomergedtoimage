import cv2
import os

def mergeImages(inputFolder, outputImage):
    imageFiles = [f for f in os.listdir(inputFolder) if os.path.isfile(os.path.join(inputFolder, f))]
    imageFiles = [f for f in imageFiles if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    if len(imageFiles) == 0:
        print("No images found in the input folder.")
        return

    images = []
    for imageFile in imageFiles:
        image = cv2.imread(os.path.join(inputFolder, imageFile))
        images.append(image)

    if len(images) == 0:
        print("No valid images found in the input folder.")
        return

    # Ensure all images have the same dimensions
    image_height, image_width, _ = images[0].shape
    for i in range(1, len(images)):
        if images[i].shape[:2] != (image_height, image_width):
            images[i] = cv2.resize(images[i], (image_width, image_height))

    # Merge the images by layering them on top of each other with equal transparency
    mergedImage = images[0].astype(float)
    alpha = 1.0 / len(images)  # Equal transparency for all images
    for i in range(1, len(images)):
        mergedImage = cv2.addWeighted(mergedImage, 1-alpha, images[i].astype(float), alpha, 0)

    mergedImage = mergedImage.astype('uint8')

    # Save the merged image
    cv2.imwrite(outputImage, mergedImage)
    print("Merged image saved successfully.")

if __name__ == "__main__":
    parentFolder = "frames"
    outputFolder = "merged_images"

    # Create the output folder if it doesn't exist
    os.makedirs(outputFolder, exist_ok=True)

    # Iterate over subfolders in the parent folder
    for folderName in os.listdir(parentFolder):
        inputFolder = os.path.join(parentFolder, folderName)
        if os.path.isdir(inputFolder):
            outputImage = os.path.join(outputFolder, folderName + ".png")
            mergeImages(inputFolder, outputImage)
