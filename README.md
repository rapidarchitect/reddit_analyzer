# Reddit Topic Analysis Tool

A Streamlit application that analyzes Reddit posts on any topic using AI-powered insights. This tool combines Reddit's API with local LLMs through Ollama to provide meaningful analysis of Reddit discussions.

## Features

- Search and analyze Reddit posts on any topic
- Utilize local LLMs via Ollama for content analysis
- Customize the number of posts to analyze (1-20)
- Generate downloadable markdown reports
- Interactive web interface built with Streamlit

## Prerequisites

- Python 3.6+
- Streamlit
- PRAW (Python Reddit API Wrapper)
- Ollama
- A Reddit Developer Account

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd reddit-topic-analysis
```

2. Install the required dependencies:
```bash
pip install streamlit praw ollama
```

3. Install Ollama and at least one language model:
```bash
# Install Ollama (instructions vary by OS)
curl https://ollama.ai/install.sh | sh

# Pull a model (e.g., Llama 2)
ollama pull llama2
```

4. Set up your Reddit API credentials:
   - Go to https://www.reddit.com/prefs/apps
   - Create a new application
   - Note your client ID and client secret

## Configuration

The application uses the some test Reddit API credentials by default

For security reasons, it's recommended to use environment variables or a configuration file for these credentials in a production environment.

## Usage

1. Start the Ollama service:
```bash
ollama serve
```

2. Run the Streamlit application:
```bash
streamlit run app.py
```

3. In the web interface:
   - Select your preferred Ollama model from the sidebar
   - Adjust the number of posts to analyze using the slider
   - Enter a topic in the main area
   - Click "Analyze Topic" to generate insights

4. The analysis will include:
   - Individual post details (title, subreddit, score)
   - AI-generated summary of insights and trends
   - Option to download the analysis as a markdown file

## Output Format

The analysis is presented in a structured markdown format:
- Topic header
- List of analyzed posts with links
- Summary of insights and trends
- Download option for the complete analysis

## Error Handling

The application includes error handling for:
- Ollama connection issues
- Reddit API errors
- Invalid topic searches
- Model availability checks

## Security Notes

- The included Reddit API credentials should be replaced with your own for production use
- Consider implementing proper credential management
- Review Ollama model access and permissions

## Contributing

Feel free to submit issues and enhancement requests!

## License
MIT LICENSE