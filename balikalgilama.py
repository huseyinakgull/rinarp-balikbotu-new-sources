import cv2
import numpy as np
from PIL import ImageGrab
import pyautogui
import time
from screeninfo import get_monitors
monitor = get_monitors()[0]
screen_width = monitor.width
screen_height = monitor.height
region = (screen_width - 100, screen_height - 300, screen_width, screen_height - 45)
def is_green(pixel):
    b, g, r = pixel
    return g > 200 and b < 100 and r < 100
last_green_time = time.time()
last_action_time = time.time()
green_detected = False
while True:
    screen = np.array(ImageGrab.grab(bbox=region))
    screen_cv = cv2.cvtColor(screen, cv2.COLOR_RGB2BGR)
    green_detected = False
    for row in screen_cv:
        for pixel in row:
            if is_green(pixel):
                green_detected = True
                last_green_time = time.time()
                break
        if green_detected:
            break
    current_time = time.time()
    if green_detected:
        pyautogui.press('x')
        time.sleep(3)
        pyautogui.press('x')
        last_action_time = current_time
    if current_time - last_green_time > 20:
        pyautogui.press('x')
        last_action_time = current_time
        last_green_time = current_time
    time.sleep(0.1)
    # Daha öncesinde virtual camera uygulamaları ile ekranı yansıtmanın kullanıcı dostu hali, herhangi bir uygulamaya ihtiyaç duymadan otomatik olarak ekranın sağ alt kısmını grabler; imshowla preview açarsınız.