import os
from openai import OpenAI
from pinecone import (
    Pinecone,
    ServerlessSpec,
    CloudProvider,
    AwsRegion,
    VectorType
)
from dotenv import load_dotenv
load_dotenv()
client = OpenAI()

pinecone_api_key = "PINECONE_API_KEY"
pinecone_env = "PINECONE_ENV"
pc = Pinecone()

index_config = pc.create_index(
    name="agent-interview",
    dimension=1536,
    spec=ServerlessSpec(
        cloud=CloudProvider.AWS,
        region=AwsRegion.US_EAST_1
    ),
    vector_type=VectorType.DENSE
)

index = pc.Index(host=index_config.host)

def embed_text(text: str):
    response = client.embeddings.create(
        input=text,
        model="text-embedding-3-small"
    )
    return response.data[0].embedding

def store_ideal_answer(question_id: str, text: str):
    vec = embed_text(text)
    index.upsert(vectors=[(question_id, vec)])

def find_similarity(user_answer: str):
    user_vec = embed_text(user_answer)
    result = index.query(
        vector=user_vec,
        top_k=1,
        include_values=False
    )
    # the closer to 1, the better
    similarity = result["matches"][0]["score"]
    return similarity