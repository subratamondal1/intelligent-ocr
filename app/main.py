from PIL import Image

from services.azure_vision_ai_ocr import azure_vision_ai_ocr
from services.enhance_text_visibility import enhance_text_visibility
from services.remove_horizontal_lines import remove_horizontal_lines

if __name__ == "__main__":
    removed_horizontal_lines: Image.Image = remove_horizontal_lines(
        image_path="data/raw images/01 table image with margin 1.jpeg",
        preserve_color="blue",
    )
    enhanced_text_visibility: Image.Image = enhance_text_visibility(
        pil_image=removed_horizontal_lines
    )
    # Step1: Extraction with Azure Vision AI OCR
    azure_image, azure_extracted_text = azure_vision_ai_ocr(
        image=enhanced_text_visibility
    )
