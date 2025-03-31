import emoji
import pandas as pd
from wordcloud import WordCloud
from collections import Counter

def fetch_statestic(selected_user,df):
    if selected_user != 'Group Analysis':
        df =df[df["User"] == selected_user]

    num_msg = df.shape[0]
    word = []
    for message in df['Message']:
            word.extend(message.split())

    links_msg = df[df['Message'] == '<Media omitted>'].shape[0]
    emoji_list = []
    for message in df['Message']:
        emoji_list.extend([c for c in message if c in emoji.EMOJI_DATA])

    df['day'] = pd.to_datetime(df['day'], errors='coerce') 
    monthly_activity = df['month'].value_counts().sort_index()

    df['day'] = df['msg_time_date'].dt.date
    daily_counts = df.groupby('day').size()
    
    df['Weekday'] = df['msg_time_date'].dt.day_name()
    weekday_counts = df['Weekday'].value_counts()
    
    wordcloud = WordCloud(
        width=800, height=400, background_color='white', colormap='viridis',
        max_words=200, contour_width=3, contour_color='steelblue'
    ).generate(" ".join(df['Message'].dropna()))
    

    return (len(word), num_msg, 
            links_msg,
              len(emoji_list),
              monthly_activity,
              daily_counts, 
              weekday_counts,
              wordcloud)


def emoji_helper(selected_user,df):
    if selected_user != 'Group Analysis':
      df =df[df["User"] == selected_user]

    emoji_list = []
    for message in df['Message']:
        emoji_list.extend([c for c in message if c in emoji.EMOJI_DATA])
    emoji_df = pd.DataFrame(Counter(emoji_list).most_common(), columns=['emoji', 'count'])

    return emoji_df
