from fastapi import FastAPI,UploadFile,File
import os
from dotenv import load_dotenv
load_dotenv()
import pandas as pd
import json
from OCR_model import ocr_model ,is_duplicate,img_processing
from LLM_model import llm_model
import shutil

app=FastAPI()

UPLOAD_DIR="Visiting_Cards"
CSV_path="data/visiting_card_detail.csv"
@app.post("/send_img")
def send_img(file:UploadFile=File(...)): 
    API_KEY=os.getenv("KEY")
    try:
        IMG_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(IMG_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)

        img=img_processing(IMG_path)#*****
        details=ocr_model(img,API_KEY)       
        model=llm_model()
        Card_detail=model.invoke({"details": details})
        details=json.loads(Card_detail)
        if is_duplicate(details,CSV_path):
            return {
                "message": "Duplicate visiting card detected",
                "status": "duplicate"
                }
        CD=pd.DataFrame([details])     
        CD.to_csv(CSV_path,
                mode="a",
                header=not os.path.exists(CSV_path),
                encoding="utf-8",
                index=False)
    except Exception as E:
            print(E)