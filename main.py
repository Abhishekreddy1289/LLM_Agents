import streamlit as st
from agent_llm import LLMAgent
import time
from config import api_version

# List of recommended questions
recommended_questions = [
    "What is the refund process for failed reservations, and which charges may be forfeited?",
    "How are cancellation charges calculated for confirmed tickets based on time and class?",
    "How is a refund processed for a party e-ticket with mixed confirmed and RAC/waitlisted passengers?"
]


st.set_page_config(page_title="Abhi Search Engine using LLM Agent", layout="wide")
st.title("🧠Advanced LLM Agent Bot")
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
if 'input_key' not in st.session_state: 
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

display_modal()

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

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

def process_input(prompt):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    try:
        final_answer = ai_agent.llm(query=st.session_state.chat_history, user_id=st.session_state.input_key)
        
        with st.chat_message("bot"):
            st.markdown(final_answer)
        
        st.session_state.chat_history.append({"role": "assistant", "content": final_answer})
    except Exception as e:
        st.error(f"Something went wrong: {e}")

# Display recommended questions as buttons
if not st.session_state.chat_history:
    st.write("**Recommended Questions:**")
    cols = st.columns(len(recommended_questions))
    for i, question in enumerate(recommended_questions):
        if cols[i].button(question):
            process_input(question)

# Directly capture user input
if query := st.chat_input("Ask your question here:"):
    process_input(query)

# Dummy element to trigger auto-scrolling
auto_scroll = st.empty()

# Trigger auto-scroll by adding an empty message after all other messages
with auto_scroll:
    st.write("") 
