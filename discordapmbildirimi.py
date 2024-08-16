import cv2
import numpy as np
import pyautogui
import pytesseract
from screeninfo import get_monitors
import requests
import time
import psutil
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
WEBHOOK_URL = 'webhook'
def get_mac_address():
    try:
        for interface, addrs in psutil.net_if_addrs().items():
            for addr in addrs:
                if addr.family == psutil.AF_LINK:
                    return addr.address
        return None
    except Exception as e:
        print(f"Error getting MAC address: {e}")
        return None
MAC_ID = get_mac_address()
sent_texts = set()

def send_discord_notification(message):
    payload = {'content': message}
    response = requests.post(WEBHOOK_URL, json=payload)
    print(f"Webhook response status code: {response.status_code}")
    print(f"Webhook response text: {response.text}")
    if response.status_code == 204:
        print("Webhook notification sent successfully.")
    else:
        print(f"Failed to send webhook notification. Status code: {response.status_code}")

def capture_screen(region=None):
    screenshot = pyautogui.screenshot(region=region)
    screenshot_np = np.array(screenshot)
    return screenshot_np

def preprocess_image(image):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    contrast_image = cv2.convertScaleAbs(gray_image, alpha=1.5, beta=0)
    _, threshold_image = cv2.threshold(contrast_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    kernel = np.array([[0, -1, 0], [-1, 5,-1], [0, -1, 0]])
    sharpened_image = cv2.filter2D(threshold_image, -1, kernel)
    return sharpened_image

def detect_text(image):
    processed_image = preprocess_image(image)
    text = pytesseract.image_to_string(processed_image, config='--psm 6')
    return text

def extract_pm_text(text):
    lines = text.splitlines()
    pm_lines = [line for line in lines if '[PM]' in line]
    
    return pm_lines

def format_message(text):
    formatted_message = f"**{MAC_ID}**'li kullanıcıya **[PM]** geldi, tam metin:\n{text}"
    return formatted_message

def main():
    monitors = get_monitors()
    monitor = monitors[0]
    region = (monitor.x + 10, monitor.y + 50, 500, 300)
    
    last_detection_time = time.time()
    detection_interval = 10
    
    while True:
        current_time = time.time()
        if current_time - last_detection_time >= detection_interval:
            print("Capturing screen...")
            screen = capture_screen(region=region)
            detected_text = detect_text(screen)
            print(f"Detected text: {detected_text}")
            filtered_text = extract_pm_text(detected_text)
            for line in filtered_text:
                formatted_message = format_message(line)
                if formatted_message not in sent_texts:
                    print(f"Sending to Discord: {formatted_message}")
                    send_discord_notification(formatted_message)
                    sent_texts.add(formatted_message)
            
            last_detection_time = current_time
        if 'screen' in locals():
            cv2.imshow('PM', screen)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

# ekranın sol üst köşesine yaslanan oyun penceresinden chati takip ederek gelen pmleri discord webhookuna atarak adminlere veya oyunculara yakalanmamayi hedefler 