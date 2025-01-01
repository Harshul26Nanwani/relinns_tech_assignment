import requests
from bs4 import BeautifulSoup
import openai
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = "open-api-key"
def fetch_website_content(url):
    try:
        print("Fetching website content...")
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the website: {e}")
        return None

def extract_information(soup):
    try:
        title = soup.title.string if soup.title else "No Title Found"
        paragraphs = [p.get_text(strip=True) for p in soup.find_all('p') if p.get_text(strip=True)]
        return {"title": title, "content": paragraphs}
    except Exception as e:
        print(f"Error extracting information: {e}")
        return None

def process_data(data):
    title = data.get('title', "No Title")
    content = data.get('content', [])
    processed_content = "\n".join(content[:5])
    return f"Website Title: {title}\n\nContent:\n{processed_content}"


def chatbot_response(user_input, context):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Context: {context}"},
                {"role": "user", "content": user_input}
            ],
            temperature=0.7,
            max_tokens=100,
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        print(f"Error generating response: {e}")
        return "Sorry, I couldn't process that."

def run_chatbot():
    url = input("Enter the website URL (e.g., https://example.com): ").strip()
    if not url.startswith("http://") and not url.startswith("https://"):
        print("Invalid URL. Please include 'http://' or 'https://'")
        return

    soup = fetch_website_content(url)
    if not soup:
        print("Failed to load the website. Please check the URL.")
        return

    data = extract_information(soup)
    if not data:
        print("Failed to extract information from the website.")
        return

    context = process_data(data)
    print("\nChatbot ready! Ask questions about the website content. Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Chatbot: Goodbye!")
            break
        response = chatbot_response(user_input, context)
        print("Chatbot:", response)

if __name__ == "__main__":
    run_chatbot()
