import os
from dotenv import load_dotenv
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_qdrant import QdrantVectorStore



load_dotenv()
Key= os.getenv("GOOGLE_API_KEY")
if not Key:
     print("Key is not present")
pdf_path = Path("Smart_Bites_RAG_Menu.pdf").resolve()
if not pdf_path :
    print('error to find pdf path')
else:
     print("PDF found at:", pdf_path)

loader = PyPDFLoader(pdf_path)
docs = loader.load()
#print(docs[0])

# make chunks

chunks = RecursiveCharacterTextSplitter(chunk_size=300,
    chunk_overlap=100)
text = chunks.split_documents(docs)


# convert that chunks into enbeddings

embeddings = GoogleGenerativeAIEmbeddings(
        model="gemini-embedding-001",
        api_key=Key
    )

# now store in vector db

Vector = QdrantVectorStore.from_documents(
     collection_name="whatsapp_assistant",
     embedding=embeddings,
     url="http://localhost:6333/",
     documents=text
     
)

print('Data Success Store in Vector Db')
