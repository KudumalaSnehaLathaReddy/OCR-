import streamlit as st
from PIL import Image
import pytesseract
import requests
import re
import numpy as np
import cv2
from streamlit_drawable_canvas import st_canvas

# Set Tesseract-OCR path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Streamlit UI
st.title("OCR Web Application")

# Apply styling
st.markdown(
    """
    <style>
        body, .stApp {
            background-color: white !important;
            color: black !important;
        }
        .stMarkdown h1, .stMarkdown h2, .stMarkdown h3, .stMarkdown h4, .stMarkdown h5, .stMarkdown h6 {
            color: black !important;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Function to extract text from the image using Tesseract
def extract_text_from_image(image):
    text = pytesseract.image_to_string(image, lang='eng+hin')
    return text

# Function to highlight keyword
def highlight_text(text, keyword):
    highlighted_text = re.sub(
        f"\\b{re.escape(keyword)}\\b", 
        f"<span style='background-color: yellow; font-weight: bold;'>{keyword}</span>", 
        text, flags=re.IGNORECASE
    )
    return highlighted_text

# Function to get keyword meaning
def get_keyword_meaning(keyword):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{keyword}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if isinstance(data, list) and len(data) > 0:
            try:
                meanings = data[0]['meanings'][0]['definitions']
                return meanings[0]['definition'] if meanings else "Meaning not found."
            except (IndexError, KeyError):
                return "Meaning not found."
    return "Could not retrieve meaning. Check your internet connection."

# Upload image file
uploaded_file = st.file_uploader("Upload an image file (JPEG, PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    original_width, original_height = image.size
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Set canvas dimensions for selection (scaling to fit the screen)
    canvas_width = min(600, original_width)  
    scale_x = original_width / canvas_width  
    scale_y = original_height / (canvas_width * (original_height / original_width))

    # Drawing tool for selection
    st.subheader("Select the text area:")
    canvas_result = st_canvas(
        fill_color="rgba(255, 255, 255, 0.0)",
        stroke_width=2,
        stroke_color="#000000",
        background_image=image,
        update_streamlit=True,
        height=int(original_height / scale_y),  
        width=int(original_width / scale_x),  
        drawing_mode="rect",
        key="canvas",
    )

    # Extract selected region
    if canvas_result.json_data is not None:
        objects = canvas_result.json_data["objects"]
        if objects:
            obj = objects[0]
            left, top, width, height = obj["left"], obj["top"], obj["width"], obj["height"]

            # Scale coordinates back to original image size
            left = int(left * scale_x)
            top = int(top * scale_y)
            width = int(width * scale_x)
            height = int(height * scale_y)

            # Ensure cropping bounds are correct
            right = min(left + width, original_width)
            bottom = min(top + height, original_height)

            # Crop image
            cropped_image = image.crop((left, top, right, bottom))
            st.image(cropped_image, caption="Cropped Selection", use_column_width=True)

            # Extract text
            extracted_text = extract_text_from_image(cropped_image)
            st.subheader("Extracted Text:")
            selected_text = st.text_area("Edit or select extracted text:", extracted_text, height=200)

            # Keyword Search
            st.subheader("Search Keyword:")
            search_keyword = st.text_input("Enter keyword to search in the extracted text:")

            if search_keyword:
                if re.search(f"\\b{re.escape(search_keyword)}\\b", selected_text, flags=re.IGNORECASE):
                    highlighted_text = highlight_text(selected_text, search_keyword)
                    st.subheader("Search Results:")
                    st.markdown(highlighted_text, unsafe_allow_html=True)

                    # Get meaning of keyword
                    meaning = get_keyword_meaning(search_keyword.lower())
                    st.subheader(f"Meaning of '{search_keyword}':")
                    st.write(meaning)

                    # Provide Google search link instead of redirecting
                    google_search_url = f"https://www.google.com/search?q={search_keyword}+meaning"
                    st.markdown(f"[Search '{search_keyword}' on Google]({google_search_url})", unsafe_allow_html=True)


