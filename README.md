# OCR Web Application

This web application extracts text from images containing both Hindi and English text using OCR (Optical Character Recognition) and 
allows users to search for specific keywords within the extracted text. The application also fetches the meaning of the keyword using 
the Dictionary API.

## Features

- Upload an image (JPEG, PNG) to extract text from it.
- Extracts both Hindi and English text using the EasyOCR model.
- Search for specific keywords in the extracted text and highlights the results.
- Fetch the meaning of the keyword using the Dictionary API.

## Table of Contents

1. [Installation](#installation)
2. [Running the App Locally](#running-the-app-locally)
3. [Deployment](#deployment)
4. [File Structure](#file-structure)
5. [Example Use](#example-use)
6. [Troubleshooting](#troubleshooting)

## Installation

### Prerequisites

- Python 3.7 or later
- pip (Python package manager)
- Git (optional, to clone the repository)
- Streamlit (for running the web application)

### Step 1: Clone the Repository

If you haven't already, clone the repository from GitHub or download the source code:

```bash
git clone https://github.com/your-username/ocr-web-app.git
cd ocr-web-app
```

Or download the ZIP file and extract it.

### Step 2: Create a Virtual Environment (Optional)

To avoid conflicts between dependencies, it’s recommended to create a virtual environment:

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install the Dependencies

Install the required Python libraries using `pip`:

```bash
pip install -r requirements.txt
```

This will install the following packages:

- `streamlit`: For creating the web application.
- `easyocr`: The OCR model for extracting text from images.
- `Pillow`: For image handling and processing.
- `requests`: To call the Dictionary API for keyword meanings.

### Step 4: Set Up the Dictionary API (Optional)

If you are using a custom Dictionary API, update the API URL in the code. The default configuration uses the free dictionary API
at [https://api.dictionaryapi.dev](https://api.dictionaryapi.dev).

## Running the App Locally

### Step 1: Start the Streamlit Application

After installing the dependencies, you can run the web application with the following command:

```bash
streamlit run app.py
```

### Step 2: Upload an Image and Test the Functionality

- Open your browser and go to `http://localhost:8501`.
- Upload a JPEG or PNG image that contains Hindi and/or English text.
- Extract the text and search for specific keywords.

## Deployment

### Deploying to Streamlit Cloud

1. Push your project to a GitHub repository (if not already).
2. Go to [Streamlit Cloud](https://share.streamlit.io/) and log in with your GitHub account.
3. Create a new app and select your repository and branch.
4. Specify the path to your `app.py` file.
5. Deploy the application, and Streamlit Cloud will provide you with a live URL.

Example URL:
```
https://share.streamlit.io/your-username/ocr-web-app/main/app.py
```

### Deploying to Hugging Face Spaces

1. Log in to your Hugging Face account and go to [Hugging Face Spaces](https://huggingface.co/spaces).
2. Create a new space and choose **Streamlit** as the environment.
3. Connect your GitHub repository or manually upload your files.
4. Deploy the application and Hugging Face Spaces will provide a live URL.

Example URL:
```
https://huggingface.co/spaces/your-username/ocr-web-app
```

## File Structure

```bash
OCR_Web_App/
├── app.py               # Main Python file for the web application
├── requirements.txt      # List of required dependencies
├── README.md             # Instructions and details for setting up the app
└── assets/               # Folder to store any additional assets (e.g., screenshots)
```

## Example Use

1. Upload an image (JPEG or PNG) with Hindi and/or English text.
2. The app will extract the text from the image using the EasyOCR model.
3. Enter a keyword to search in the extracted text.
4. The app highlights the keyword in the text and fetches its meaning using the Dictionary API.

## Troubleshooting

- **App Running Slowly:** If the app is slow, consider reducing the size of the images being uploaded or deploying the app on a server with more resources.
- **No Text Extracted:** Make sure the image quality is good and that the text is clearly visible for the OCR model to work effectively.
- **Meaning Not Found:** If the Dictionary API fails, ensure that the internet connection is active and the API endpoint is correct.

