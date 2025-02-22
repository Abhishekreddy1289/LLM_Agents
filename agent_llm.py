from langchain_community.tools.tavily_search import TavilySearchResults
from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec
from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from langchain_openai import ChatOpenAI
from datetime import datetime
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode
from langchain.chat_models import init_chat_model
from config import *

class Tools:
    def __call__(self):
        @tool
        def web_search(query: str):
            """This is web search technique to get real time data."""
            search = TavilySearchResults(max_results=3)
            search_results = search.invoke(query)
            return search_results

        @tool
        def index(query:str):
            """This Index contain user uploaded PDF data."""
            pc = Pinecone(api_key="pcsk_4hp8P_FGu8ZMCRX7gEjF1AH7ZTF3fv6V4uFyrTpNHkCidkvCofdF6LjR4QLwSZCpqSTGC")
            index = pc.Index("index1")
            query_embedding = pc.inference.embed(
                model="multilingual-e5-large",
                inputs=[query],
                parameters={
                    "input_type": "query"
                }
            )
            # Search the index for the three most similar vectors
            results = index.query(
                namespace="namespace1",
                vector=query_embedding[0].values,
                top_k=3,
                include_values=False,
                include_metadata=True
            )
            
            return results["matches"]
        tools = [index, web_search]
        # tool_node = ToolNode(tools)
        return tools

class LLMAgent:
    def __init__(self, tool:Tools, openai_type="mistral", model_name=None,api_key=None,azure_endpoint=None, api_version=None):
        self.openai_type=openai_type
        if openai_type == 'azure_openai':
            self.model = AzureChatOpenAI(
                api_key=api_key,
                azure_endpoint=azure_endpoint,
                azure_deployment=model_name,
                openai_api_version=api_version
            )
        elif openai_type == "openai":
            self.model = ChatOpenAI(model=model_name,api_key=api_key)
        else:
            self.model=init_chat_model(model="mistral-large-latest",api_key=mistral_api, model_provider="mistralai")
            
        self.tools = tool.__call__()
        self.memory = MemorySaver()
        
        # Create the agent executor using react agent
        self.agent_executor = create_react_agent(self.model, self.tools, checkpointer=self.memory)
    def _system_prompt(self):
        today_date = datetime.today().strftime('%d-%m-%Y')
        prompt=f"""You are an Advanced Mutli Agent Chatbot equipped with access to real-time data from web search and user upload data from vector database. To ensure responses are accurate and pertinent, follow these steps carefully before replying to any user query:

1. If the query refers to a specific timeframe (e.g., today, yesterday, tomorrow), verify the current date and adjust your response accordingly.
2. Review the preceding interaction to fully understand the context before providing an answer.

Today's date: {today_date}"""
        return prompt
    def llm(self, query, user_id):
        try:
            if len(query) > 5:
                query=query[-5:]
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
        except Exception as e:
            print("Error:",e)
            if self.openai_type == "openai":
                return "Please check Your OpenAI Credentials."
            elif self.openai_type == "azure_openai":
                return "Please check Your Azure OpenAI Credentials."
            else:
                return "There is High traffic in Mistral, Please try after sometime."
