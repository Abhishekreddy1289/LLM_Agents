import streamlit as st
from agent_llm import LLMAgent
import time
from config import api_version

# Set the page title and layout
st.set_page_config(page_title="Abhi Search Engine using LLM Agent", layout="wide")

# Initialize session state variables
if 'api_key' not in st.session_state:
    st.session_state.api_key = ''
if 'endpoint' not in st.session_state:
    st.session_state.endpoint = ''
if 'version' not in st.session_state:
    st.session_state.version = ''
if 'model_name' not in st.session_state:
    st.session_state.model_name = ''
if 'openai_type' not in st.session_state:
    st.session_state.openai_type = ''
if 'input_key' not in st.session_state:  # Ensure input_key is initialized
    st.session_state.input_key = None

# Function to display the modal
def display_modal():
    with st.expander("Please enter your Model Details:", expanded=False):
        # User selection for OpenAI or Azure OpenAI
        service = st.selectbox("Select Service", ["OpenAI", "Azure OpenAI"])
        with st.form(key='model_details_form'):
            if service == "OpenAI":
                st.session_state.openai_type = "openai"
                st.session_state.api_key = st.text_input("API Key", type="password")
                st.session_state.model_name = st.text_input("Model Name")
                st.session_state.user_name = st.text_input("User Name/ID")
            elif service == "Azure OpenAI":
                st.session_state.openai_type = "azure_openai"
                st.session_state.api_key = st.text_input("API Key", type="password")
                st.session_state.endpoint = st.text_input("Endpoint")
                st.session_state.version = st.text_input("Version")
                st.session_state.model_name = st.text_input("Model Name")
                st.session_state.user_name = st.text_input("User Name/ID")

            if st.form_submit_button("Submit"):
                # Collect and display the input values
                st.success("Details submitted successfully!")

# Display the modal when the app starts
display_modal()

# Function to show notification
def show_notification(message, message_type="success"):
    # Define CSS styles for the notification
    css = f"""
    <style>
    .notification {{
        position: fixed;
        top: 0;
        right: 0;
        margin: 20px;
        padding: 10px 20px;
        color: white; /* Text color */
        border-radius: 5px;
        z-index: 1000; /* Ensure it's on top */
        background-color: {"#4CAF50" if message_type == "success" else "#f44336"}; /* Green for success, red for error */
    }}
    </style>
    """
    notification_placeholder = st.empty()
    notification_placeholder.markdown(f'{css}<div class="notification">{message}</div>', unsafe_allow_html=True)
    time.sleep(5)
    notification_placeholder.empty()

# Initialize AI Agent if API key is available
if st.session_state.api_key and st.session_state.model_name:
    openai_type = st.session_state.openai_type
    gpt_engine_name = st.session_state.model_name
    azure_endpoint = st.session_state.endpoint
    api_key = st.session_state.api_key
    api_version = st.session_state.version
    ai_agent = LLMAgent(
        api_key=api_key,
        openai_type=openai_type,
        azure_endpoint=azure_endpoint,
        api_version=api_version,
        model_name=gpt_engine_name
    )

# Initialize chat history in session state if not already present
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

def process_input(prompt):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.chat_history.append({"role": "user", "content": prompt})

    try:
        # Get response from LLM agent
        final_answer = ai_agent.llm(query=prompt, user_id=st.session_state.input_key)
        # Display bot's response in chat message container
        with st.chat_message("bot"):
            st.markdown(final_answer)
        # Add bot's response to chat history
        st.session_state.chat_history.append({"role": "bot", "content": final_answer})
    except Exception as e:
        st.error(f"Something went wrong: {e}")



# Directly capture user input
if query := st.chat_input("Ask your question here:"):
    process_input(query)

# Dummy element to trigger auto-scrolling
auto_scroll = st.empty()

# Trigger auto-scroll by adding an empty message after all other messages
with auto_scroll:
    st.write("") 
