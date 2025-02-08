import os

os.environ["TAVILY_API_KEY"] = "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"
os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_API_KEY"] = "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"

os.environ["OPENAI_API_KEY"] ="OpenAI key" #if use openai_type is OpenAI
os.environ["AZURE_OPENAI_API_KEY"] = "Azure OpenAI Key" #API key
os.environ["AZURE_OPENAI_ENDPOINT"]="Azure Base/Endpoint" #Endpoint
os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"]="gpt-4o" #model/deployment name 
os.environ["AZURE_OPENAI_API_VERSION"]="2023-07-01-preview"
os.environ["EMBEDDING_MODEL"]="text-embedding-ada-002"


api_key=os.environ["AZURE_OPENAI_API_KEY"]
azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"]
api_version=os.environ["AZURE_OPENAI_API_VERSION"]
model_name=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"]
embedding_model_name=os.environ["EMBEDDING_MODEL"]