# /// script
# requires-python = ">=3.13"
# dependencies = ["requests"]
# ///


import csv
import requests
import json

BASE_URL = (
    "https://storefrontgateway.shoprite.com/api/stores/3000/categories/520625/search"
)
PARAMS = {
    "take": 50,
    "skip": 0,
    "sort": "brand",
    "f": "Breadcrumb:grocery/pantry/canned & packaged foods",
}
HEADERS = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-US,en;q=0.9",
    "cookie": "__cf_bm=8s9pS4JKGHQjjcYjjCTuty.AKTHpCA7ZS5Kv3eXYbn0-1738349967-1.0.1.1-qiXb7itFXyAsJCmoPKsRrjF.RDKx2XTHJExRiEFYBWCy0DsP_Fap3P4TCkTDSr3k9_K9cd2HdvMlzU._dNpGH4jpweLgiL0R3q5sRdEvtP8; __cfruid=b1546f84d805b17071c094727df55dc106db7a4a-1738349967; fw_se={%22value%22:%22fws2.6050b16c-7b4d-4de0-a89a-eb315b1030a5.1.1738349968808%22%2C%22createTime%22:%222025-01-31T18:59:28.809Z%22}; cf_clearance=4NfdI64U_U32Dx9IdAK9RX_lvnvaOg_ymNy0uPrzIQM-1738349968-1.2.1.1-31uhVF0TUEZKR1uuU8Hg_UdpVQTBCTRZAasfTk1bVYn4b34o1qTqYix7VWZwRwukgqjRZgrxr6BZMfr7Bqqm.If54IZs1wiFuw.2CSNB2.Ae6t.6sMadY0jC.muZuzEcEv19odD5GgFZ7Km6Tmugk9qeIhZCa2JcWM2BJ7LGRrRlQ_.8QGB7OXuX2WczRNagpf24C4qSR1_dyj5EGgN9JwDwe0pnLAZ5iCQwYkrBr3VuWVHbiSKBN_HNtQnsLvopFPdzMdmauOm4CZC.y65edNllzgnqu4BGWO9blmJzRpg; OptanonAlertBoxClosed=2025-01-31T18:59:34.719Z; fw_uid={%22value%22:%22105a3b71-64cf-4d64-9c6b-ccc6da48a752%22%2C%22createTime%22:%222025-01-31T18:59:39.024Z%22}; OptanonConsent=isGpcEnabled=0&datestamp=Fri+Jan+31+2025+14%3A01%3A24+GMT-0500+(Eastern+Standard+Time)&version=202409.2.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=208edb56-6baf-4be6-b1b0-673ac7f9e7d7&interactionCount=1&isAnonUser=1&landingPath=NotLandingPage&groups=C0003%3A1%2CC0001%3A1%2CC0004%3A0%2CC0002%3A0%2CC0005%3A0&intType=2&geolocation=US%3BNJ&AwaitingReconsent=false; __cf_bm=jlOdybrjVMUkm7mHdUItYyMUK2NbSPqrHBd7gX15km8-1738354237-1.0.1.1-F8Pna6OI.wHLHlm.01FROWFvDeqJeb0oj1WFAl0boWxnXt9Ewzsg1A7c.69LYNXmCvVMCQD50pZjWRqoBOrYSh7aXjIfagAilu6E2JPUBfk",
    "dnt": "1",
    "origin": "https://www.shoprite.com",
    "priority": "u=1, i",
    "referer": "https://www.shoprite.com/",
    "sec-ch-ua": '"Not A(Brand";v="8", "Chromium";v="132"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36",
    "x-correlation-id": "af4a3e16-217e-43eb-96b0-4dd57b4cc4cc",
    "x-customer-session-id": "https://www.shoprite.com|150d7af6-26e0-47e9-8d90-89c8dfcd6ebe",
    "x-shopping-mode": "11111111-1111-1111-1111-111111111111",
    "x-site-host": "https://www.shoprite.com",
    "x-site-location": "HeadersBuilderInterceptor",
}


def fetch_products():
    # Check if products cache exists
    try:
        with open("products-cache.json", mode="r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        pass

    all_items = []
    while True:
        response = requests.get(BASE_URL, params=PARAMS, headers=HEADERS)
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            break

        data = response.json()
        items = data.get("items", [])
        all_items.extend(items)

        # Pagination handling
        pagination = data.get("pagination", {}).get("_links", {}).get("next", {})
        if not pagination:
            break

        PARAMS["skip"] += PARAMS["take"]

    # Save products to cache
    with open("products-cache.json", mode="w", encoding="utf-8") as file:
        json.dump(all_items, file)

    return all_items


def add_can_status(products):
    # load old products data with can status
    old_products = []
    with open("products-can_filtered.csv", mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        old_products = list(reader)

    # create a dictionary of old products
    old_products_dict = {int(product["productID"]): product for product in old_products}
    
    # add can status to new products
    for product in products:
        product_id = int(product.get("productId", ""))
        if product_id in old_products_dict:
            product["status"] = old_products_dict[product_id].get("status", "")

    return products


def save_to_csv(products, filename="products.csv"):
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(
            ["productID", "name", "description", "price", "weight", "weightUnit", "image", "imageUrl", "can"]
        )
        for product in products:
            writer.writerow(
                [
                    product.get("productId", ""),
                    product.get("name", ""),
                    product.get("description", ""),
                    product.get("price", ""),
                    product.get("unitOfSize", {}).get("size", ""),
                    product.get("unitOfSize", {}).get("abbreviation", ""),
                    "",
                    product.get("image", {}).get("default", ""),
                    product.get("status", ""),
                ]
            )


if __name__ == "__main__":
    print("Fetching products...")
    products = fetch_products()
    print(f"Fetched {len(products)} products")

    print("Adding can status to products...")
    products = add_can_status(products)

    print("Saving products to CSV...")
    save_to_csv(products)
    print(f"Saved {len(products)} products to products.csv")
