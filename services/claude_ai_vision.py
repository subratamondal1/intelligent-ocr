import base64
import io
import os

from anthropic import Anthropic
from dotenv import load_dotenv
from PIL import Image

# Load the environment variables from the .env file
load_dotenv()

CLAUDE_KEY = os.getenv(key="CLAUDE_KEY", default="")

# Initialize the Anthropic client
client = Anthropic(api_key=CLAUDE_KEY)


def encode_pil_image(pil_image):
    buffered = io.BytesIO()
    pil_image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")


def compare_and_correct_text(final_processed_image: Image.Image, extracted_text):
    """Compare and correct the extracted text from GPT-4O with the original image using Claude AI"""
    # Encode the PIL image
    base64_image = encode_pil_image(final_processed_image)

    # Prepare the messages for the API call
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": (
                        "I have an original handwritten image and extracted text from it. "
                        "Please compare the extracted text with the original image, find any errors in the extracted text, correct them, "
                        "and provide the final corrected text exactly as it appears in the original image.\n\n"
                        "If the extracted text contains tabular data, represent it as an ASCII table for better readability. "
                        "Otherwise, provide the text as-is without any tabular formatting."
                    ),
                },
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/png",
                        "data": base64_image,
                    },
                },
                {"type": "text", "text": f"Extracted text: {extracted_text}"},
            ],
        }
    ]

    # Make the API call
    response = client.messages.create(
        model="claude-3-sonnet-20240229", max_tokens=1000, messages=messages
    )

    return response.content[0].text
