from PIL import Image

from services.claude_ai_vision import compare_and_correct_text
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
    print("=*=" * 50)
    print("Compared text:")
    print(compared_text)
    print()

    corrected_text = compare_and_correct_text(
        final_processed_image=enhanced_text_visibility,
        extracted_text=extracted_text,
    )

    print("=*=" * 50)
    print("Corrected text:")
    print(corrected_text)
    print()
