import streamlit as st
import praw
import ollama
from typing import List, Dict


def get_available_models() -> List[str]:
    """Fetch available models from Ollama."""
    try:
        models = ollama.list()
        return [model["name"] for model in models["models"]]
    except Exception as e:
        st.error(f"Error fetching Ollama models: {str(e)}")
        return []


def search_reddit_posts(reddit: praw.Reddit, topic: str, num_posts: int) -> List[Dict]:
    """Search Reddit for posts on a given topic."""
    post_analysis = []
    try:
        results = reddit.subreddit("all").search(topic, limit=num_posts)
        for post in results:
            analysis = {
                "title": post.title,
                "score": post.score,
                "url": post.url,
                "subreddit": post.subreddit.display_name,
            }
            post_analysis.append(analysis)
        return post_analysis
    except Exception as e:
        st.error(f"Error searching Reddit: {str(e)}")
        return []


def generate_analysis_prompt(topic: str, post_analysis: List[Dict]) -> str:
    """Create the analysis prompt for the LLM."""
    analysis_text = "\n".join(
        [
            f"Title: {post['title']}\nSubreddit: {post['subreddit']}\nScore: {post['score']}\nURL: {post['url']}\n"
            for post in post_analysis
        ]
    )
    return (
        f"Analyze the following Reddit posts about '{topic}'. "
        "For each post, summarize the key point and then identify any common themes or trends.\n\n"
        f"{analysis_text}\n\n"
        "Summarize the main insights and trends found in these posts."
    )


def format_markdown_output(
    topic: str, post_analysis: List[Dict], summary_text: str
) -> str:
    """Format the analysis results in Markdown."""
    markdown_output = f"# Analysis of Reddit Topic: '{topic}'\n\n"
    markdown_output += "## Individual Post Analysis\n"
    for post in post_analysis:
        markdown_output += f"- **Title**: [{post['title']}]({post['url']})\n"
        markdown_output += f"  - **Subreddit**: {post['subreddit']}\n"
        markdown_output += f"  - **Score**: {post['score']}\n\n"

    markdown_output += "## Summary of Insights and Trends\n"
    markdown_output += f"{summary_text}\n"
    return markdown_output


def main():
    st.title("Reddit Topic Analysis")
    st.write("Analyze Reddit posts on any topic using AI-powered insights")

    # Sidebar for configurations
    with st.sidebar:
        st.header("Configuration")

        # Reddit API credentials
        st.subheader("Reddit API Credentials")
        app_id = st.text_input("Reddit App ID", value="GBFYIgcOttkM61vPhlztqw")
        app_secret = st.text_input(
            "Reddit App Secret", value="bODxWCRaXKxX71yey5JrOzlIBZrxeg", type="password"
        )
        user_agent = st.text_input("User Agent", value="testingLangchain")

        # Number of posts to analyze
        num_posts = st.slider(
            "Number of posts to analyze", min_value=1, max_value=20, value=5
        )

    # Main content area
    st.header("Topic Analysis")

    # Get available Ollama models
    available_models = get_available_models()
    if not available_models:
        st.error(
            "No Ollama models available. Please ensure Ollama is running and has models installed."
        )
        st.stop()

    # Model selection and topic input
    selected_model = st.selectbox("Select Ollama Model", available_models)
    topic = st.text_input("Enter a topic to analyze")

    if st.button("Analyze Topic"):
        if not topic:
            st.warning("Please enter a topic to analyze")
            return

        with st.spinner("Analyzing Reddit posts..."):
            try:
                # Initialize Reddit client
                reddit = praw.Reddit(
                    client_id=app_id, client_secret=app_secret, user_agent=user_agent
                )

                # Search Reddit
                post_analysis = search_reddit_posts(reddit, topic, num_posts)
                if not post_analysis:
                    st.error("No posts found for the given topic")
                    return

                # Generate and get AI analysis
                prompt = generate_analysis_prompt(topic, post_analysis)
                response = ollama.generate(model=selected_model, prompt=prompt)
                summary_text = response["response"]

                # Format and display results
                markdown_output = format_markdown_output(
                    topic, post_analysis, summary_text
                )
                st.markdown(markdown_output)

                # Add download button for the analysis
                st.download_button(
                    label="Download Analysis",
                    data=markdown_output,
                    file_name=f"reddit_analysis_{topic}.md",
                    mime="text/markdown",
                )

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()
