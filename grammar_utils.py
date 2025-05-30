import os
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

async def correct_grammar(text: str) -> str:
    """
    Temporarily bypass grammar correction and return the original text.
    
    Args:
        text (str): Text to be processed
        
    Returns:
        str: Original text
    """
    logger.info(f"Bypassing grammar correction for text: {text[:100]}...")
    return text 