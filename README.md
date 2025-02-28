# LLM Agent Chatbot - Real-Time Query Handler

This project demonstrates a basic chatbot built using LLM (Large Language Model) agents that can process real-time queries. The chatbot provides real-time responses to user queries such as weather updates or market prices using an internal agent that interacts with various APIs to fetch the required data. In this specific example, it integrates with a tool called "Tavily Search" to fetch information based on user requests.

The project can be deployed using **FastAPI** (for API-based interactions) or **Streamlit** (for a user-friendly web interface).

## Features
- **Real-Time Queries:** Handle real-time queries such as "What is the weather in Bangalore?" or "What is the gold price in Bangalore today?"
- **Internal LLM Agent:** Uses a customizable LLM Agent to process user queries and fetch real-time data.
- **Multi-Platform Access:**
  - **FastAPI** (via an API endpoint) for backend integration.
  - **Streamlit** for a simple user interface to interact with the chatbot.

## Prerequisites
Before running the project, ensure you have the following:
- Python 3.8+
- API Keys and relevant configuration data for services like OpenAI or Azure OpenAI.
- The `agent_llm` module and `Tavily Search` integration.

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Abhishekreddy1289/LLM_Agents.git
   ```

2. **Install dependencies:**

   Make sure you have `FastAPI`, `Streamlit`, and other required dependencies installed. You can install them using `pip`:

   ```bash
   pip install -r requirements.txt
   ```

   This file should include:
   - fastapi
   - streamlit
   - openai (or azure-openai depending on your service)
   - any other dependencies used in your agent

3. **Configure API Details:**
   
   Set your `api_key`, `model_name`, `openai_type`, `azure_endpoint`, and `api_version` in the configuration file (`config.py`) or directly in the Streamlit app.

## Project Structure

```plaintext
.
├── agent_llm.py            # LLM Agent definition and logic
├── config.py               # API keys and configuration settings
├── app.py          # FastAPI app for API-based interaction
├── main.py        # Streamlit app for user interface
├── requirements.txt        # List of required Python packages
├── README.md               # Project documentation
```

## Usage

### 1. FastAPI Integration (API)

To use the chatbot through **FastAPI**:

- Ensure your API keys and configuration details are correctly set up in `config.py`.
- Run the FastAPI app by executing:

   ```bash
   uvicorn app:app --reload
   ```

- This will start the FastAPI server, and you can interact with the chatbot by sending `POST` requests to:

   ```
   POST http://127.0.0.1:8000/interaction/{id}
   ```

   - The body of the request should include a `query` field with the user's query.

   Example request body:
   ```json
   {
     "query": "What is the weather in Bangalore?"
   }
   ```

### 2. Streamlit Interface (UI)

To use the chatbot with **Streamlit**:

1. Run the Streamlit app by executing:

   ```bash
   streamlit run main.py
   ```

2. This will launch a local web interface where you can:
   - Select your service (OpenAI or Azure OpenAI).
   - Provide your API keys and model details.
   - Start chatting with the bot.

   You will see your chat history, and the chatbot will generate responses to your real-time queries.

### Example Interaction

Once you’ve set up the interface:

1. A user can ask questions like:
   - "What is the weather in Bangalore right now?"
   - "What is the gold price in Bangalore today?"

2. The LLM agent internally uses the configured tools (like "Tavily Search") to search for the most relevant information, processes the query, and generates an appropriate response.

3. The chatbot then provides a response based on the real-time data gathered.

### Configuration Options

You can configure the following details:

- **Service Type:** Choose between "OpenAI" and "Azure OpenAI".
- **API Key:** Enter your API key for the selected service.
- **Model Name:** Specify the model name (e.g., `gpt-4o`).
- **User Name/ID:** Optionally provide a user identifier.
- **Endpoint and Version (for Azure):** Provide Azure OpenAI endpoint and version information.

## How the LLM Agent Works

The **LLM Agent** is a core component that handles queries and interacts with external tools like Tavily Search:

- When a user inputs a query, the chatbot sends this query to the **LLM Agent**.
- The **LLM Agent** internally processes the query by:
  - Using APIs or internal tools (like Tavily Search) to fetch real-time information.
  - Generating a response using the large language model (GPT or similar).
- The response is then sent back to the user through the chatbot interface.

## Error Handling

- If the API or agent encounters any issues, an error message will be displayed on the Streamlit interface.
- If the FastAPI service experiences an error, a 500 Internal Server Error will be returned with the message `"Internal Server Error"`.

## Contributing

Feel free to fork the repository, open issues, and submit pull requests to improve the project. If you'd like to contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-name`).
3. Make your changes and commit them (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature-name`).
5. Open a pull request to merge your changes.

## License

This project is open source and available under the [MIT License](LICENSE).
