import streamlit as st
import easyocr
from PIL import Image
import requests

# Create an EasyOCR reader instance
reader = easyocr.Reader(['en', 'hi'])  # Specify languages

# Function to extract text from the image using EasyOCR
def extract_text_from_image(image):
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

# Function to get the meaning of the searched keyword using the Dictionary API
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

# Streamlit application
st.title("OCR Web Application")

# Step 1: Upload image file (JPEG, PNG)
uploaded_file = st.file_uploader("Upload an image file (JPEG, PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Step 2: Open and display the uploaded image
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Step 3: Extract text from the image
    extracted_text = extract_text_from_image(image)
    st.subheader("Extracted Text:")
    
    # Display the extracted text as-is with line breaks
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
