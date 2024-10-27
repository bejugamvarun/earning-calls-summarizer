from dotenv import load_dotenv
import logging
import os
from pinecone import Pinecone, ServerlessSpec
from langchain_openai.embeddings import OpenAIEmbeddings
from earnings_calls_fetcher import get_earnings_call_transcript
from fastapi import HTTPException

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,  # Set to DEBUG for more detailed logs
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler()  # This ensures logs are printed to the console
    ]
)

logger = logging.getLogger(__name__)

load_dotenv()

# Initialize Pinecone using the new class-based approach
pc = Pinecone(
    api_key=os.getenv("PINECONE_API_KEY")  # You can use environment variables for the API key
)

index_name = "earnings-calls"

# Check if the index exists, if not, create it
if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=1536,
        metric='euclidean',
        spec=ServerlessSpec(
            cloud='aws',
            region='us-east-1'  # Set your appropriate region
        )
    )

index = pc.Index(index_name)  # Get the index object

# Set up the OpenAI Embeddings model
embeddings_model = OpenAIEmbeddings()


def store_transcript_in_pinecone(transcripts, company_name):
    """
    Store the combined transcript embeddings in Pinecone under one unique key (company_name).
    - transcripts: A dictionary containing the quarterly transcripts.
    - company_name: The unique key under which to store the embeddings.
    """
    # Concatenate the transcripts into one string
    combined_transcript = " ".join(transcripts.values())

    # Vectorize the combined transcript
    vector = embeddings_model.embed_query(combined_transcript)

    # Store the combined embedding in Pinecone with metadata
    index.upsert(vectors=[{
        "id": company_name,  # Store everything under one key (the company name)
        "values": vector,
        "metadata": {
            "company_name": company_name,
            "quarters": list(transcripts.keys()),  # Store the quarters in metadata
            "transcripts": transcripts  # Optionally, store the original transcripts in metadata
        }
    }])
    
    return f"Combined transcript for {company_name} stored in Pinecone."


# Example function to fetch transcripts and store in Pinecone
def summarize_and_store(company_name, year):
    """
    Fetch transcripts, store embeddings, and summarize the data.
    """
    try:
        # Step 1: Fetch earnings call transcripts for all quarters
        transcripts = {}
        for quarter in range(1, 5):  # Q1 to Q4
            earnings_data = get_earnings_call_transcript(company_name, year, quarter)
            if earnings_data:
                transcripts[f"Q{quarter}"] = earnings_data
            else:
                transcripts[f"Q{quarter}"] = "No data available for this quarter."
        
        # Step 2: Store the transcripts as embeddings in Pinecone
        store_transcript_in_pinecone(transcripts, f"{company_name}_{year}")

        return transcripts

    except Exception as e:
        logger.error(f"Error summarizing earnings for {company_name}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
