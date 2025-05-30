import pytesseract
from PIL import Image
import logging

logger = logging.getLogger(__name__)

def extract_text_from_image(image_path: str) -> str:
    """
    Extract text from an image using Tesseract OCR.
    
    Args:
        image_path (str): Path to the image file
        
    Returns:
        str: Extracted text from the image
    """
    try:
        # Open the image
        image = Image.open(image_path)
        
        # Extract text using Tesseract
        text = pytesseract.image_to_string(image)
        
        # Clean up the text
        text = text.strip()
        
        if not text:
            raise ValueError("No text could be extracted from the image")
            
        return text
        
    except Exception as e:
        logger.error(f"Error in OCR processing: {e}")
        raise 