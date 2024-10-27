from langchain.chains import LLMChain
from langchain_community.llms import OpenAI
from langchain.prompts import PromptTemplate
from pinecone_module import embeddings_model, index

def retrieve_and_summarize(company_name):
    # Generate query vector based on the company name
    query_vector = embeddings_model.embed_query(company_name)  # Updated to use embed_query
    
    # Search Pinecone for similar embeddings
    query_response = index.query(queries=[query_vector], top_k=5, include_metadata=True)
    
    # Extract transcripts from the metadata
    transcripts = [match["metadata"]["transcript"] for match in query_response["matches"]]
    
    if not transcripts:
        return f"No transcripts found for {company_name}"
    
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
