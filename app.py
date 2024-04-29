import os
import random
import time

import google.generativeai as genai
from google.generativeai.types import HarmBlockThreshold, HarmCategory

import streamlit as st
from dotenv import load_dotenv
from PIL import Image

# Load environment variables
load_dotenv()

# Configure Streamlit app
st.set_page_config(page_title="Gemini Pro 1.5", page_icon="🤖")

# Configure Google AI API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

st.title("Chat with Gemini Pro")


# Function to generate and display response stream
def write_stream(prompt, image=None, safety_settings=None, generation_config=None):
    message_placeholder = st.empty()
    message_placeholder.markdown("Thinking...")
    try:
        full_response = ""
        if image:
            chucks = st.session_state.chat_model.send_message(
                [image, prompt],
                generation_config=generation_config,
                safety_settings=safety_settings,
                stream=True,
            )

        else:
            chucks = st.session_state.chat_model.send_message(
                prompt,
                generation_config=generation_config,
                safety_settings=safety_settings,
                stream=True,
            )

        chucks.resolve()

        for chunk in chucks:
            word_count = 0
            random_int = random.randint(5, 10)
            for word in chunk.text:
                full_response += word
                word_count += 1
                if word_count == random_int:
                    time.sleep(0.05)
                    message_placeholder.markdown(full_response + "_")
                    word_count = 0
                    random_int = random.randint(5, 10)
        message_placeholder.markdown(full_response)
        return full_response

    except genai.types.generation_types.BlockedPromptException as e:
        st.exception(e)
    except Exception as e:
        st.exception(e)


if "system_instruction" not in st.session_state:
    st.session_state.system_instruction = """You are a helpful AI assistant and are talkative, proficient in both English and Vietnamese languages, and provide lots of specific details from your context. If you do not know the answer to a question, you truthfully say you do not know.
    """

# Initialize chat and vision model instances
if "model" not in st.session_state:
    st.session_state.model = genai.GenerativeModel("gemini-1.5-pro-latest",
                                                   system_instruction=st.session_state.system_instruction)
    st.session_state.chat_model = st.session_state.model.start_chat()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "Hi there. Can I help you?"}
    ]

# Sidebar configuration
with st.sidebar:
    upload_image = st.file_uploader(
        "Upload Your Image Here",
        accept_multiple_files=False,
        type=["jpg", "png", "jpg"],
        key="image_uploader"
    )

    st.divider()

    if upload_image:
        image = Image.open(upload_image)
    else:
        image = None  # Reset image if no file is uploaded

    st.write("Adjust Model Parameters Here:")
    temperature = st.number_input(
        "Temperature", min_value=0.0, max_value=2.0, value=0.1, step=0.01
    )
    max_token = st.number_input(
        "Maximum Output Tokens", min_value=1, max_value=4096, value=3000
    )
    top_p = st.number_input(
        "Top-P sampling", min_value=0.0, max_value=1.0, value=0.7, step=0.01
    )
    top_k = st.number_input(
        "Top-K sampling", min_value=0, max_value=50, value=20, step=1
    )
    generation_config = genai.types.GenerationConfig(
        max_output_tokens=max_token, temperature=temperature, top_p=top_p, top_k=top_k
    )

    st.divider()

    st.write("Adjust Safety Settings Here:")

    harm_categories = {
        "Dangerous Content": HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
        "Harassment": HarmCategory.HARM_CATEGORY_HARASSMENT,
        "Hate Speech": HarmCategory.HARM_CATEGORY_HATE_SPEECH,
        "Sexually Explicit": HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
    }

    harm_threshold_options = {
        "Allow All": HarmBlockThreshold.BLOCK_NONE,
        "Block Low and Above": HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
        "Block Medium and Above": HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        "Block High": HarmBlockThreshold.BLOCK_ONLY_HIGH,
    }

    safety_settings = {}
    for category_name, category in harm_categories.items():
        threshold = st.selectbox(
            f"**{category_name}**",
            harm_threshold_options.keys(),
            index=0,
            key=f"{category}_threshold",
        )
        safety_settings[category] = harm_threshold_options[threshold]

    st.divider()
    if st.button("Clear Chat History"):
        st.session_state.messages = [st.session_state.messages[0]]
        st.session_state.chat_model = st.session_state.model.start_chat()

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
        if msg.get("image"):
            st.image(msg.get("image"), width=300)

if prompt := st.chat_input():
    with st.chat_message("user"):
        st.write(prompt)

        if image:
            st.image(image, width=300)

        st.session_state.messages.append(
            {"role": "user", "content": prompt, "image": image}
        )

    with st.chat_message("assistant"):
        msg = write_stream(
            prompt, image, safety_settings=safety_settings, generation_config=generation_config
        )
        st.session_state.messages.append({"role": "assistant", "content": msg})
