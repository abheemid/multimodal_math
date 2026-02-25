# Import required libraries
import streamlit as st  # for creating the web app
from dotenv import load_dotenv  # for loading API key from .env file
import os
import google.generativeai as genai  # Google's AI model
from PIL import Image  # for handling images

# Load the API key from .env file
load_dotenv()

# Set up the Google Gemini AI with your API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to get AI response about the food image
def get_gemini_response(image, prompt):
    """Send image to Google's AI and solve the math problem"""
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content([image[0], prompt])
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

# Function to prepare the uploaded image for AI processing
def prepare_image(uploaded_file):
    """Convert uploaded image to format required by Google's AI"""
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        return None

# Main web app
def main():
    # Set up the webpage
    st.set_page_config(page_title="Math Problem Solver", page_icon="🔢")
    
    # Add title and description
    st.title("🔢 Math Advisor")
    st.write("Upload a photo of your math problem to solve it!")

    # Create file uploader
    uploaded_file = st.file_uploader(
        "Upload your math problem image (jpg, jpeg, or png)",
        type=["jpg", "jpeg", "png"]
    )

    # Display uploaded image
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Your Math Problem Image", use_column_width=True)

        # Create Analyze button
        if st.button("Solve the problem"):
            with st.spinner("Analyzing your math problem..."):
                # Prepare the prompt for AI
                prompt = """
                Please solve this math image and provide:
                1. Step-by-step breakdown
                2. Solution

                Format like this:
                Step-by-step breakdown:
                1. [calculation] = [result]
                2. [calculation] = [result]

                Solution: [Number]

                """

                # Get and display AI response
                image_data = prepare_image(uploaded_file)
                if image_data is not None:
                    response = get_gemini_response(image_data, prompt)
                    st.success("Analysis Complete!")
                    st.write(response)
                else:
                    st.error("Please upload an image first!")

# Run the app
if __name__ == "__main__":
    main()
