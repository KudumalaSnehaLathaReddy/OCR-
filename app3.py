import streamlit as st
from PIL import Image
import pytesseract
import requests
import re
import webbrowser
import numpy as np
import cv2
from streamlit_drawable_canvas import st_canvas

# Set Tesseract-OCR path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Streamlit UI
st.title("OCR Web Application with Google Search")

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

# Function to search on Google
def search_google(query):
    search_url = f"https://www.google.com/search?q={query}"
    webbrowser.open(search_url)

# Upload image file
uploaded_file = st.file_uploader("Upload an image file (JPEG, PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    original_width, original_height = image.size
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Extract text
    extracted_text = extract_text_from_image(image)
    st.subheader("Extracted Text:")
    selected_text = st.text_area("Edit or select extracted text:", extracted_text, height=200)
    
    # Google Search Button
    if st.button("Search Extracted Text in Google"):
        search_google(selected_text)

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

            # Provide Google search link
            google_search_url = f"https://www.google.com/search?q={search_keyword}+meaning"
            st.markdown(f"[Search '{search_keyword}' on Google]({google_search_url})", unsafe_allow_html=True)
