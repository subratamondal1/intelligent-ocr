import io
import os

from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv
from PIL import Image, ImageDraw, ImageFont

# Load the environment variables from the .env file
load_dotenv()


def azure_vision_ai_ocr(image: Image.Image):
    # Set the values of your computer vision endpoint and computer vision key
    try:
        AZURE_ENDPOINT: str = os.getenv(key="AZURE_ENDPOINT")
        AZURE_KEY = os.getenv(key="AZURE_KEY")
    except NameError:
        print("Missing environment variables 'AZURE_ENDPOINT' or 'AZURE_KEY'")
        print("Set them before running this sample.")
        return None, None

    # Create an Image Analysis client
    client = ImageAnalysisClient(
        endpoint=AZURE_ENDPOINT, credential=AzureKeyCredential(key=AZURE_KEY)
    )

    # # Load image to analyze
    # image_path = "/content/final.jpeg"
    # with open(image_path, "rb") as f:
    #     image_data = f.read()

    image_byte_array = io.BytesIO()
    image.save(image_byte_array, format="JPEG")  # Save in an appropriate format
    image_data = image_byte_array.getvalue()

    # Analyze the image
    result = client.analyze(
        image_data=image_data, visual_features=[VisualFeatures.READ]
    )

    # Open the image for drawing
    # image = Image.open(image_path)
    draw = ImageDraw.Draw(image)

    # Try to load a font, fall back to default if not available
    try:
        font = ImageFont.truetype(font="arialbd.ttf", size=80)
    except IOError:
        font = ImageFont.load_default()

    extracted_text = []

    # Draw bounding boxes and collect text
    if result.read is not None:
        for block in result.read.blocks:
            for line in block.lines:
                # Draw bounding box
                points = [(p.x, p.y) for p in line.bounding_polygon]
                draw.polygon(points, outline="red", width=2)

                # Add text to the list
                extracted_text.append(line.text)

                # Optionally, draw text near the bounding box
                draw.text(
                    (points[0][0], points[0][1] - 20), line.text, fill="red", font=font
                )

    return image, extracted_text
