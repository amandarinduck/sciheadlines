import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import streamlit as st

# TODO: add sort by field
# TODO: add status indicator
st.title("Nature Headline Aggregator", text_alignment="center")


subjects = [
    "microbiology",
    "virology",
    "protein-design",
    "synthetic-biology",
    "biotechnology",
    "biochemistry",
    "computational-biology-and-bioinformatics",
]


headlines = []
for subject in subjects:
    url = f"https://www.nature.com/subjects/{subject}"
    r = requests.get(url)
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, "html.parser")
        title = soup.find_all("a", class_="u-link-inherit")
        date = soup.find_all("time", class_="c-meta__item c-meta__item--block-at-lg")
        type = soup.find_all("span", class_="c-meta__type")

        print(f"SCRAPING HEADLINES IN SUBJECT FIELD: {subject}")
        for x in title:
            for y in date:
                for z in type:
                    data = {
                        "Field": subject,
                        "Date": y.text,
                        "Type": z.text,
                        "Headline": x.text,
                        "URL": f"www.nature.com{x['href']}",
                    }
                    headlines.append(data)

        time.sleep(10)

    elif r.status_code == 400:
        print(f"Error scraping {subject}, continuing to next subject")
        continue
    else:
        print(f"Exiting with status code {r.status_code} while scraping {subject}")
        break

df = pd.DataFrame(headlines)
df = df.drop_duplicates("Headline")
st.dataframe(df)
