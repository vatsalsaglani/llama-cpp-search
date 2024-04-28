from brave_search import brave_search
from llm_invoke import LLM

print(f"Loading LLM")
llm = LLM("./model/Phi-3-mini-4k-instruct-q4.gguf")
# llm = LLM("./model/Meta-Llama-3-8B-Instruct-IQ3_M.gguf")
print(f"Loaded LLM")


# bs = BraveSearch()
async def search(query: str):
    prompt = "You are a helpful news summary agent. You are provided with user query in single backticks and reterieved search results in triple backticks. There will be multiple search results and each result will contain a title and a description. Using all the title and description you have to summarize the news for the query in simple concise terms with citations of urls if the search results are relevant. When you have a variety of relevant results please answer in bullet points with only citation for each. Note: Please provide the citations in markdown format and for one topic provide only one citation even if there are multiple URLs."
    search_items = await brave_search(query)
    messages = [{
        "role": "system",
        "content": prompt
    }, {
        "role":
        "user",
        "content":
        f"Query: `{query}` \n\n Search Results: ```{search_items}```"
    }]
    for content in llm.__stream__(messages, max_tokens=512):
        yield content
