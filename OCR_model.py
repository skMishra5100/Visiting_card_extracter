import cv2
import requests
import pandas as pd
import numpy as np

def img_processing(img_path):
    # Read image
    img = cv2.imread(img_path)
    # ----- CONTRAST ENHANCEMENT -----
    # Convert BGR → LAB
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)

    l, a, b = cv2.split(lab)

    # Apply CLAHE on L-channel
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    l = clahe.apply(l)

    # Merge back
    enhanced = cv2.merge((l, a, b))
    enhanced = cv2.cvtColor(enhanced, cv2.COLOR_LAB2BGR)

    # ----- SHARPENING -----
    kernel = np.array([
        [0, -1,  0],
        [-1, 5, -1],
        [0, -1,  0]
    ])

    sharpened = cv2.filter2D(enhanced, -1, kernel)

    # Save processed image
    processed_path = "processed.jpg"
    cv2.imwrite(processed_path, sharpened)

    return processed_path



def is_duplicate(details,csv_path):
    DF=pd.read_csv(csv_path)
    email=details.get("email").strip().lower()

    if email in DF["email"].values:
        return True
    


def ocr_model(img_path,API_key):
    server_url="https://api.ocr.space/parse/image" # OCR.space 

    payload={
        "apikey":API_key, #ocr model key 
        "language":"eng", #language
        "OCRengine":2, #OCR engine version
        "isOverlayRequired":False
    }

    with open(img_path,"rb") as f: #It opens the image and sends it to the OCR.space server so the server can extract text.
        response=requests.post(
            server_url,
            files={"file":f},
            data=payload
        ) #This code opens an image file in binary mode and sends it via a POST request to the OCR.space API along with an API key, receiving extracted text as a JSON response.

    text=response.json()

    return text["ParsedResults"][0]["ParsedText"]


    

