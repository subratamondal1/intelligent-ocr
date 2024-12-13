import base64
import io
from typing import Dict

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from PIL import Image
from starlette.requests import Request

from services.ocr_pipeline import ocr_pipeline

# Initialize FastAPI app
app = FastAPI(
    title="Intelligent OCR API",
    description="API for performing OCR on images with both UI and API endpoints",
    version="1.0.0"
)

# Static files and templates configuration
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


def process_image(image_contents: bytes) -> Image.Image:
    """Process uploaded image and convert to desired format.
    
    Args:
        image_contents: Raw bytes of the uploaded image
        
    Returns:
        PIL Image object in RGB mode
    """
    image = Image.open(io.BytesIO(image_contents))
    if image.mode != "RGB":
        image = image.convert("RGB")
    return image


def create_image_base64(image: Image.Image) -> str:
    """Convert PIL Image to base64 string.
    
    Args:
        image: PIL Image object
        
    Returns:
        Base64 encoded string of the image
    """
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")


@app.get(path="/", include_in_schema=False)
async def root() -> RedirectResponse:
    """Redirect root to API documentation."""
    return RedirectResponse(url="/docs")


@app.get("/v1/api/ai/upload/", response_class=HTMLResponse, tags=["UI"])
async def landing_page(request: Request) -> HTMLResponse:
    """Render the OCR upload form page.
    
    Args:
        request: FastAPI request object
        
    Returns:
        HTML page with upload form
    """
    return templates.TemplateResponse("upload.html", {"request": request})


@app.post("/v1/api/ai/upload/", response_class=HTMLResponse, tags=["UI"])
async def upload_image(
    request: Request,
    file: UploadFile = File(..., description="Image file to perform OCR on")
) -> HTMLResponse:
    """Process uploaded image and display OCR results in UI.
    
    Args:
        request: FastAPI request object
        file: Uploaded image file
        
    Returns:
        HTML page with OCR results and image preview
    """
    contents = await file.read()
    image = process_image(contents)
    
    # Create base64 image for display
    image_base64 = create_image_base64(image)
    image_src = f"data:image/jpeg;base64,{image_base64}"
    
    # Perform OCR
    ocr_text = ocr_pipeline(image=image)

    return templates.TemplateResponse(
        "upload.html",
        {
            "request": request,
            "file_name": file.filename,
            "uploaded_image": image_src,
            "ocr_text": ocr_text,
        },
    )


@app.post("/v1/api/ai/ocr/", tags=["API"])
async def ocr(
    file: UploadFile = File(..., description="Image file to perform OCR on")
) -> Dict[str, str]:
    """Perform OCR on uploaded image and return extracted text.
    
    Args:
        file: Uploaded image file
        
    Returns:
        Dictionary containing extracted text
    """
    contents = await file.read()
    image = process_image(contents)
    ocr_text = ocr_pipeline(image=image)
    
    return {"text": ocr_text}
