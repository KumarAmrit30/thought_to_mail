import os
import logging
from google.cloud import vision

logger = logging.getLogger(__name__)

def extract_text_from_image(image_path: str) -> str:
    """
    Extract text from an image using Google Cloud Vision OCR.
    
    Args:
        image_path (str): Path to the image file
        
    Returns:
        str: Extracted text from the image
    """
    try:
        # Set the environment variable for authentication
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "google-vision-key.json"

        client = vision.ImageAnnotatorClient()
        with open(image_path, "rb") as image_file:
            content = image_file.read()
        image = vision.Image(content=content)
        response = client.document_text_detection(image=image)
        text = response.full_text_annotation.text.strip()
        if not text:
            raise ValueError("No text could be extracted from the image")
        return text
    except Exception as e:
        logger.error(f"Error in OCR processing: {e}")
        raise 