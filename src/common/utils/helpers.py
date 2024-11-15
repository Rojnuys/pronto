import requests


def fetch_pic(url: str = "https://picsum.photos/800/500") -> str:
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        raise Exception("Something went wrong")
