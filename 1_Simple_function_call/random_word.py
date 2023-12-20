import requests


def get_random_word() -> str:
    response = requests.get("https://random-word-api.vercel.app/api?words=1")
    return response.json()[0]


if __name__ == "__main__":
    print(get_random_word())
