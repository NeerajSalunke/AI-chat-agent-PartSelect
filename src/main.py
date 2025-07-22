from fastapi import FastAPI, Request
from pydantic import BaseModel
from chromadb import PersistentClient
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
import os
from openai import OpenAI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import re
from langchain.memory import ConversationBufferMemory
from langchain.schema import HumanMessage, SystemMessage, AIMessage
from langchain_core.messages import get_buffer_string



load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
deepseek_api_key = os.getenv("DEEPSEEK_API_KEY")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserQuery(BaseModel):
    query: str

persist_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "chroma_db"))
embedding_func = OpenAIEmbeddingFunction(api_key=openai_api_key)
chroma_client = PersistentClient(path=persist_path)
collection = chroma_client.get_collection(name="partselect_parts", embedding_function=embedding_func)

#  deepseek api key
client = OpenAI(api_key=deepseek_api_key, base_url="https://api.deepseek.com")
memory = ConversationBufferMemory(return_messages=True)



@app.post("/api/ask")
async def ask_question(user_query: UserQuery):
    query = user_query.query
    part_number_match = re.search(r'\b[A-Z]{2,5}\d{5,}\b', query, re.IGNORECASE)

    if part_number_match:
        part_number = part_number_match.group(0).upper()
        print(f"Detected part number: {part_number}")
        
        
        results = collection.query(
            query_texts=[query],
            n_results=5,
            include=["documents"],
            where={"partSelect_number": part_number}
        )
    else:
        results = collection.query(
            query_texts=[query],
            n_results=5,
            include=["documents"]
        )


    docs = results["documents"][0]
    context = "\n\n".join(docs)

    memory.chat_memory.add_user_message(query)

    chat_history = memory.chat_memory.messages

    prompt = f"""
    You are an expert in appliance repair parts. Your job is to answer user questions clearly and helpfully based on the product and parts data below.

    Only include relevant information in your answers. Do not show internal data like cross-reference IDs, long lists, or technical codes unless asked specifically.

    If the user is asking about compatibility, installation steps, or part usage, provide a clear and friendly explanation. If there is a helpful video link available in the parts data, mention all the videos to the user.

    If a part number is mentioned, use it to locate the correct part and respond accordingly.
    Always check for exact part number matches if available.

    If user asks whether a part is compatible with a specific appliance or model number, check the part's product description and model cross reference to see if it's compatible.

    If multiple parts match the query, mention each briefly and help the user choose the most appropriate one.

    At the end of your answer, optionally suggest up to two related follow-up questions that are within your knowledge. These should be specific questions like:
    1. "Is this part compatible with [model]?"
    2. "How do I install this part?"
    3. "What symptoms does this part fix?"
    Do not suggest questions that cannot be answered from the given parts data or that require live customer support.

    If user asks about return policy, inform them that they can return the part within 365 days of purchase. Parts should be in re-sellable condition. Please allow 7-10 business days for the return to be processed.

    If user asks about warranty, inform them that they can get a 1-year warranty on the part.

    If user asks about shipping, inform them that we provide same day shipping on most parts.

    If user asks about payment, inform them that we accept all major credit cards and PayPal.

    Here is the parts information you can use:
    {context}

    User Question:
    {query}

    Answer:"""

    memory.chat_memory.add_user_message(prompt)

    messages = []
    for msg in memory.chat_memory.messages:
        role = "user" if msg.type == "human" else "assistant"
        messages.append({
            "role": role,
            "content": msg.content
        })


    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages
    )

    answer = response.choices[0].message.content.strip()
    memory.chat_memory.add_ai_message(answer)
    # print(answer)
    return {"role": "assistant", "content": answer}
