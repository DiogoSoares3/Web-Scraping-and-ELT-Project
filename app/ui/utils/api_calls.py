import requests


def fetch_data_from_api(api_url: str):
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.HTTPError as err:
        print(f"HTTP Error occurred: {err}")
    except requests.exceptions.RequestException as err:
        print(f"Error occurred: {err}")
        
    return []
