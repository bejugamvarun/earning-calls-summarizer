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
embeddings_model = OpenAIEmbeddings(model="text-embedding-3-small")


def store_quarterly_embeddings(company_name, year, transcripts):
    """
    Store the earnings call embeddings for each quarter of a company in Pinecone.
    - transcripts: A dictionary containing transcripts for each quarter.
    - company_name: The company's name (e.g., "AAPL").
    - year: The year of the earnings call (e.g., 2024).
    """
    try:
        # Prepare vectors for each quarter
        pinecone_vectors = []
        for quarter, transcript in transcripts.items():
            if transcript != "No data available for this quarter.":
                # Generate embedding for the transcript
                vector = embeddings_model.embed_query(transcript)
                # Create a unique ID for each quarter
                record_id = f"{company_name}_{year}_Q{quarter}"
                # Prepare the vector data for upsertion
                pinecone_vectors.append({
                    "id": record_id,
                    "values": vector,
                    "metadata": {
                        "company_name": company_name,
                        "year": year,
                        "quarter": f"Q{quarter}",
                        "transcript": transcript
                    }
                })

        # Upsert all vectors in a batch to Pinecone
        if pinecone_vectors:
            index.upsert(vectors=pinecone_vectors)
            logger.info(f"Stored embeddings for {company_name} for year {year}")
        else:
            logger.warning(f"No valid transcripts to store for {company_name} in {year}")
    
    except Exception as e:
        logger.error(f"Error storing embeddings for {company_name}: {str(e)}")

def summarize_and_store(company_name, year):
    """
    Fetch transcripts for all quarters, store embeddings, and return the transcripts.
    """
    try:
        transcripts = {}
        for quarter in range(1, 5):  # Q1 to Q4
            earnings_data = get_earnings_call_transcript(company_name, year, quarter)
            if earnings_data:
                transcripts[quarter] = earnings_data
            else:
                transcripts[quarter] = "No data available for this quarter."

        # Store the embeddings for each quarter
        store_quarterly_embeddings(company_name, year, transcripts)

    except Exception as e:
        logger.error(f"Error fetching or storing data for {company_name}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
