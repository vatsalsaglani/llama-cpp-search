from configs import BRAVE_API_KEY
import httpx


async def brave_search(search_term):
    brave_api_key = BRAVE_API_KEY
    url = f'https://api.search.brave.com/res/v1/web/search?q={search_term}&count=3'
    headers = {
        'X-Subscription-Token': brave_api_key,
        'Accept': 'application/json'
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            print('Search Data: ', data)
            return format_search(data)
        print(await response.text())
        return None


def format_search(search_results):
    retrieve_keys = ['web', 'news']
    formatted_results = []
    for value in retrieve_keys:
        if value in search_results:
            results = search_results[value]['results']
            formatted_results.append('\n'.join(
                f"Title: {result['title']} Description: {result['description']} URL: {result['url']}"
                for result in results))
    print('Formatted Results: ', formatted_results)
    if formatted_results:
        return '\n'.join(formatted_results)
    return None
