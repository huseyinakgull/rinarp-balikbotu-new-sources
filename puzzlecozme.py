import cv2
import numpy as np
import pyautogui
from PIL import ImageGrab
import time
import glob
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
triangle_template = cv2.imread('triangle.png', 0)
triangle_w, triangle_h = triangle_template.shape[::-1]
slot_templates = [cv2.imread(file, 0) for file in glob.glob('puzzle*.png')]
def capture_screen(region=None):
    screenshot = ImageGrab.grab(bbox=region)
    screenshot_np = np.array(screenshot)
    return cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2RGB)
def find_template(image, template, threshold=0.9):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    res = cv2.matchTemplate(gray_image, template, cv2.TM_CCOEFF_NORMED)
    loc = np.where(res >= threshold)
    if len(loc[0]) > 0:
        for pt in zip(*loc[::-1]):
            return pt[0], pt[1]
    return None
def detect_puzzle_piece(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)
        return x, y, w, h
    return None
def move_slider(start, end):
    pyautogui.moveTo(start)
    pyautogui.mouseDown()
    pyautogui.moveTo(end, duration=0.5)
    pyautogui.mouseUp()
while True:
    screen = capture_screen()
    triangle_pos = find_template(screen, triangle_template)
    if triangle_pos:
        triangle_x, triangle_y = triangle_pos
        piece = detect_puzzle_piece(screen)
        if piece:
            x, y, w, h = piece
            for i, slot_template in enumerate(slot_templates):
                slot_pos = find_template(screen, slot_template)
                if slot_pos:
                    slot_x, slot_y = slot_pos
                    end_point = (slot_x + slot_template.shape[1] // 2 + 4, triangle_y)
                    pyautogui.moveTo(triangle_x + triangle_w // 2, triangle_y)
                    pyautogui.mouseDown()
                    pyautogui.moveTo(end_point, duration=0.5)
                    pyautogui.mouseUp()
                    break
    time.sleep(1)

    # image recognition ile basit sekilde puzzle cozer