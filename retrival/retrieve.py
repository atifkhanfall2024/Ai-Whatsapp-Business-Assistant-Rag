
def RetrivalPhase(Query):
 from langchain_google_genai import GoogleGenerativeAIEmbeddings
 from dotenv import load_dotenv
 import os
 from langchain_qdrant import QdrantVectorStore
 from openai import OpenAI

 load_dotenv()
 Key = os.getenv("GOOGLE_API_KEY")
 if not Key:
  raise ValueError('Key is not present')
 
 client = OpenAI(
    api_key=Key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)


 embeddings = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-001",
    api_key=Key
 )

 vector = QdrantVectorStore.from_existing_collection(
   collection_name="whatsapp_assistant",
     embedding=embeddings,
     url="http://localhost:6333/",
     
 )

 # simliarity search

 Similarity_search=vector.similarity_search(query=Query , k=3)

# this will return relevent chunks now interacting with llm 
 context = "\n\n\n".join([f"{output.page_content}" for output in Similarity_search ])

 System_Prompt=f"""
  you are a helpful ai whatsapp business assistant  , you will give only the answer related to the data do you have in rag . if data not present with you then tell please contact with owner . 
  Also you need to talk only in postive way , not not talk something elase.
  also answer according to the data that provide to you.
  on first message from user you if he talk in english or urdu you give answer according to that .
  only on the first message of user you say Assalam o alekm Sir . 
  on every message you need to talk with customer in polite way like
  example: 
  Question from user : hi can you place my order
  your answer : yes sir mean on every message use the word sir as well with message to attract customer
  in context below this is the relevent chunks from rag:
  {context}


"""
 response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {"role":"system"  , "content":System_Prompt},
        {"role":"user"  , "content":Query}
    ]
    )

 print(" Response :> " +response.choices[0].message.content  )
 return response.choices[0].message.content