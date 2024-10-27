import logging
import uvicorn
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_module import retrieve_and_summarize
from pinecone_module import summarize_and_store
from typing import List
import time

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,  # Set to DEBUG for more detailed logs
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler()  # This ensures logs are printed to the console
    ]
)

logger = logging.getLogger(__name__)

app = FastAPI()

# Add CORS middleware to allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class EarningsRequest(BaseModel):
    company_name: str
    year: int

class ComparativeRequest(BaseModel):
    company_names: List[str]
    year: int

# Add custom middleware to log request details
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    logger.debug(f"Start request: {request.method} {request.url.path}")
    
    # Process the request
    response = await call_next(request)

    process_time = time.time() - start_time
    logger.debug(f"Completed request: {request.method} {request.url.path} in {process_time:.4f} seconds with status {response.status_code}")
    
    return response

@app.post("/summarize/")
async def summarize_earnings(request: EarningsRequest):
    try:
        # Store and summarize the earnings for the whole year
        summarize_and_store(request.company_name, request.year)
        summary = retrieve_and_summarize(request.company_name, request.year)
        return {"message": summary}
    except Exception as e:
        logger.error(f"Error summarizing earnings for {request.company_name}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/compare/")
async def compare_earnings(request: ComparativeRequest):
    comparative_report = {}
    try:
        for company in request.company_names:
            summarize_and_store(company, request.year)
            comparative_report[company] = retrieve_and_summarize(company, request.year)
        return {"comparative_report": comparative_report}
    except Exception as e:
        logger.error(f"Error comparing earnings: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(
        "app:app", 
        host="0.0.0.0", 
        port=8000, 
        # reload=True,
        log_level="trace", 
        access_log=True
    )