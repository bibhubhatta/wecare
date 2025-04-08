import time

import requests


def get_items(session_id: str) -> str:
    url = "https://app.pantrysoft.com/inventoryitem/indexdata"

    cookies = {
        "PHPSESSID": session_id,
    }

    headers = {
        "accept": "text/html, */*; q=0.01",
        "accept-language": "en-US,en;q=0.9",
        "priority": "u=1, i",
        "referer": "https://app.pantrysoft.com/client/dashboard/",
        "sec-ch-ua": '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
        "x-requested-with": "XMLHttpRequest",
        # 'cookie': 'PHPSESSID=vov09qjcp00ncjddflt1c1vrjl',
    }

    params = {"_": str(int(time.time() * 1000))}

    response = requests.get(
        url=url,
        cookies=cookies,
        headers=headers,
        params=params,
    )

    if response.status_code != 200:
        raise Exception(f"Failed to get items: {response.status_code}")

    return response.json()["data"]
