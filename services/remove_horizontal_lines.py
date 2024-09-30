import cv2
import numpy as np
from PIL import Image


def remove_horizontal_lines(image_path, preserve_color) -> Image.Image:
    """
    Removes horizontal lines from the image and returns a PIL Image object.

    Parameters
    ----------
    image_path : str
        Path to the image
    preserve_color : str
        Color to preserve in the image. Options are "blue", "red", "black", or "green".

    Returns
    -------
    pil_image : PIL Image
        Image after removing horizontal lines.
    """
    # Read the image
    img = cv2.imread(image_path)

    # Convert the image to HSV color space
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Define color ranges in HSV
    color_ranges = {
        "blue": (np.array([90, 30, 30]), np.array([140, 255, 255])),
        "green": (np.array([35, 30, 30]), np.array([85, 255, 255])),
        "black": (np.array([0, 0, 0]), np.array([180, 255, 30])),
        "red1": (np.array([0, 30, 30]), np.array([10, 255, 255])),
        "red2": (np.array([170, 30, 30]), np.array([180, 255, 255])),
    }

    if preserve_color not in color_ranges:
        raise ValueError("Invalid color. Choose 'blue', 'green', 'black', or 'red'.")

    # Create a mask to isolate the specified color
    if preserve_color == "red":
        mask1 = cv2.inRange(hsv, color_ranges["red1"][0], color_ranges["red1"][1])
        mask2 = cv2.inRange(hsv, color_ranges["red2"][0], color_ranges["red2"][1])
        mask = cv2.bitwise_or(mask1, mask2)
    else:
        lower_color, upper_color = color_ranges[preserve_color]
        mask = cv2.inRange(hsv, lower_color, upper_color)

    # Dilate the mask to include nearby pixels
    kernel = np.ones((3, 3), np.uint8)
    mask = cv2.dilate(mask, kernel, iterations=1)

    # Create a white background
    white_bg = np.ones_like(img) * 255

    # Put the preserved color on the white background
    result = white_bg.copy()
    result[mask > 0] = img[mask > 0]

    # Enhance the preserved color
    for i in range(3):  # for each color channel
        channel = result[:, :, i]
        channel[mask > 0] = np.clip(channel[mask > 0] * 1.2, 0, 255)
        result[:, :, i] = channel

    # Convert from BGR to RGB
    result_rgb = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)

    convert_to_pil_image = Image.fromarray(result_rgb)
    return convert_to_pil_image


removed_horizontal_lines = remove_horizontal_lines(
    image_path="data/raw images/01 table image with margin 1.jpeg",
    preserve_color="blue",
)

if __name__ == "__main__":
    removed_horizontal_lines.show(title="Removed Horizontal Lines")
