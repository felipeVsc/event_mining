from flair.models import TextClassifier
from flair.data import Sentence
import time
import pandas as pd
from datetime import datetime

inicio = time.time()  # Marca o início


news_data = pd.read_json("news.json",orient="records",lines=True)

# Extracting info from date
def extract_periods(date: datetime):
    day = date.day
    year = date.year
    month = date.month
    
    bimonthly = (month - 1) // 2 + 1
    quarter = (month - 1) // 3 + 1
    four_months = (month - 1) // 4 + 1
    decade = (year // 10) * 10

    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday","Sunday"]
    weekday = weekdays[date.weekday()]

    return {
        "fullDate":str(date.__str__()[:10]),
        "day":day,
        "dayOfWeek":weekday,
        "month": month,
        "bimonthly": bimonthly,
        "quarter": quarter,
        "fourMonths": four_months,
        "year": year,
        "decade": decade,
    }

# Sentiment Extraction using FLAIR

sentiment_model = TextClassifier.load('en-sentiment')

def analyze_sentiment(text):
    if text == "":
        return "POSITIVE"
    sentence = Sentence(text)
    sentiment_model.predict(sentence)
    sentiment = sentence.labels[0]
    return sentiment.value


# Selecting and cleaning news dataset
politics_raw = news_data[news_data['category']=="POLITICS"]
politics_not_null = politics_raw.dropna()
politics_cleaned = politics_not_null[(politics_not_null['authors']!="")& (politics_not_null['headline']!="") & (politics_not_null['short_description']!="")]
politics = politics_cleaned.reset_index(drop=True)

# Sentiment analysis
sentiments_list = [analyze_sentiment(text) for text in politics['short_description'].tolist()]
politics['sentiment'] = sentiments_list

# Date Table
date_df = pd.DataFrame(columns=["fullDate","day","dayOfWeek", "month", "bimonthly", "quarter", "fourMonths", "year", "decade"])
for date in politics['date'].unique():
    extracted_date = extract_periods(date)
    date_df.loc[len(date_df)] = extracted_date.values()

# Location Table
cities = pd.read_csv("./cities.csv")
cities_filtered = cities[["city","state_name","population","lat","lng"]]
cities_filtered['country'] = "United States"
top100_cities = cities_filtered.sort_values(by="population",ascending=False)[:100]
top100_cities = top100_cities.rename({"state_name":"state","lat":"latitude","lng":"longitude"})

# Content Table

content_table = politics.rename(columns={"link":"linkSource","headline":"title","short_description":"summary"})

# Event Table

import random

event_table = pd.DataFrame(columns=["dateID","locationID","contentID","NumberNegativeNews","NumberPositiveNews","totalQuantity"])

for index,event in content_table.iterrows():  
    date_id = date_df.loc[date_df['fullDate']== str(event.date)[:10]].index[0]
    location_id = random.randrange(0,len(cities))
    content_id = index
    number_negative = 1 if event.sentiment == "POSITIVE" else 0
    number_positive = 1 if event.sentiment == "NEGATIVE" else 0
    total_qnt = 1 if number_negative==1 or number_positive == 1 else 0
    
    new_row = [date_id,location_id,content_id,number_negative,number_positive,total_qnt]
    event_table.loc[len(event_table)] = new_row

# Dropping Content table "date" field because it is not necessary anymore

content_table = content_table.drop(['date'],axis='columns')

fim = time.time()  # Marca o fim
tempo_total = fim - inicio  # Calcula o tempo total
print(f"Tempo de execução: {tempo_total:.6f} segundos")

content_table.to_csv("teste.csv")
