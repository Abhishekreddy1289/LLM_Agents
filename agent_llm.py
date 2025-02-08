from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain_openai import ChatOpenAI
from datetime import datetime
from langchain.chat_models import init_chat_model
from config import *

class LLMAgent:
    def __init__(self, openai_type, model_name,api_key,azure_endpoint=None, api_version=None):
        
        if openai_type == 'azure_openai':
            self.model = AzureChatOpenAI(
                api_key=api_key,
                azure_endpoint=azure_endpoint,
                azure_deployment=model_name,
                openai_api_version=api_version
            )
        elif openai_type == "mistral":
            self.model=init_chat_model(model=model_name,api_key=api_key, model_provider="mistralai")
        else:
            self.model = ChatOpenAI(model=model_name,api_key=api_key)
        
        # Initialize Tavily search tool and memory saver
        self.tavily_search = TavilySearchResults(max_results=3)
        self.tools = [self.tavily_search]
        self.memory = MemorySaver()
        
        # Create the agent executor using react agent
        self.agent_executor = create_react_agent(self.model, self.tools, checkpointer=self.memory)
    def _system_prompt(self):
        today_date = datetime.today().strftime('%d-%m-%Y')
        prompt=f"""You are an advanced Assistant Chatbot equipped with access to real-time data. To ensure responses are accurate and pertinent, follow these steps carefully before replying to any user query:

1. If the query refers to a specific timeframe (e.g., today, yesterday, tomorrow), verify the current date and adjust your response accordingly.
2. Review the preceding interaction to fully understand the context before providing an answer.

Today's date: {today_date}"""
        return prompt
    def llm(self, query, user_id):
        if len(query) > 7:
            query=query[-7:]
        config = {"configurable": {"thread_id": user_id}}
        # Run the agent executor's stream method
        response_chunks = []
        messages=[{"role": "system", "content":self._system_prompt()}]
        for chunk in self.agent_executor.stream(
            {"messages": query}, config
        ):
            print(chunk)
            if 'agent' in chunk:
                # Proceed with accessing 'agent' related keys
                print(type(chunk['agent']['messages'][0].content))
                try:
                    answer=""
                    for i,text in enumerate(chunk['agent']['messages'][0].content):
                        if text["type"] == "text":
                            answer+=text["text"]
                    response_chunks.append(answer)
                except:
                    response_chunks.append(chunk['agent']['messages'][0].content)
            else:
                print("No 'agent' key found in the response.")

        
        return response_chunks[-1]
