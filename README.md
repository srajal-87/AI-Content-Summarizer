# AI Content Summarizer 📚

An intelligent content summarization tool that can process YouTube videos and web articles, providing concise summaries using AI. Built with Streamlit, LangChain, and Groq AI.

## Features

- 🎥 YouTube video summarization
- 🌐 Web article summarization
- 📊 Configurable summary length and style
- 📝 Summary history tracking
- ⚡ Real-time processing status
- 🎨 Clean, modern user interface

## Prerequisites

Before running the application, make sure you have Python 3.8+ installed on your system.

### Required API Keys

- **Groq API Key**: Sign up at [Groq's website](https://groq.com) to get your API key

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd ai-content-summarizer
```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

### Requirements.txt
```
streamlit
langchain
langchain_community
langchain-groq
youtube-transcript-api
unstructured
validators
python-dotenv
```

## Usage

1. Start the application:
```bash
streamlit run app.py
```

2. Open your web browser and navigate to the provided URL (typically http://localhost:8501)

3. Enter your Groq API key in the sidebar

4. Paste a YouTube URL or website link in the input field

5. Configure summary settings:
   - Summary Length: Brief, Moderate, or Detailed
   - Language Style: Professional, Casual, or Academic

6. Click "Generate Summary" to process the content

## Features in Detail

### Content Processing
- **YouTube Videos**: Automatically extracts and processes video transcripts
- **Web Articles**: Processes article content while preserving important context
- **Multiple Language Support**: Handles various English transcript variants

### Customization Options
- **Summary Length**:
  - Brief: ~200 words
  - Moderate: ~400 words
  - Detailed: ~600 words

- **Language Styles**:
  - Professional: Business-focused language
  - Casual: Conversational tone
  - Academic: Scholarly analysis

### User Interface
- Clean, modern design
- Responsive layout
- Progress tracking
- Error handling
- Summary history
- Performance metrics

## Project Structure

```
ai-content-summarizer/
├── app.py                 # Main application file
├── requirements.txt       # Project dependencies
├── .env                  # Environment variables (create this)
└── README.md             # Project documentation
```

## Configuration

Create a `.env` file in the project root:
```env
GROQ_API_KEY=your_api_key_here
```

## Error Handling

The application handles various error cases:
- Invalid URLs
- Missing API keys
- Failed content fetching
- Processing errors

## Performance

- Processing time is displayed for each summary
- Content type is automatically detected
- Summary history is maintained during the session

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Troubleshooting

Common issues and solutions:

1. **API Key Error**:
   - Verify your Groq API key is correct
   - Check if the key is properly set in the sidebar

2. **YouTube Transcript Error**:
   - Ensure the video has available captions
   - Try a different video if captions are unavailable

3. **Website Loading Error**:
   - Check if the website is accessible
   - Verify the URL format is correct

## Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Powered by [LangChain](https://langchain.org/)
- Uses [Groq](https://groq.com/) for AI processing
- YouTube transcript processing by [youtube-transcript-api](https://github.com/jdepoix/youtube-transcript-api)