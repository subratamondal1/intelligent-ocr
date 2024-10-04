from collections import Counter

import cv2
import numpy as np
from PIL import Image
from sklearn.cluster import KMeans

from services.remove_horizontal_lines import remove_horizontal_lines

# Load Image
original_image: Image.Image = Image.open(
    "data/raw images/01 table image with margin 1.jpeg"
)

original_image.show()


def detect_line_color(image_pil, n_clusters=3):
    # Convert PIL image to OpenCV format
    image_cv = cv2.cvtColor(np.array(image_pil), cv2.COLOR_RGB2BGR)

    # Convert to grayscale to detect lines
    gray_image = cv2.cvtColor(image_cv, cv2.COLOR_BGR2GRAY)

    # Use edge detection to detect horizontal lines
    edges = cv2.Canny(gray_image, 50, 150, apertureSize=3)

    # Find contours which can represent the lines
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Extract the line pixels from the original image
    line_pixels = []
    for contour in contours:
        for point in contour:
            x, y = point[0]
            line_pixels.append(image_cv[y, x])

    # If no line pixels detected, return None
    if not line_pixels:
        return None

    # Cluster colors using KMeans to find dominant colors in the lines
    kmeans = KMeans(n_clusters=n_clusters, random_state=0)
    kmeans.fit(line_pixels)
    colors = kmeans.cluster_centers_.astype(int)

    # Count frequency of each color
    counts = Counter(kmeans.labels_)

    # Identify the most frequent color (dominant)
    dominant_color = colors[np.argmax(list(counts.values()))]

    # Convert BGR to RGB
    dominant_color_rgb = dominant_color[::-1]

    # Convert RGB to Hex
    hex_color = "#{:02x}{:02x}{:02x}".format(*dominant_color_rgb)

    return hex_color


def detect_handwritten_text_color(image_pil, n_clusters=3):
    # Convert PIL image to OpenCV format
    image_cv = cv2.cvtColor(np.array(image_pil), cv2.COLOR_RGB2BGR)

    # Convert to grayscale to detect handwritten text
    gray_image = cv2.cvtColor(image_cv, cv2.COLOR_BGR2GRAY)

    # Use adaptive thresholding to extract potential handwritten text pixels
    # We invert the image, so text pixels become white (255) and background becomes black (0)
    _, binary_image = cv2.threshold(
        gray_image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
    )

    # Extract pixels corresponding to potential handwritten text
    text_pixels = image_cv[binary_image > 0]

    # If no text pixels detected, return None
    if text_pixels.size == 0:
        return None

    # Filter text pixels by brightness to avoid noise
    # Only consider dark pixels, as these are likely to be part of the text
    # You can adjust the threshold value if needed
    brightness_threshold = 60
    dark_pixels_mask = gray_image[binary_image > 0] < brightness_threshold
    dark_text_pixels = text_pixels[dark_pixels_mask]

    # If filtered pixels are empty, use the original text_pixels
    if dark_text_pixels.size > 0:
        text_pixels = dark_text_pixels

    # Cluster colors using KMeans to find the main color in the text pixels
    kmeans = KMeans(n_clusters=n_clusters, random_state=0)
    kmeans.fit(text_pixels)
    colors = kmeans.cluster_centers_.astype(int)

    # Count frequency of each color
    counts = Counter(kmeans.labels_)

    # Identify the most frequent color (dominant text color)
    dominant_color = colors[np.argmax(list(counts.values()))]

    # Convert BGR to RGB
    dominant_color_rgb = dominant_color[::-1]

    # Map color to general categories
    def categorize_color(rgb):
        r, g, b = rgb
        # Define basic color categories based on RGB values
        if max(r, g, b) - min(r, g, b) < 20:  # If the color is almost grey
            return "black"
        elif b > r and b > g:
            return "blue"
        elif g > r and g > b:
            return "green"
        elif r > g and r > b:
            return "red"
        elif r > 200 and g > 200 and b < 150:
            return "yellow"
        else:
            return "unknown"

    # Categorize the detected color
    detected_color_name = categorize_color(dominant_color_rgb)

    return detected_color_name


# Example usage
detected_color_name = detect_handwritten_text_color(image_pil=original_image)
print(f"Detected handwritten text color: {detected_color_name}")


modified_image = remove_horizontal_lines(
    pil_image=original_image, preserve_color=detected_color_name
)
modified_image.show()