from brave_search import brave_search
from llm_invoke import LLM

print(f"Loading LLM")
llm = LLM("./model/Phi-3-mini-4k-instruct-q4.gguf")
# llm = LLM("./model/Meta-Llama-3-8B-Instruct-IQ3_M.gguf")
print(f"Loaded LLM")


# bs = BraveSearch()
async def search(query: str):
    prompt = "You are a helpful news summary agent. You are provided with user query in single backticks and reterieved search results in triple backticks. There will be multiple search results and each result will contain a title and a description. Using all the title and description you have to summarize the news for the query in simple concise terms with citations of urls if the search results are relevant. If the search results are not relevant you can politely reply that you cannot help. Once you are done with your answer return </done>. When you have a variety of relevant results please answer in bullet points with only citation for each. Note: Please provide the citations in markdown format and for one topic provide only one citation even if there are multiple URLs."
    search_items = await brave_search(query)
    # results = """## Search Results:\n\n"""
    # results += "\n".join([
    #     f"Title: {r.get('title')} Description: {r.get('description')} URL: {r.get('url')}"
    #     for r in search_items
    # ])
    messages = [{
        "role": "system",
        "content": prompt
    }, {
        "role":
        "user",
        "content":
        f"Query: `{query}` \n\n Search Results: ```{search_items}```"
    }]
    # print("MESSAGES: ", messages)
    for content in llm.__stream__(messages, stop=["</done>"], max_tokens=512):
        yield content
