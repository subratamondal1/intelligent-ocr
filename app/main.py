from PIL import Image

from services.enhance_text_visibility import enhance_text_visibility
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
    # Step1: Extraction with Azure Vision AI OCR
    synthesized_image, extracted_text = synthesize_azure_ai_ocr(
        image=enhanced_text_visibility
    )
    synthesized_image.show()
    print(extracted_text)
