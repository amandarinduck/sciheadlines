import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import streamlit as st

# TODO: add sort by field

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

@st.cache_data(show_spinner="Fetching fresh data...",ttl=86400)
def headlinescrape():
   
    for subject in subjects:
        url = f"https://www.nature.com/subjects/{subject}"
        r = requests.get(url)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, "html.parser")
            articles = soup.find_all("article")
            for article in articles:
                title = article.find("a", class_="u-link-inherit")
                date = article.find("time", class_="c-meta__item c-meta__item--block-at-lg")
                articletype = article.find("span", class_="c-meta__type")
                data = {
                            "Field": subject,
                            "Date": date.text,
                            "Type": articletype.text,
                            "Headline": title.text,
                            "URL": f"www.nature.com{title['href']}",
                        }
                headlines.append(data)
            print(subject)
            time.sleep(5)


        elif r.status_code in range(400,499):
            print(f"Client side error code {r.status_code} while scraping {subject}, ensure appropriate URL and authorization. Continuing to next subject")
            continue
        else:
            print(f"Exiting with status code {r.status_code} while scraping {subject}")
            break
    df=pd.DataFrame(headlines)
    df = pd.DataFrame(headlines)
    return df

def displaydf(df):
    st.dataframe(df)


    
if __name__ == '__main__':
    df = headlinescrape()
    displaydf(df)

