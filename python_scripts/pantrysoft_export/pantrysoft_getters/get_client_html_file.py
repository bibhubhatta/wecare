import requests
from joblib import Memory


@Memory(".cache", verbose=0).cache
def get_client_dashboard_html_page(client_id: int, session_id: str) -> str:
    set_client_dashboard(client_id, session_id)

    url = "https://app.pantrysoft.com/client/dashboard/"

    cookies = {
        "PHPSESSID": session_id,
    }

    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "en-US,en;q=0.9",
        "priority": "u=0, i",
        "referer": "https://app.pantrysoft.com/client/",
        "sec-ch-ua": '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
        # 'cookie': 'PHPSESSID=ilkhu0vt8kdkdak4b1bl75m03d',
    }

    response = requests.get(url, cookies=cookies, headers=headers)

    if response.status_code != 200:
        raise Exception(
            f"Failed to get client dashboard HTML page: {response.status_code}"
        )
    return response.text


def set_client_dashboard(client_id: int, session_id: str) -> None:
    url = f"https://app.pantrysoft.com/client/dashboard/setclient/{client_id}"

    cookies = {
        "PHPSESSID": session_id,
    }

    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "en-US,en;q=0.9",
        "priority": "u=0, i",
        "referer": "https://app.pantrysoft.com/client/",
        "sec-ch-ua": '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "same-origin",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
        # 'cookie': 'PHPSESSID=ilkhu0vt8kdkdak4b1bl75m03d',
    }

    response = requests.get(url, cookies=cookies, headers=headers)

    if response.status_code not in (200, 302):
        raise Exception(f"Failed to set client dashboard: {response.status_code}")
