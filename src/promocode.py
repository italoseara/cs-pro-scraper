import cv2
import pytesseract
import numpy as np
from PIL import Image


class PromocodeReader:
    image: cv2.typing.MatLike

    def __init__(self, image: Image.Image) -> None:
        rgb_image = image.convert("RGB")
        array_image = np.array(rgb_image)
        self.image = cv2.cvtColor(array_image, cv2.COLOR_RGB2BGR)

    def extract(self) -> str:
        """Extract the promocode from the image."""
        
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        self.image = self.image[335:400, 55:455]
        _, self.image = cv2.threshold(self.image, 127, 255, cv2.THRESH_BINARY)

        # Open image (for debugging)
        # cv2.imshow("Image", self.image)
        # cv2.waitKey(0)

        text = pytesseract.image_to_string(self.image, config="--psm 6")
        text = "".join(char for char in text if char.isalnum()) 
        
        return text.strip()
