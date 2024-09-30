import io
import os

from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont

# Load the environment variables from the .env file
load_dotenv()


def synthesize_image_from_ocr(ocr_results, pil_image):
    # Use the PIL image object to get its size
    width, height = pil_image.size

    # Create a new white image with the same size as the original
    image = Image.new("RGB", (width, height), color="white")

    # Load a clearer font
    font_families = ["DejaVuSans.ttf", "LiberationSans-Regular.ttf", "Arial.ttf"]
    font = None
    for family in font_families:
        try:
            font = ImageFont.truetype(
                family, 60
            )  # Using a clearer font and adjusting size
            break
        except IOError:
            continue  # Try the next font
    if font is None:
        font = ImageFont.load_default()  # Fall back to default font

    if ocr_results.read is not None:
        for block in ocr_results.read.blocks:
            for line in block.lines:
                # Get text and bounding box
                text = line.text
                box = line.bounding_polygon

                # Convert bounding box to list of tuples
                points = [(p.x, p.y) for p in box]

                # Calculate text position (top-left corner of bounding box)
                text_x, text_y = points[0]

                # Create a temporary image for this text with higher resolution
                temp_img = Image.new(
                    "RGBA", (width * 2, height * 2), (255, 255, 255, 0)
                )
                temp_draw = ImageDraw.Draw(temp_img)

                # Draw text on the temporary image with anti-aliasing
                temp_draw.text(
                    (text_x * 2, text_y * 2), text, fill=(0, 0, 0, 255), font=font
                )

                # Resize the temporary image back to original size and paste it onto the main image
                temp_img = temp_img.resize((width, height), Image.LANCZOS)
                image.paste(temp_img, (0, 0), temp_img)

    return image


def synthesize_azure_ai_ocr(image: Image.Image):
    # Set the values of your computer vision endpoint and computer vision key
    try:
        AZURE_ENDPOINT: str = os.getenv(key="AZURE_ENDPOINT", default="")
        AZURE_KEY = os.getenv(key="AZURE_KEY", default="")
    except NameError:
        print("Missing environment variables 'AZURE_ENDPOINT' or 'AZURE_KEY'")
        print("Set them before running this sample.")
        return None, None

    # Create an Image Analysis client
    client = ImageAnalysisClient(
        endpoint=AZURE_ENDPOINT, credential=AzureKeyCredential(key=AZURE_KEY)
    )

    # Convert the PIL image to byte data
    image_byte_array = io.BytesIO()
    image.save(image_byte_array, format="JPEG")  # Save in an appropriate format
    image_data = image_byte_array.getvalue()

    # Analyze the image
    result = client.analyze(
        image_data=image_data, visual_features=[VisualFeatures.READ]
    )

    # Synthesize new image from OCR results
    synthesized_image = synthesize_image_from_ocr(result, image)

    extracted_text = []

    # Collect extracted text
    if result.read is not None:
        for block in result.read.blocks:
            for line in block.lines:
                extracted_text.append(line.text)

    return synthesized_image, extracted_text
