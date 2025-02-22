# Import the Pinecone library
from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec
import time
import PyPDF2
from langchain.text_splitter import RecursiveCharacterTextSplitter

class TextProcessor:
    def __init__(self, chunk_size=1000, chunk_overlap=20):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len,
            is_separator_regex=False,
        )
    def extract_text(self, file_path, file_name):
        try:
            reader = PyPDF2.PdfReader(file_path)
            docs=[]
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text = page.extract_text() if page.extract_text() else ""
                doc={"id":f"{file_name}-{int(page_num)+1}","text":text, "category": file_name}
                docs.append(doc)
            return docs
        except Exception as e:
            print(f"Error reading PDF file: {e}")
            raise Exception("Error in PDF reading")

class Indexing:
    def __init__(self,text_processor : TextProcessor):
        self.pc=Pinecone(api_key="pcsk_4hp8P_FGu8ZMCRX7gEjF1AH7ZTF3fv6V4uFyrTpNHkCidkvCofdF6LjR4QLwSZCpqSTGC")
        self.index_name = "index1"
        self.doc_processing=text_processor
        self.__call__()

    def __call__(self):
        existing_indexes = [index_info["name"] for index_info in self.pc.list_indexes()]
        if self.index_name not in existing_indexes:
            self.pc.create_index(
                name=self.index_name,
                dimension=1024,
                metric="cosine",
                spec=ServerlessSpec(
                    cloud="aws", 
                    region="us-east-1"
                ) 
            ) 
        # Wait for the index to be ready
        while not self.pc.describe_index(self.index_name).status['ready']:
            time.sleep(1)

    def embedding(self,docs):
        embeddings = self.pc.inference.embed(
                        model="multilingual-e5-large",
                        inputs=[d["text"] for d in docs],
                        parameters={
                            "input_type": "passage", 
                            "truncate": "END"
                        }
                    )
        return embeddings
    
    def insert_doc(self,file_path, file_name):

        index = self.pc.Index(self.index_name)
        records = []
        docs=self.doc_processing.extract_text(file_path, file_name)
        embeddings=self.embedding(docs)
        for d, e in zip(docs, embeddings):
            records.append({
                "id": d["id"],
                "values": e["values"],
                "metadata": {
                    "source_text": d["text"],
                    "category": d["category"]
                }
            })

        index.upsert(
            vectors=records,
            namespace="namespace1"
        )
        time.sleep(10)
        return index.describe_index_stats()

