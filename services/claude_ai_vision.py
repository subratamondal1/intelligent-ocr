import base64
import io
import os

from anthropic import Anthropic
from dotenv import load_dotenv

# Load the environment variables from the .env file
load_dotenv()

CLAUDE_KEY = os.getenv(key="CLAUDE_KEY", default="")

# Initialize the Anthropic client
client = Anthropic(api_key=CLAUDE_KEY)


def encode_pil_image(pil_image):
    buffered = io.BytesIO()
    pil_image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")


def compare_and_correct_text(original_pil, synthesized_pil, extracted_text):
    # Encode both PIL images
    base64_original = encode_pil_image(original_pil)
    base64_synthesized = encode_pil_image(synthesized_pil)

    # Prepare the messages for the API call
    messages = [
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": """
                            Task: Final Precision Text Extraction and Verification

                            Input:
                            1. Original handwritten image
                            2. Synthesized image (based on OCR extraction)
                            3. Pre-corrected extracted text (from GPT-4o)

                            Context: This is the third and final pass in a high-precision text extraction pipeline. Previous steps include Microsoft Azure Vision AI OCR and GPT-4V correction. The current accuracy is estimated at 99%, aiming for 100%.

                            Objective: Perform a meticulous final review and correction of the extracted text, focusing on eliminating the remaining 1% error rate.

                            Guidelines:
                            1. Prioritize the original handwritten image as the ultimate source of truth.
                            2. Use the synthesized image and pre-corrected text as high-confidence references.
                            3. Conduct a character-by-character comparison between all three inputs.
                            4. Pay exceptional attention to:
                              - Numerical data
                              - Special characters and symbols
                              - Formatting, including line breaks and spacing
                              - Capitalization and punctuation
                            5. Preserve the exact structure and layout of the original handwritten text.
                            6. Do not introduce new interpretations or significant changes to the pre-corrected text.
                            7. If discrepancies are found, always defer to the original handwritten image.

                            Special Instructions for Tables:
                            - If any tabular data is detected, represent it using ASCII characters (e.g., |, -, +) to create a visually accurate table that mirrors the structure of the original handwritten image.
                            - Maintain the alignment of columns and rows to ensure the table's readability and accuracy.
                            - If the content is not tabular, output the text in its natural format without creating a table.


                            Error Handling:
                            - For any remaining ambiguities, replace or remove them.
                            - If a character is indecipherable, describe it in detail using [description] format.

                            Verification Process:
                            1. Scan the entire document systematically, line by line.
                            2. Cross-reference each word and character across all three inputs.
                            3. Identify and correct any remaining discrepancies, no matter how minor.
                            4. Double-check all corrections against the original image.

                            Note:
                            In case of, if the transcription provided accurately reflects the original handwritten image, with 100% fidelity in terms of text content, formatting, symbols, and layout. Then no 
                            corrections are required and in that case return the TEXT AS IT IS with no extra words added.

                            Output Format:
                            Provide the final, corrected text exactly as it appears in the original handwritten image. Maintain all formatting, line breaks, and spatial relationships between text elements.

                            Final Instruction: Analyze all inputs thoroughly, then produce the most accurate transcription possible of the original handwritten document, aiming for 100% fidelity to the source material.
                            """,
                },
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/png",
                        "data": base64_original,
                    },
                },
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/png",
                        "data": base64_synthesized,
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
