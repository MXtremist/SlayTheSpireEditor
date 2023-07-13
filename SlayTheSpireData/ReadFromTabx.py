from bs4 import BeautifulSoup
import pandas as pd


def readcardsfromtabx():
    tabx = "Data-Card_data.tabx"
    output = "SlayTheSpireCardData.csv"
    lenx = 16
    df = pd.DataFrame(
        columns=[
            "page",
            "name",
            "card_id",
            "name_en",
            "color",
            "type",
            "rarity",
            "cost",
            "description",
            "ability",
            "upgrade_cost",
            "upgrade_desc",
            "upgrade_ability",
            "image",
            "test_image",
            "main_category",
        ]
    )
    # page,name,card_id,name_en,color,type,rarity,cost,description,ability,upgrade_cost,upgrade_desc,upgrade_ability,image,test_image,main_category
    with open(tabx, encoding="utf-8") as file:
        for line in file:
            soup = BeautifulSoup(line, "html.parser")
            td_all = soup.find_all("td")
            td_text = []
            for td in td_all:
                td_text.append(td.text)
            df2 = pd.DataFrame(td_text).T
            df2.columns = df.columns

            df = df.append(df2, ignore_index=True)
            # print(df)

            # break
        # print(df)
        df = df.drop(
            columns=[
                "page",
                "ability",
                "upgrade_ability",
                "image",
                "test_image",
                "main_category",
            ]
        )
        df.to_csv(output, index=None)


readcardsfromtabx()
exit()
