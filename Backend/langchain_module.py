from langchain.chains import LLMChain
from langchain_community.llms import OpenAI
from langchain.prompts import PromptTemplate
from pinecone_module import index

def retrieve_and_summarize(company_name, year):
    """
    Retrieve all embeddings for a company in a given year and summarize them.
    """
    try:
        # Query Pinecone for all embeddings related to the company in the given year
        query_response = index.query(
            filter={"company_name": company_name, "year": year},
            top_k=10,  # Adjust this based on the number of quarters stored
            include_metadata=True
        )
        
        # Extract transcripts from the metadata
        transcripts = [match["metadata"]["transcript"] for match in query_response["matches"]]
        
        if not transcripts:
            return f"No transcripts found for {company_name} in {year}"
        
        # Combine all retrieved transcripts into one string for summarization
        full_transcript = " ".join(transcripts)
        
        # Define an LLM with Langchain (OpenAI in this case)
        llm = OpenAI(temperature=0.7)
        
        # Prompt template for summarization
        prompt_template = """
        You are a financial analyst. Here is a set of earnings call transcripts for the company. Summarize the key points and provide insights on the company's performance:

        {transcript}
        """
        
        prompt = PromptTemplate(input_variables=["transcript"], template=prompt_template)
        chain = LLMChain(llm=llm, prompt=prompt)
        
        # Run the LLM to summarize the concatenated transcript
        summary = chain.run(transcript=full_transcript)
        
        return summary

    except Exception as e:
        return f"Error retrieving or summarizing transcripts for {company_name}: {str(e)}"