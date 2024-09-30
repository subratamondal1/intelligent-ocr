from PIL import Image

from services.enhance_text_visibility import enhance_text_visibility
from services.openai_vision import compare_images
from services.remove_horizontal_lines import remove_horizontal_lines
from services.synthesize_azure_ai_ocr import synthesize_azure_ai_ocr

if __name__ == "__main__":
    removed_horizontal_lines: Image.Image = remove_horizontal_lines(
        image_path="data/raw images/01 table image with margin 1.jpeg",
        preserve_color="blue",
    )
    enhanced_text_visibility: Image.Image = enhance_text_visibility(
        pil_image=removed_horizontal_lines
    )
    synthesized_image_from_azure_ocr, extracted_text = synthesize_azure_ai_ocr(
        image=enhanced_text_visibility
    )
    synthesized_image_from_azure_ocr.show()
    print(extracted_text)
    compared_text = compare_images(
        final_processed_image=enhanced_text_visibility,
        synthesized_image=synthesized_image_from_azure_ocr,
    )
    print(compared_text)
