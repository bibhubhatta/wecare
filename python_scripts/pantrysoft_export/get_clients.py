from typing import Any

import requests
from joblib import Memory


@Memory("cache", verbose=0).cache
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
        "draw": "2",
        "columns[0][data]": "clientId",
        "columns[0][name]": "clientId",
        "columns[0][searchable]": "true",
        "columns[0][orderable]": "true",
        "columns[0][search][value]": "",
        "columns[0][search][regex]": "false",
        "columns[1][data]": "locationName",
        "columns[1][name]": "locationName",
        "columns[1][searchable]": "true",
        "columns[1][orderable]": "true",
        "columns[1][search][value]": "",
        "columns[1][search][regex]": "false",
        "columns[2][data]": "deliveryRoute",
        "columns[2][name]": "deliveryRoute",
        "columns[2][searchable]": "true",
        "columns[2][orderable]": "true",
        "columns[2][search][value]": "",
        "columns[2][search][regex]": "false",
        "columns[3][data]": "locationCounty",
        "columns[3][name]": "locationCounty",
        "columns[3][searchable]": "true",
        "columns[3][orderable]": "true",
        "columns[3][search][value]": "",
        "columns[3][search][regex]": "false",
        "columns[4][data]": "accountNumber",
        "columns[4][name]": "accountNumber",
        "columns[4][searchable]": "true",
        "columns[4][orderable]": "true",
        "columns[4][search][value]": "",
        "columns[4][search][regex]": "false",
        "columns[5][data]": "businessName",
        "columns[5][name]": "businessName",
        "columns[5][searchable]": "true",
        "columns[5][orderable]": "true",
        "columns[5][search][value]": "",
        "columns[5][search][regex]": "false",
        "columns[6][data]": "firstName",
        "columns[6][name]": "firstName",
        "columns[6][searchable]": "true",
        "columns[6][orderable]": "true",
        "columns[6][search][value]": "",
        "columns[6][search][regex]": "false",
        "columns[7][data]": "lastName",
        "columns[7][name]": "lastName",
        "columns[7][searchable]": "true",
        "columns[7][orderable]": "true",
        "columns[7][search][value]": "",
        "columns[7][search][regex]": "false",
        "columns[8][data]": "birthday",
        "columns[8][name]": "birthday",
        "columns[8][searchable]": "true",
        "columns[8][orderable]": "true",
        "columns[8][search][value]": "",
        "columns[8][search][regex]": "false",
        "columns[9][data]": "status",
        "columns[9][name]": "status",
        "columns[9][searchable]": "true",
        "columns[9][orderable]": "true",
        "columns[9][search][value]": "",
        "columns[9][search][regex]": "false",
        "columns[10][data]": "streetAddress",
        "columns[10][name]": "streetAddress",
        "columns[10][searchable]": "true",
        "columns[10][orderable]": "true",
        "columns[10][search][value]": "",
        "columns[10][search][regex]": "false",
        "columns[11][data]": "unitNo",
        "columns[11][name]": "unitNo",
        "columns[11][searchable]": "true",
        "columns[11][orderable]": "true",
        "columns[11][search][value]": "",
        "columns[11][search][regex]": "false",
        "columns[12][data]": "phoneNumber",
        "columns[12][name]": "phoneNumber",
        "columns[12][searchable]": "true",
        "columns[12][orderable]": "true",
        "columns[12][search][value]": "",
        "columns[12][search][regex]": "false",
        "order[0][column]": "7",
        "order[0][dir]": "asc",
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
