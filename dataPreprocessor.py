import re
import pandas as pd

def preprocessor(chat_data):
    pattern = r'(\d{1,2}/\d{1,2}/\d{2,4}),\s(\d{1,2}:\d{2})[\s\u202f]*([apAP][mM])\s-\s(\+91\s\d{5}\s\d{5}|[^:]+):\s(.+)'
    matches = re.findall(pattern, chat_data)
    df = pd.DataFrame(matches, columns=['Date', 'Time', 'AM_PM', 'User', 'Message'])
    df['msg_time_date'] = pd.to_datetime(df['Date'] + ' ' + df['Time'] + ' ' + df['AM_PM'], format='%d/%m/%y %I:%M %p')

    df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%y')
    df["day"] = df["Date"].dt.strftime('%A')
    df["month"] = df["Date"].dt.strftime('%B')
    df["year"] = df["Date"].dt.year

    df.drop(['Date', 'Time', 'AM_PM'], axis=1, inplace=True)
    return df