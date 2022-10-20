import requests
import json
import shutil
import pyjsonviewer

i = 1
SIZE = 96
page = 1
categories = ["consumables", "equipment", "pets", "resources", "weapons"]
category = 0

while category <= (len(categories)-1):
    apiRequest = requests.get("https://enc.dofusdu.de/dofus/en/" + categories[category] + "?page%5Bnumber%5D=" + str(page)
                              + "&page%5Bsize%5D=" + str(SIZE))

    while apiRequest.status_code == 200:
        apiResponse = json.loads(apiRequest.content)
        # pyjsonviewer.view_data(json_data=apiResponse)
        for item in apiResponse["items"]:
            wikiRequest = requests.get(item["item_url"])
            wikiResponse = json.loads(wikiRequest.content)
            # pyjsonviewer.view_data(json_data=wikiResponse)
            # print(wikiResponse["image_url"])  # TODO: REPLACE PRINTING WITH DOWNLOADING THE PNG FILES
            img = requests.get(wikiResponse["image_url"], stream=True)
            with open((".\\output\\" + str(i) + ".png"), 'wb') as f:
                shutil.copyfileobj(img.raw, f)
            i += 1
            print(categories[category] + " : " + str(i))
        if "next" in apiResponse["_links"]:
            apiRequest = requests.get(apiResponse["_links"]["next"])
        else:
            apiRequest = requests.get("https://enc.dofusdu.de/dofus/en/" + categories[category] + "?page%5Bnumber%5D=" + str(page)
                                      + "&page%5Bsize%5D=97")  # INTENTIONAL 404 TO BREAK LOOP
    print("ALL DONE, NO MORE " + categories[category].upper())
    category += 1
print("ALL SPRITES DOWNLOADED.")
