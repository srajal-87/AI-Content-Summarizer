# 📚 AI Content Summarizer

**Transform YouTube videos and web articles into concise, intelligent summaries with customizable options.**

## 📌 Project Description

AI Content Summarizer is a powerful tool that leverages artificial intelligence to extract and condense information from YouTube videos and web articles, saving users time while retaining key insights. Perfect for researchers, students, and professionals who need to quickly digest content.

## 🚀 Features

- 🎥 **YouTube video summarization** - Extract and process video transcripts automatically
- 🌐 **Web article summarization** - Process article content while preserving important context
- 📊 **Configurable summary settings**:
  - Adjustable summary length (Brief, Moderate, Detailed)
  - Multiple language styles (Professional, Casual, Academic)
- 📝 **Summary history tracking** - Review previously generated summaries
- ⚡ **Real-time processing status** - Track progress with visual indicators
- 🎨 **Clean, modern user interface** - Intuitive Streamlit-based web application

## 🛠️ Tech Stack

- **Python** - Core programming language
- **Streamlit** - Interactive web application framework
- **LangChain** - Framework for LLM applications
- **Groq** - AI model provider for text processing
- **YouTube Transcript API** - Extract transcripts from YouTube videos
## 📁 Project Structure

```
ai-content-summarizer/
├── app.py                 # Main application file
├── requirements.txt       # Project dependencies
├── .env                   # Environment variables (create this)
└── README.md              # Project documentation
```

## 🧠 How It Works

1. **Input Processing**:
   - User enters a YouTube URL or webpage link
   - System validates the URL and determines content type
   - For YouTube: Extracts video transcript using YouTube Transcript API
   - For websites: Uses UnstructuredURLLoader to extract relevant content

2. **Summarization Pipeline**:
   - Extracted content is processed through LangChain's summarization chain
   - Summary parameters (length, style) customize the prompt template
   - Groq LLM (Llama3-8b-8192) generates the final summary

3. **Output Handling**:
   - Summary is displayed in a formatted container
   - Processing metrics are shown (time, content type, summary length)
   - Summary is added to session history for future reference

## 🧪 Setup & Installation Instructions

### Prerequisites

- Python 3.8+ installed
- Groq API key (sign up at [Groq's website](https://groq.com))

### Installation Steps

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ai-content-summarizer.git
cd ai-content-summarizer
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root:
```
GROQ_API_KEY=your_api_key_here
```

5. Start the application:
```bash
streamlit run app.py
```

6. Open your web browser and navigate to http://localhost:8501

### Usage Instructions

1. Enter your Groq API key in the sidebar
2. Paste a YouTube URL or website link in the input field
3. Configure summary settings:
   - Summary Length: Brief (~200 words), Moderate (~400 words), or Detailed (~600 words)
   - Language Style: Professional, Casual, or Academic
4. Click "Generate Summary" to process the content
5. Review the summary and processing metrics
6. Access previous summaries in the history section (if enabled)


## 📌 Future Improvements

- 🔄 Support for additional content sources (PDF, Twitter threads, podcasts)
- 🔤 Expanded language support for non-English content
- 📊 Advanced visualization of key topics and concepts
- 🔑 Additional AI model options beyond Groq

## 🧑‍💻 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please ensure your code follows the project's coding standards and includes appropriate tests.

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

Made with ❤️ using Streamlit and LangChain
