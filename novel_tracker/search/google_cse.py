# novel_tracker/search/google_cse.py
import requests

def google_search(query, api_key, cse_id, num=10):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        'q': query,
        'key': api_key,
        'cx': cse_id,
        'num': num
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        results = response.json().get('items', [])
        return [result['link'] for result in results][:num]
    except Exception as e:
        print(f"Search failed: {str(e)}")
        return []