import requests


def get_status_code(url):
    try:
        response = requests.get(url)
        return response.status_code
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None


if __name__ == "__main__":
    url = input("Enter a URL: ")
    status_code = get_status_code(url)
    if status_code is not None:
        print(f"The status code for {url} is: {status_code}")
