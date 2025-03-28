from typing import Any

import requests
from joblib import Memory


@Memory(".cache", verbose=0).cache
def get_clients(php_session_id: str) -> list[dict[str, Any]]:
    url = "https://app.pantrysoft.com/client/client_index_data"

    cookies = {
        "PHPSESSID": f"{php_session_id}",
    }

    headers = {
        "accept": "application/json, text/javascript, */*; q=0.01",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        # 'cookie': '',
        "origin": "https://app.pantrysoft.com",
        "priority": "u=1, i",
        "referer": "https://app.pantrysoft.com/client/",
        "sec-ch-ua": '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
        "x-requested-with": "XMLHttpRequest",
    }

    params = {
        "specFilter": "client",
    }

    data = {
        "start": "0",
        "length": "100",
        "search[value]": "",
        "search[regex]": "false",
    }

    clients = []

    while True:
        # Make the request
        response = requests.post(
            url=url,
            params=params,
            cookies=cookies,
            headers=headers,
            data=data,
        )

        # Parse the response
        json_response = response.json()
        clients.extend(json_response["data"])

        # Check if there are more pages
        if json_response["recordsFiltered"] <= len(clients):
            break

        # Update the start parameter for the next request
        data["start"] = len(clients)
        data["length"] = "100"

    return [client["0"] for client in clients]
