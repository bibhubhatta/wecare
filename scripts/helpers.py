def get_detailed_description(shoprite_item_json: dict) -> str:
    """
    Get a detailed description for the item.

    Parameters:
    - upc (str): The Universal Product Code of the item to retrieve.

    Returns:
    str: The generated description.
    """

    html_description = f"<h1>{shoprite_item_json['name']}</h2>"
    if shoprite_item_json["description"].lower() != shoprite_item_json["name"].lower():
        description = shoprite_item_json["description"].replace("\n", "<br>")
        html_description += f"<p>{description}</p>"

    # Add ingredients list
    try:
        if shoprite_item_json["ingredients"].split(";")[0].strip() == "":
            return html_description
    except Exception:
        return html_description

    html_description += "<h2>Ingredients</h3>"
    html_description += "<ul>"
    ingredients = shoprite_item_json["ingredients"].split(";")
    for ingredient in ingredients:
        stripped_ingredient = ingredient.strip()
        if stripped_ingredient:
            html_description += f"<li>{stripped_ingredient}</li>"
    html_description += "</ul>"

    try:
        if shoprite_item_json["nutritionProfiles"]["nutrition"].items() is None:
            return html_description
    except Exception:
        return html_description

    # Add nutrition profile table
    html_description += "<h2>Nutrition Profile</h2>"
    html_description += "<table border='1'>"
    html_description += (
        "<tr><th>Nutrient</th><th>Amount per Serving</th><th>% Daily Value</th></tr>"
    )
    for nutrient, data in shoprite_item_json["nutritionProfiles"]["nutrition"].items():
        html_description += "<tr>"
        html_description += f"<td>{nutrient}</td>"
        html_description += (
            f"<td>{data['size']} {data['unit']} ({data['abbreviation']})</td>"
        )
        if data["percentDailyValue"] is not None:
            html_description += f"<td>{data['percentDailyValue']}%</td>"
        else:
            html_description += "<td>N/A</td>"
        html_description += "</tr>"
    html_description += "</table>"

    return html_description
