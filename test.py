import cv2
import pytesseract


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

image = cv2.imread("coffee2.jpeg", cv2.IMREAD_GRAYSCALE) 
print(pytesseract.image_to_string(image, lang='eng', config='--psm 4 --oem 1'))