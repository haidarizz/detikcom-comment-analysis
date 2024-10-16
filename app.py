import streamlit as st
import pandas as pd
import plotly.express as px

# Load the data from Excel files
file_path_df_analysis = 'df_analysis.xlsx'
df_analysis = pd.read_excel(file_path_df_analysis)

file_path_df_word_count = 'df_word_count.xlsx'
df_word_count = pd.read_excel(file_path_df_word_count)

file_path_df_word_count_all = 'df_word_count_all.xlsx'
df_word_count_all = pd.read_excel(file_path_df_word_count_all)

# Create df_comment where username != 'detikcom' and sentiment != 'unknown'
df_comment = df_analysis[(df_analysis['username'] != 'detikcom') & (df_analysis['sentiment'] != 'unknown')]

# Create df_caption where username == 'detikcom'
df_caption = df_analysis[df_analysis['username'] == 'detikcom']

# Sidebar with menu options
menu = st.sidebar.radio(
    "Select a Menu",
    ("Comment Distribution", "Caption Analysis", "Sentiment Overview", "Emotion Overview", "Frequent Words (All)", "What People Say in Certain Mood", "User Analysis and Behavior", "Table of All Data", "Data Source")
)

# Default view - when the app is loaded, show 'Data Visualization' by default
if menu == "Comment Distribution":
    st.title("Comment Distribution")
    # Bar Chart: Comment Distribution (based on post_id)
    # Bar Chart: Comment Distribution (post_id on y-axis, count on x-axis)

    # Count the number of comments per post and reset index to create a DataFrame
    comment_count = df_comment['post_id'].value_counts(ascending=True).reset_index()
    comment_count.columns = ['post_id', 'count']  # Renaming the columns appropriately

    # Create bar chart
    fig_comment_dist = px.bar(
        comment_count, 
        x='count',  # Number of comments
        y='post_id', 
        orientation='h',
        title='Comment Distribution by Post',
        labels={'count': 'Number of Comments', 'post_id': 'Post ID'},
        height=600
    )

    # Show chart
    st.plotly_chart(fig_comment_dist)


    # Line Chart: Time Distribution (based on hour)
    st.write("### Comment Time Distribution (by Hour of Day)")

    # Extract the hour from the 'time' column
    df_comment['hour'] = df_comment['time'].dt.hour

    # Count the number of comments per hour
    time_distribution = df_comment['hour'].value_counts().sort_index().reset_index()
    time_distribution.columns = ['hour', 'comment_count']

    # Create line chart
    fig_time_dist_comment = px.line(
        time_distribution,
        x='hour',
        y='comment_count',
        title='Time Distribution of Comments',
        labels={'hour': 'Hour of the Day', 'comment_count': 'Number of Comments'},
    )

    # Customize x-axis to show only 5, 10, 15, 20
    fig_time_dist_comment.update_xaxes(dtick=5)

    # Show chart
    st.plotly_chart(fig_time_dist_comment)

     # Line Chart: Caption Time Distribution (based on hour) for df_caption
    st.write("### Post Time Distribution (by Hour of Day)")

    # Extract the hour from the 'time' column in df_caption
    df_caption['hour'] = df_caption['time'].dt.hour

    # Count the number of captions per hour
    time_distribution_caption = df_caption['hour'].value_counts().sort_index().reset_index()
    time_distribution_caption.columns = ['hour', 'caption_count']

    # Create line chart
    fig_time_dist_caption = px.line(
        time_distribution_caption,
        x='hour',
        y='caption_count',
        title='Time Distribution of Posts',
        labels={'hour': 'Hour of the Day', 'caption_count': 'Number of Posts'},
    )

    # Customize x-axis to show only 5, 10, 15, 20
    fig_time_dist_caption.update_xaxes(dtick=5)

    # Show chart
    st.plotly_chart(fig_time_dist_caption)

elif menu == "Caption Analysis":
    st.title("Caption Analysis")
    st.write("### Instagram Caption Analysis with Sentiment and Emotion")
    
    # Pie chart based on sentiment counts
    sentiment_count = df_caption['sentiment'].value_counts().reset_index()
    sentiment_count.columns = ['sentiment', 'count']

    # Custom sentiment colors (like the ones used in Sentiment Overview)
    sentiment_colors = {
        'negative': '#FF6B6B',  # soft red
        'positive': '#4CAF50',  # soft green
        'neutral': '#1E90FF'    # soft blue
    }

    # Create pie chart for sentiment
    fig_sentiment = px.pie(
        sentiment_count,
        values='count',
        names='sentiment',
        title='Sentiment Distribution in Captions',
        color='sentiment',
        color_discrete_map=sentiment_colors
    )

    # Display pie chart for sentiment
    st.plotly_chart(fig_sentiment)

    # Pie chart based on emotion counts
    emotion_count = df_caption['emotion'].value_counts().reset_index()
    emotion_count.columns = ['emotion', 'count']

    # Custom emotion colors (same as Emotion Overview)
    emotion_colors = {
        'happy': '#FFD700',    # gold
        'fear': '#FF6347',     # tomato
        'love': '#FF69B4',     # hot pink
        'anger': '#DC143C',    # crimson
        'sadness': '#1E90FF'   # dodger blue
    }

    # Create pie chart for emotion
    fig_emotion = px.pie(
        emotion_count,
        values='count',
        names='emotion',
        title='Emotion Distribution in Captions',
        color='emotion',
        color_discrete_map=emotion_colors
    )

    # Display pie chart for emotion
    st.plotly_chart(fig_emotion)

elif menu == "Sentiment Overview":
    st.title("Sentiment Overview")
    st.write("### Instagram Sentiment Overview")

    # Pie chart based on sentiment counts
    sentiment_count = df_comment['sentiment'].value_counts().reset_index()
    sentiment_count.columns = ['sentiment', 'count']

    # Custom colors for sentiment (easier to differentiate)
    sentiment_colors = {
        'negative': '#FF6B6B',  # soft red
        'positive': '#4CAF50',  # soft green
        'neutral': '#1E90FF'    # soft blue
    }

    # Create pie chart
    fig_sentiment = px.pie(
        sentiment_count,
        values='count',
        names='sentiment',
        title='Sentiment Distribution',
        color='sentiment',
        color_discrete_map=sentiment_colors
    )

    # Show pie chart in Streamlit
    st.plotly_chart(fig_sentiment)

    # Line Chart: Sentiment over time (grouped by hour)
    st.write("### Sentiment Over Time (Per Hour)")

    # Extract hour from 'time' column if not already done
    if 'hour' not in df_comment.columns:
        df_comment['hour'] = df_comment['time'].dt.hour

    # Group data by hour and sentiment, then count occurrences
    sentiment_time = df_comment.groupby(['hour', 'sentiment']).size().reset_index(name='count')

    # Create line chart
    fig_sentiment_time = px.line(
        sentiment_time,
        x='hour',
        y='count',
        color='sentiment',
        title='Sentiment Distribution Over Time (Per Hour)',
        labels={'hour': 'Hour of Day', 'count': 'Number of Comments'},
        color_discrete_map=sentiment_colors
    )

    # Customize x-axis to show only 5, 10, 15, 20
    fig_sentiment_time.update_xaxes(dtick=5)

    # Show line chart in Streamlit
    st.plotly_chart(fig_sentiment_time)

elif menu == "Emotion Overview":
    st.title("Emotion Overview")
    st.write("### Instagram Emotion Overview")

    # Pie chart based on emotion counts
    emotion_count = df_comment['emotion'].value_counts().reset_index()
    emotion_count.columns = ['emotion', 'count']

    # Custom colors for emotion (easy to differentiate)
    emotion_colors = {
        'happy': '#FFD700',    # gold
        'fear': '#FF6347',     # tomato
        'love': '#FF69B4',     # hot pink
        'anger': '#DC143C',    # crimson
        'sadness': '#1E90FF'   # dodger blue
    }

    # Create pie chart
    fig_emotion = px.pie(
        emotion_count,
        values='count',
        names='emotion',
        title='Emotion Distribution',
        color='emotion',
        color_discrete_map=emotion_colors
    )

    # Show pie chart in Streamlit
    st.plotly_chart(fig_emotion)

    # Line Chart: Emotion over time (grouped by hour)
    st.write("### Emotion Over Time (Per Hour)")

    # Extract hour from 'time' column if not already done
    if 'hour' not in df_comment.columns:
        df_comment['hour'] = df_comment['time'].dt.hour

    # Group data by hour and emotion, then count occurrences
    emotion_time = df_comment.groupby(['hour', 'emotion']).size().reset_index(name='count')

    # Create line chart
    fig_emotion_time = px.line(
        emotion_time,
        x='hour',
        y='count',
        color='emotion',
        title='Emotion Distribution Over Time (Per Hour)',
        labels={'hour': 'Hour of Day', 'count': 'Number of Comments'},
        color_discrete_map=emotion_colors
    )

    # Customize x-axis to show only 5, 10, 15, 20
    fig_emotion_time.update_xaxes(dtick=5)

    # Show line chart in Streamlit
    st.plotly_chart(fig_emotion_time)

elif menu == "Frequent Words (All)":
    st.title("Frequent Words (All)")
    st.write("### Top Words of Instagram Comments")

    # Sort df_word_count_all by frequency and select top 20 words
    top_words = df_word_count_all.nlargest(20, 'Frequency')

    # Create a bar chart with Plotly Express
    fig_top_words = px.bar(
        top_words,
        x='Frequency',
        y='Word',
        orientation='h',  # horizontal bar chart
        title='Top 20 Most Frequent Words',
        labels={'frequency': 'Frequency', 'word': 'Word'},
        height=600
    )

    # Customize layout for better readability
    fig_top_words.update_layout(
        xaxis_title="Frequency",
        yaxis_title="Word",
        yaxis=dict(categoryorder='total ascending')  # Ensures words are sorted by frequency
    )

    # Display the bar chart
    st.plotly_chart(fig_top_words)

elif menu == "What People Say in Certain Mood":
    st.title("What People Say in Certain Mood")
    st.write("### Most Frequent Words Based on Sentiment and Emotion")

    # Define the categories to visualize
    categories = df_word_count['Category'].unique()

    # Loop through each category to create a separate bar chart
    for category in categories:
        #st.write(f"### Top Words in {category.capitalize()} Category")
        
        # Filter the DataFrame for the current category
        df_category = df_word_count[df_word_count['Category'] == category]

        # Sort by frequency and select the top 10 words for each category
        top_words_category = df_category.nlargest(15, 'Frequency')

        # Create a bar chart for the current category
        fig_category = px.bar(
            top_words_category,
            x='Frequency',
            y='Word',
            orientation='h',  # horizontal bar chart
            title=f'Top 10 Words in {category.capitalize()} Category',
            labels={'Frequency': 'Frequency', 'Word': 'Word'},
            height=400
        )

        # Customize layout for better readability
        fig_category.update_layout(
            xaxis_title="Frequency",
            yaxis_title="Word",
            yaxis=dict(categoryorder='total ascending')  # Sort words by frequency
        )

        # Display the bar chart for the current category
        st.plotly_chart(fig_category)

elif menu == "User Analysis and Behavior":
    st.title("User Analysis and Behavior")
    st.write("### Top 20 Users by Comment Count with Sentiment Distribution")

    # Count the number of comments per user
    user_comment_count = df_comment['username'].value_counts().reset_index()
    user_comment_count.columns = ['username', 'count']

    # Get top 20 users
    top_users = user_comment_count.nlargest(20, 'count')

    # Get sentiment distribution for each top user
    sentiment_distribution = df_comment[df_comment['username'].isin(top_users['username'])].groupby(['username', 'sentiment']).size().unstack(fill_value=0)

    # Combine the comment counts with the sentiment distribution
    combined_data = top_users.set_index('username').join(sentiment_distribution, how='left').fillna(0)

    # Define custom colors for the sentiments
    sentiment_colors = {
        'negative': '#FF6B6B',  # soft red
        'positive': '#4CAF50',  # soft green
        'neutral': '#1E90FF'    # soft blue
    }

    # Sort the combined data by count in descending order
    combined_data = combined_data.sort_values(by='count', ascending=True)  # Sort in ascending order for plotting

    # Create a stacked bar chart
    fig_user_sentiment = px.bar(
        combined_data,
        y=combined_data.index,  # Usernames on y-axis
        x=combined_data.columns[1:],  # Sentiment columns on x-axis
        title='Top 20 Users by Comment Count with Sentiment Distribution',
        labels={'value': 'Number of Comments', 'username': 'User'},
        height=600,
        color_discrete_sequence=[sentiment_colors[sentiment] for sentiment in combined_data.columns[1:]]  # Assign colors based on sentiment
    )

    # Update the layout for better visualization
    fig_user_sentiment.update_layout(
        barmode='stack',
        yaxis_title='User',
        xaxis_title='Number of Comments',
        legend_title='Sentiment',
        xaxis=dict(tickvals=combined_data.columns[1:])  # Show sentiment labels on x-axis
    )

    # Display the stacked bar chart
    st.plotly_chart(fig_user_sentiment)

elif menu == "Table of All Data":
    #st.title("Comment Data")
    st.write("### Comment Data (Main Data)")
    st.dataframe(df_analysis)
    st.write("### Word Count of All Data")
    st.dataframe(df_word_count_all)
    st.write("## Word Count Based on Sentiment and Emotion")
    st.dataframe(df_word_count)

elif menu == "Data Source":
    st.title("Data Source")
    st.write("Here are the Instagram post links used for data collection:")

    # List of hyperlinks to display
    links = [
        "https://www.instagram.com/p/DA0MCtnsErV/",
        "https://www.instagram.com/p/DA0TAETMhdl/",
        "https://www.instagram.com/p/DA0xxl9sOYG/",
        "https://www.instagram.com/p/DA0_gY0ySbj/",
        "https://www.instagram.com/p/DA0_hEAyWsR/",
        "https://www.instagram.com/p/DA2F5hxod2I/",
        "https://www.instagram.com/p/DA2fjcDvcwb/",
        "https://www.instagram.com/p/DA2LnunSL-u/",
        "https://www.instagram.com/p/DA2mk-kqSOW/",
        "https://www.instagram.com/p/DA2R6onIhzG/",
        "https://www.instagram.com/p/DA2_kIRMh0k/",
        "https://www.instagram.com/p/DA3CCsdC3NE/",
        "https://www.instagram.com/p/DA3dbRyypeF/",
        "https://www.instagram.com/p/DA3ZKe3Ped8/",
        "https://www.instagram.com/p/DA5SfXFsxb5/",
        "https://www.instagram.com/p/DAw6lcMIBZF/",
        "https://www.instagram.com/p/DAyJgBmtceg/",
        "https://www.instagram.com/p/DAz-W5oCzAn/",
        "https://www.instagram.com/p/DAz476zyeP6/",
        "https://www.instagram.com/p/DAzAfbMy0jg/"
    ]

    # Loop to display each link
    for link in links:
        st.markdown(f"[{link}]({link})")