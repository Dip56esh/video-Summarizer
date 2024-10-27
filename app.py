import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genAI
from youtube_transcript_api import YouTubeTranscriptApi

load_dotenv()

genAI.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def extract_video_transcript(youtube_video_url):
    try:
        video_id=youtube_video_url.split("=")[1]
        
        transcript_text=YouTubeTranscriptApi.get_transcript(video_id)

        transcript = ""
        for i in transcript_text:
            transcript += " " + i["text"]

        return transcript

    except Exception as e:
        raise e
    
def generate_content(transcript_text,prompt):
    model=genAI.GenerativeModel("gemini-pro")
    response=model.generate_content(prompt+transcript_text)
    return response.text

prompt="""You are Youtube video summarizer. You will be taking the transcript text
and summarizing the entire video and providing the important summary in points
within 250 words in bulletin. Please provide the summary of the text given here:  """

st.title("Youtube Video Summarizer")
youtube_link = st.text_input("Enter YouTube Video Link:")

if youtube_link:
    video_id = youtube_link.split("=")[1]
    print(video_id)
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

if st.button("Summarize the video"):
    transcript_text=extract_video_transcript(youtube_link)

    if transcript_text:
        summary=generate_content(transcript_text,prompt)
        st.markdown("## Detailed Notes:")
        st.write(summary)