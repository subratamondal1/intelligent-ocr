import base64
import io
import os

from dotenv import load_dotenv
from openai import OpenAI
from PIL import Image

# Load the environment variables from the .env file
load_dotenv()


OPENAI_KEY: str = os.getenv(key="OPENAI_KEY", default="")
client = OpenAI(api_key=OPENAI_KEY)


def encode_pil_image(pil_image) -> str:
    """Encodes images for sending to OpenAI"""
    buffered = io.BytesIO()
    pil_image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")


def compare_images(final_processed_image: Image.Image, synthesized_image: Image.Image):
    """Compare final processed image with synthesized image using GPT-4o"""
    # Encode both images
    original_base64 = encode_pil_image(final_processed_image)
    extracted_base64 = encode_pil_image(synthesized_image)

    # Prepare the messages for the API call
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": """
                    Task: Perform high-precision text extraction from handwritten images.

                    Input: Two images are provided:
                    1. Original: A handwritten document.
                    2. Synthesized: A digital recreation of the handwritten document.

                    Context: The synthesized image is a close representation of the original, created using OCR technology. While it offers improved readability, it may contain errors.

                    Primary Objective: Extract the text from the original handwritten image with 100% accuracy.

                    Guidelines:
                    1. Prioritize the original handwritten image as the primary source of information.
                    2. Use the synthesized image as a reference to aid in deciphering unclear handwriting.
                    3. Pay meticulous attention to all characters, including special symbols, punctuation, and formatting.
                    4. For numerical data, cross-reference both images to ensure accuracy.
                    5. Preserve the exact formatting, capitalization, and spacing as presented in the original image.
                    6. If discrepancies exist between the two images, default to the original handwritten version.
                    
                    Special Instructions for Tables:
                    - If any tabular data is detected, represent it using ASCII characters (e.g., |, -, +) to create a visually accurate table that mirrors the structure of the original handwritten image.
                    - Maintain the alignment of columns and rows to ensure the table's readability and accuracy.
                    - If the content is not tabular, output the text in its natural format without creating a table.

                    Special Considerations:
                    - Treat the content as highly sensitive data.
                    - If any part of the handwriting is ambiguous, indicate uncertainty using [?].
                    - For complex symbols or characters not easily typed, provide a detailed description in square brackets.

                    Output Format:
                    Provide the extracted text exactly as it appears in the original handwritten image, maintaining all formatting, line breaks, and spatial relationships between text elements. If the extracted text contains tables, represent them accurately using ASCII characters.

                    Final Instruction: Analyze both images thoroughly, then produce the most accurate transcription possible of the original handwritten document, drawing tables with ASCII characters if they are present.
                """,
                },
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/png;base64,{original_base64}"},
                },
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/png;base64,{extracted_base64}"},
                },
            ],
        }
    ]

    # Make the API call
    response = client.chat.completions.create(
        model="gpt-4-vision-preview", messages=messages, max_tokens=300
    )

    return response.choices[0].message.content
