import validators
import streamlit as st
import os
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain.schema import Document
from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs
from dotenv import load_dotenv
import time

## Page configuration with custom theme
st.set_page_config(
    page_title="AI Content Summarizer",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

## Custom CSS
st.markdown("""
    <style>
        .stApp {
            max-width: 1200px;
            margin: 0 auto;
        }
        .success-message {
            padding: 1rem;
            border-radius: 0.5rem;
            background-color: #f0f9ff;
            border: 1px solid #e0f2fe;
        }
        .stButton>button {
            width: 100%;
        }
        .url-input {
            margin-bottom: 1rem;
        }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'summary_history' not in st.session_state:
    st.session_state.summary_history = []
if 'processing_time' not in st.session_state:
    st.session_state.processing_time = 0

def extract_video_id(url):
    """Extract the video ID from various forms of YouTube URLs."""
    try:
        # Handle youtu.be URLs
        if 'youtu.be' in url:
            return url.split('/')[-1].split('?')[0]
        
        # Handle youtube.com URLs
        parsed_url = urlparse(url)
        if 'youtube.com' in parsed_url.netloc:
            return parse_qs(parsed_url.query)['v'][0]
    except Exception:
        return None
    return None

def get_youtube_transcript(url):
    try:
        video_id = extract_video_id(url)
        if not video_id:
            raise Exception("Could not extract video ID from URL")

        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        transcript_text = " ".join([entry['text'] for entry in transcript_list])
        
        if not transcript_text:
            raise Exception("No transcript content could be extracted")

        return [Document(
            page_content=transcript_text,
            metadata={"source": url, "video_id": video_id}
        )]
    except Exception as e:
        try:
            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
            
            # Try different transcript options
            for lang in ['en', 'en-US', 'en-GB']:
                try:
                    transcript = transcript_list.find_transcript([lang])
                    transcript_data = transcript.fetch()
                    transcript_text = " ".join([entry['text'] for entry in transcript_data])
                    return [Document(
                        page_content=transcript_text,
                        metadata={"source": url, "video_id": video_id}
                    )]
                except:
                    continue
            
            # If no English transcript found, try auto-generated
            transcript = transcript_list.find_generated_transcript()
            transcript_data = transcript.fetch()
            transcript_text = " ".join([entry['text'] for entry in transcript_data])
            
            return [Document(
                page_content=transcript_text,
                metadata={"source": url, "video_id": video_id}
            )]
        except Exception as inner_e:
            raise Exception(f"Failed to fetch YouTube transcript: {str(inner_e)}")

# Sidebar configuration
with st.sidebar:
    st.image("https://em-content.zobj.net/thumbs/240/apple/325/books_1f4da.png", width=50)
    st.title("Settings")
    
    # API Key input with validation
    groq_api_key = st.text_input(
        "Enter Groq API Key",
        type="password",
        help="Enter your Groq API key to enable summarization"
    )
    
    # Summary length selector
    summary_length = st.select_slider(
        "Summary Length",
        options=["Brief", "Moderate", "Detailed"],
        value="Moderate"
    )
    
    # Language style selector
    language_style = st.selectbox(
        "Language Style",
        ["Professional", "Casual", "Academic"]
    )
    
    # Show history toggle
    show_history = st.checkbox("Show Summary History", value=True)

# Main content area
st.title("📚 AI Content Summarizer")
st.markdown("### Transform Videos and Articles into Quick Summaries")

# URL input
url = st.text_input(
    "Enter YouTube URL or Website Link",
    placeholder="https://youtube.com/... or https://...",
    help="Paste a YouTube video URL or website link to get started"
)

# Dynamic prompt template based on user settings
def get_prompt_template(length, style):
    length_words = {
        "Brief": "200",
        "Moderate": "400",
        "Detailed": "600"
    }
    
    style_instructions = {
        "Professional": "Use professional language and focus on key business insights",
        "Casual": "Use conversational language and make it easy to understand",
        "Academic": "Use academic language and provide detailed analysis"
    }
    
    template = f"""
    As an AI assistant, provide a {length_words[length]}-word summary of the following content.
    {style_instructions[style]}
    
    Focus on:
    - Main topics and key points
    - Important insights or conclusions
    - Overall message or purpose
    
    Content: {{text}}
    
    Summary:
    """
    return template

if st.button("Generate Summary", key="generate"):
    if not groq_api_key.strip():
        st.error("⚠️ Please enter your Groq API key in the sidebar to continue")
    elif not url.strip():
        st.error("⚠️ Please enter a URL to summarize")
    elif not validators.url(url):
        st.error("⚠️ Please enter a valid URL")
    else:
        try:
            start_time = time.time()
            
            # Progress bar and status
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Initialize LLM and prompt
            status_text.text("Initializing AI model...")
            progress_bar.progress(20)
            
            llm = ChatGroq(groq_api_key=groq_api_key, model="Llama3-8b-8192")
            prompt = PromptTemplate(
                input_variables=["text"],
                template=get_prompt_template(summary_length, language_style)
            )
            
            # Fetch content
            status_text.text("Fetching content...")
            progress_bar.progress(40)
            
            if "youtube.com" in url or "youtu.be" in url:
                docs = get_youtube_transcript(url)
                content_type = "video"
            else:
                loader = UnstructuredURLLoader(
                    urls=[url],
                    ssl_verify=False,
                    headers={
                        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
                    }
                )
                docs = loader.load()
                content_type = "article"
            
            # Generate summary
            status_text.text("Generating summary...")
            progress_bar.progress(70)
            
            chain = load_summarize_chain(
                llm,
                chain_type="stuff",
                prompt=prompt,
                verbose=True
            )
            
            summary = chain.run(docs)
            
            # Calculate processing time
            end_time = time.time()
            processing_time = round(end_time - start_time, 2)
            st.session_state.processing_time = processing_time
            
            # Update progress
            progress_bar.progress(100)
            status_text.empty()
            
            # Display summary
            st.markdown("### Summary")
            st.markdown(f"""
            <div class="success-message">
                {summary}
            </div>
            """, unsafe_allow_html=True)
            
            # Display metadata
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Processing Time", f"{processing_time}s")
            with col2:
                st.metric("Content Type", content_type.title())
            with col3:
                st.metric("Summary Length", summary_length)
            
            # Add to history
            st.session_state.summary_history.append({
                "url": url,
                "summary": summary,
                "time": processing_time,
                "type": content_type
            })
            
        except Exception as e:
            st.error(f"Error: {str(e)}")
            
# Display history if enabled
if show_history and st.session_state.summary_history:
    st.markdown("### Summary History")
    for i, item in enumerate(reversed(st.session_state.summary_history)):
        with st.expander(f"Summary {i+1} - {item['url'][:50]}..."):
            st.markdown(item['summary'])
            st.markdown(f"*Processed in {item['time']}s - {item['type'].title()}*")

# Footer
st.markdown("---")
st.markdown(
    "Made with ❤️ using Streamlit and LangChain"
)
