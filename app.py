import streamlit as st
import dataPreprocessor,Helper
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import matplotlib

matplotlib.rcParams['font.family'] = 'DejaVu Sans' 

emoji_font_path = "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf"  # Adjust for your OS
# prop = fm.FontProperties(fname=emoji_font_path)

st.sidebar.title("Whatsapp Chat Analyzer")
# add file uploader
uploaded_files = st.sidebar.file_uploader("Choose a CSV file")

if uploaded_files is not None:
    # get value of file
    bytes_data = uploaded_files.getvalue()
    data=bytes_data.decode("utf-8")
    # to see it in window(side)
    # st.text(data)

    # cll function of preprocesson
    df = dataPreprocessor.preprocessor(data)
#   show data frame in display
    st.dataframe(df)

    # now start owr analysis

    # Fetch unique user(single use)
    user_list = df['User'].unique().tolist()
    user_list.sort()
    # Select overall or single person analysis 
    user_list.insert(0,"Group Analysis")
    selected_user = st.sidebar.selectbox("Show user analysis",user_list)

    if st.sidebar.button("Show Analysis"):

        stat = Helper.fetch_statestic(selected_user,df)
        word,num_msg, midea_msg, emojis, monthly_activity, daily_activity, weekday_counts,wordcloud=stat
        st.header("📊 TOP Statistics")
        col1, col2, col3 ,col4,col5 = st.columns(5) 
        with col1: 
            st.subheader("Total Messages")
            st.write(f"*****Total Messages:***** {num_msg}")
        with col2: 
            st.subheader("Total Words")
            st.write(f"*****Total Words:***** {word}")  
        with col3: 
            st.subheader("Media share")
            st.write(f"*****Media Shared:***** {midea_msg}")
        with col4: 
            st.subheader("Total Emoji")
            st.write(f"*****EMOJIS:***** {emojis}")  

        st.header("TimeLine and Activities")
        fig1, ax1 = plt.subplots(figsize=(12, 4))
        sns.lineplot(x=monthly_activity.index, y=monthly_activity.values, marker="o", ax=ax1)
        plt.xticks(rotation=90)
        ax1.set_title("Monthly Timeline")
        st.pyplot(fig1)

        # daily time line
        fig2, ax2 = plt.subplots(figsize=(12, 5))
        daily_activity.plot(kind='line', color='green')
        ax2.set_xlabel('Date')
        ax2.set_ylabel('Messages Sent')
        ax2.set_title('Daily Chat timeline')
        plt.xticks(rotation=45)
        plt.grid()
        st.pyplot(fig2)

    #    Weekly activity map
        print(df['msg_time_date'].dtype)
        print(df['msg_time_date'].head())  # See if it's properly formatted

        print("Weekday Counts Data:", weekday_counts)
        print("Index:", weekday_counts.index)
        print("Values:", weekday_counts.values)
        fig3, ax3 = plt.subplots(figsize=(8, 4))
        sns.barplot(x=weekday_counts.index, y=weekday_counts.values, palette="viridis", ax=ax3)
        ax3.set_xlabel("Day of the Week")
        ax3.set_ylabel("Message Count")
        ax3.set_title("Busiest Days in Chat")
        plt.xticks(rotation=45)
        st.pyplot(fig3)

        st.subheader("☁️ WordCloud - Most Used Words")
        fig4, ax4 = plt.subplots(figsize=(10, 5))
        ax4.imshow(wordcloud, interpolation="bilinear")
        ax4.axis("off")  # Hide axes
        st.pyplot(fig4)

        
        st.header("EMOJIS Analysis")
        emoji_df = Helper.emoji_helper(selected_user,df)
        # st.dataframe(emoji_df.head())
        # st.dataframe(emoji_df.columns)
        st.dataframe(emoji_df)
