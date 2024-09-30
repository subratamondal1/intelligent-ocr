from PIL import Image

from services.claude_ai_vision import compare_and_correct_text
from services.enhance_text_visibility import enhance_text_visibility
from services.openai_vision import compare_images
from services.remove_horizontal_lines import remove_horizontal_lines
from services.synthesize_azure_ai_ocr import synthesize_azure_ai_ocr


def ocr_pipeline(image: Image.Image) -> str:
    """
    Run the entire OCR pipeline from start to finish.

    This pipeline applies the following steps in order:
    1. Remove horizontal lines from the image.
    2. Enhance text visibility.
    3. Apply Azure AI OCR to the enhanced image.
    4. Compare the extracted text with the original image using GPT-4o.
    5. Correct any errors in the extracted text using Claude AI.

    Returns the final corrected text.
    """
    removed_horizontal_lines: Image.Image = remove_horizontal_lines(
        pil_image=image,
        preserve_color="blue",
    )
    enhanced_text_visibility: Image.Image = enhance_text_visibility(
        pil_image=removed_horizontal_lines
    )
    synthesized_image_from_azure_ocr, extracted_text = synthesize_azure_ai_ocr(
        image=enhanced_text_visibility
    )
    gpt4o_compared_text = compare_images(
        final_processed_image=enhanced_text_visibility,
        synthesized_image=synthesized_image_from_azure_ocr,
    )

    claude_corrected_text = compare_and_correct_text(
        original_pil=enhanced_text_visibility,
        synthesized_pil=synthesized_image_from_azure_ocr,
        extracted_text=gpt4o_compared_text,
    )
    return claude_corrected_text
