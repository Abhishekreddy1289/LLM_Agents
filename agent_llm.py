from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain_openai import ChatOpenAI

class LLMAgent:
    def __init__(self, openai_type, model_name,api_key,azure_endpoint=None, api_version=None):
        
        if openai_type == 'azure_openai':
            self.model = AzureChatOpenAI(
                api_key=api_key,
                azure_endpoint=azure_endpoint,
                azure_deployment=model_name,
                openai_api_version=api_version
            )
        else:
            self.model = ChatOpenAI(model=model_name,api_key=api_key)
        
        # Initialize Tavily search tool and memory saver
        self.tavily_search = TavilySearchResults(max_results=3)
        self.tools = [self.tavily_search]
        self.memory = MemorySaver()
        
        # Create the agent executor using react agent
        self.agent_executor = create_react_agent(self.model, self.tools, checkpointer=self.memory)
    
    def llm(self, query, user_id):
        if len(query) > 7:
            query=query[-7:]
        config = {"configurable": {"thread_id": user_id}}
        # Run the agent executor's stream method
        response_chunks = []
        for chunk in self.agent_executor.stream(
            {"messages": query}, config
        ):
            if 'agent' in chunk:
                # Proceed with accessing 'agent' related keys
                print(chunk['agent']['messages'][0].content)
                response_chunks.append(chunk['agent']['messages'][0].content)
            else:
                print("No 'agent' key found in the response.")

        
        return response_chunks[-1]

