import json
import chromadb
import os
from chromadb.config import Settings
from chromadb import PersistentClient
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
from dotenv import load_dotenv


load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables")

persist_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "chroma_db"))
print("Persist path:", persist_path)
if not os.path.exists(persist_path):
    os.makedirs(persist_path)

with open("data2.json", encoding="utf-8") as f:
    parts_data = json.load(f)

chroma_client = PersistentClient(path=persist_path)

embedding_function = OpenAIEmbeddingFunction(api_key=openai_api_key)

collection = chroma_client.get_or_create_collection(
    name="partselect_parts",
    embedding_function=embedding_function
)

documents = []
ids = []
metadatas = []

for idx, part in enumerate(parts_data):
    print(f"Ingesting: {part['partSelect_number']}")  # Debug line
    part_text = f"""
    PartSelect Number: {part['partSelect_number']}
    Manufacturer Number: {part['manufacturer_number']}
    Brand: {part['brand']}
    Can Also Be Used With Brands: {', '.join(part['can_be_used_with_brands'])}
    Product Type: {part['for_product']}
    Cost: {part['cost']}
    Product Description: {part['product_description']}
    Model Cross Reference: {', '.join(part['model_cross_reference'])}
    Fixes Symptoms: {', '.join(part['fixes_symptoms'])}
    Similar To: {', '.join(part['similar_to'])}
    Videos: {', '.join(part['videos'])}
    """

    documents.append(part_text)
    ids.append(part["partSelect_number"])  # unique ID
    metadatas.append({  # for filtering or lookup
        "brand": part["brand"],
        "product_type": part["for_product"]
    })

collection.add(
    documents=documents,
    metadatas=metadatas,
    ids=ids
)

# chroma_client.persist()

print("Parts successfully added to vector DB!")
