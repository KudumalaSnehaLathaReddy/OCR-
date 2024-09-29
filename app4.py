import streamlit as st
import easyocr
from PIL import Image, ImageOps
import requests
from io import BytesIO

# Set maximum file upload size to prevent large files
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB

# Lazy-load EasyOCR reader for performance
@st.cache_resource
def load_ocr_model(languages=['en', 'hi']):
    return easyocr.Reader(languages)

# Function to extract text from the image using EasyOCR, cached for performance
@st.cache_data
def extract_text_from_image(image_bytes):
    image = Image.open(BytesIO(image_bytes))
    reader = load_ocr_model()  # Load the OCR model
    result = reader.readtext(image)
    formatted_text = "\n".join([item[1] for item in result])
    return formatted_text

# Function to highlight the keyword in yellow and bold in the extracted text
def highlight_text(text, keyword):
    lines = text.splitlines()
    highlighted_lines = []
    for line in lines:
        highlighted_line = line.replace(keyword, f"<span style='background-color: yellow; font-weight: bold;'>{keyword}</span>")
        highlighted_lines.append(highlighted_line)
    return "<br>".join(highlighted_lines)

# Async function to get the meaning of the searched keyword using the Dictionary API
@st.cache_data
def get_keyword_meaning(keyword):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{keyword}"
    r = requests.get(url)
    data = r.json()

    if isinstance(data, list) and len(data) > 0:
        try:
            meanings = data[0]['meanings'][0]['definitions']
            meaning = meanings[0]['definition'] if meanings else "Meaning not found."
        except (IndexError, KeyError):
            meaning = "Meaning not found."
    elif isinstance(data, dict) and 'message' in data:
        meaning = data['message']  # For error messages
    else:
        meaning = "Could not retrieve meaning. Check your internet connection."

    return meaning

# Function to resize and preprocess image to reduce resource usage
def resize_image(image, max_size=(800, 800)):
    image.thumbnail(max_size)
    return image

# Streamlit application
st.title("OCR Web Application")

# Step 1: Upload image file (JPEG, PNG)
uploaded_file = st.file_uploader("Upload an image file (JPEG, PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Check file size before processing
    file_size = uploaded_file.size
    if file_size > MAX_FILE_SIZE:
        st.error(f"File size is too large ({file_size / (1024 * 1024):.2f} MB). Please upload a file smaller than 10 MB.")
    else:
        # Open the image
        image = Image.open(uploaded_file)

        # Resize image to reduce processing time
        image = resize_image(image)
        
        # Convert the image to bytes for EasyOCR processing
        img_byte_arr = BytesIO()
        image.save(img_byte_arr, format=image.format)
        image_bytes = img_byte_arr.getvalue()

        # Display the processed image
        st.image(image, caption="Processed Image", use_column_width=True)

        # Step 3: Extract text from the image (cached for faster reprocessing)
        extracted_text = extract_text_from_image(image_bytes)
        st.subheader("Extracted Text:")
        st.text(extracted_text)

        # Step 4: Search for keywords in the extracted text
        search_keyword = st.text_input("Enter keyword to search in the extracted text:")
        
        if search_keyword:
            if search_keyword.lower() in extracted_text.lower():
                # Highlight matching keywords in the extracted text
                highlighted_text = highlight_text(extracted_text, search_keyword)
                st.subheader("Search Results:")
                
                # Display the highlighted text as HTML to apply the background color and bold text
                st.markdown(highlighted_text, unsafe_allow_html=True)

                # Step 5: Get and display the meaning of the searched keyword
                meaning = get_keyword_meaning(search_keyword.lower())
                st.subheader(f"Meaning of '{search_keyword}':")
                st.write(meaning)
            else:
                # No matches found message
                st.subheader("Search Results:")
                st.write("No matches found.")
