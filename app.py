import os
import shutil
import streamlit as st
from PIL import Image
from lyzr import ChatBot

# Set the OpenAI API key
os.environ["OPENAI_API_KEY"] = st.secrets["apikey"]

# Set Streamlit page configuration
st.set_page_config(
    page_title="Lyzr",
    layout="centered",
    initial_sidebar_state="auto",
    page_icon="./logo/lyzr-logo-cut.png",
)

# Load and display the logo
image = Image.open("./logo/lyzr-logo.png")
st.image(image, width=150)

# App title and introduction
st.title("Study Planner📚")
st.markdown("### Built using Lyzr SDK🚀")
st.markdown(" Immerse yourself in efficient studying with our Study Planner app! Generate a tailored study schedule effortlessly based on your syllabus, ensuring optimal utilization of your free time.")

# Function to remove existing files in the directory
def remove_existing_files(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            st.error(f"Error while removing existing files: {e}")

# Set the local directory
data_directory = "data"

# Create the data directory if it doesn't exist
os.makedirs(data_directory, exist_ok=True)

# Remove existing files in the data directory
remove_existing_files(data_directory)


# File upload widget
uploaded_file = st.file_uploader("Choose Word file", type=["docx"])

# User inputs for number of free days in a week and number of months for preparation
if uploaded_file is not None:
    num_free_days_week = st.number_input("Number of free days in a week", min_value=1, max_value=7, value=3)
    num_months_preparation = st.number_input("Number of months for preparation", min_value=1, value=2)
    button_clicked = st.button("OK")
else:
    num_free_days_week = None
    num_months_preparation = None
    button_clicked = False

# Function to implement RAG Lyzr Chatbot
def rag_implementation():
    # Get the file path
    file_path = get_files_in_directory()[0]

    # Initialize the RAG Lyzr ChatBot
    rag = ChatBot.docx_chat(
        input_files=[file_path],
        llm_params={"model": "gpt-3.5-turbo"},
    )


    return rag

# Function to get files in directory
def get_files_in_directory(directory="data"):
    files_list = []

    if os.path.exists(directory) and os.path.isdir(directory):
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path):
                files_list.append(file_path)

    return files_list

# Function to get Lyzr response
def resume_response():
    rag = rag_implementation()
    prompt = f"""Please follow the instructions below to create a study schedule based on the provided syllabus, the number of free days in a week ({num_free_days_week} days), and the number of months for preparation ({num_months_preparation} months):

- After that, create an effective study plan for the topics provided.
- Ensure that all the topics are covered within the crash study plan.
- Try to specify in-depth about each day and the subjects that can be studied."""

    response = rag.chat(prompt)
    return response.response

# If file is uploaded and user inputs are provided
if button_clicked:
    if uploaded_file is not None and num_free_days_week is not None and num_months_preparation is not None:
        # Save the uploaded Word file to the data directory
        file_path = os.path.join(data_directory, uploaded_file.name)
        with open(file_path, "wb") as file:
            file.write(uploaded_file.getvalue())

        # Display success message
        st.success(f"File successfully saved")

        # Get Lyzr response
        automatic_response = resume_response()
        st.markdown(f"""{automatic_response}""")

# Footer or any additional information
with st.expander("ℹ️ - About this App"):
    st.markdown(
        """Experience the seamless integration of Lyzr's ChatBot as you refine your documents with ease. For any inquiries or issues, please contact Lyzr."""
    )
    st.link_button("Lyzr", url="https://www.lyzr.ai/", use_container_width=True)
    st.link_button(
        "Book a Demo", url="https://www.lyzr.ai/book-demo/", use_container_width=True
    )
    st.link_button(
        "Discord", url="https://discord.gg/nm7zSyEFA2", use_container_width=True
    )
    st.link_button(
        "Slack",
        url="https://join.slack.com/t/genaiforenterprise/shared_invite/zt-2a7fr38f7-_QDOY1W1WSlSiYNAEncLGw",
        use_container_width=True,
    )
