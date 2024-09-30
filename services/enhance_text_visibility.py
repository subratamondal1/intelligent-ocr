import cv2
import numpy as np
from PIL import Image, ImageEnhance


def enhance_text_visibility(pil_image: Image.Image) -> Image.Image:
    """
    Enhances the visibility of text in an image.

    Args:
        pil_image: A PIL Image object.

    Returns:
        A PIL Image object with enhanced text visibility.
    """
    # Enhance the contrast
    pil_image = ImageEnhance.Contrast(pil_image).enhance(1.5)  # Increase contrast

    # Enhance the color saturation
    pil_image = ImageEnhance.Color(pil_image).enhance(1.5)  # Increase saturation

    # Convert back to OpenCV format
    enhanced_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

    # Optional: Apply mild denoising to reduce any remaining noise
    denoised_image = cv2.fastNlMeansDenoisingColored(
        enhanced_image, None, 10, 10, 7, 21
    )

    # Convert the denoised image back to a PIL Image object for final processing
    final_pil_image = Image.fromarray(denoised_image)

    # Convert the image to grayscale
    grayscale_image = final_pil_image.convert("L")

    # Adjust the brightness of the grayscale image
    brightened_image: Image.Image = ImageEnhance.Brightness(grayscale_image).enhance(
        1.2
    )

    return brightened_image
