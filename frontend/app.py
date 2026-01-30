import streamlit as st
import pandas as pd
import requests
import os

API_URL="http://127.0.0.1:8000/send_img"

st.set_page_config(
    page_title="Upload visiting card image",
    page_icon="📊",
    layout="wide"
)

st.title("Visiting Card Info Extracter")


st.subheader("📤 Upload Visiting Card")

uploaded_image = st.file_uploader(
    "Upload visiting card image",
    type=["png", "jpg", "jpeg"]
)



if uploaded_image is not None:
    st.image(
        uploaded_image,
        caption="Uploaded Visiting Card",
        width=300 
        )
    if st.button("Visiting Card Info extracter"):
        files={
            "file":(
                uploaded_image.name,
                uploaded_image.getvalue(),
                uploaded_image.type
            )
        }
        try:
            res=requests.post(API_URL, files=files)
            st.success("Image sent successfully")
            st.write(res.json())

        except requests.exceptions.ConnectionError:
            st.error("❌ Cannot connect to FastAPI. Is the server running?")

    


st.subheader("📋 Card Details")

csv_path = "../data/visiting_card_detail.csv"

columns = ["name", "designation","email", "phone", "company-name","address","website-name"]


if not os.path.exists(csv_path):
    DF = pd.DataFrame(columns=columns)
    DF.to_csv(csv_path, index=False)
else:
    DF=pd.read_csv(csv_path)
    DF=pd.DataFrame(DF)
    
st.dataframe(DF, width="stretch", hide_index=True)

st.markdown("---")
