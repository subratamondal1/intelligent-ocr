from services.enhance_text_visibility import enhance_text_visibility
from services.remove_horizontal_lines import remove_horizontal_lines

if __name__ == "__main__":
    removed_horizontal_lines = remove_horizontal_lines(
        image_path="data/raw images/01 table image with margin 1.jpeg",
        preserve_color="blue",
    )
    enhanced_text_visibility = enhance_text_visibility(
        pil_image=removed_horizontal_lines
    )
    enhanced_text_visibility.show(title="Enhanced Text Visibility")
