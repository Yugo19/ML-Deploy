import os
from openai import OpenAI

client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key=os.getenv("OPENAI_KEY"),
)


messages = [{"role": "assistant", "content": "How can I help?"}]

# Function to display the chat history
def display_chat_history(messages):
    for message in messages:
        print(f"{message['role'].capitalize()}: {message['content']}")

# Function to get the assistant's response
def get_assistant_response(messages):
    try:
        r = client.chat.completions.create(
            model="gpt-4",  # Update this based on the model you intend to use
            messages=[{"role": m["role"], "content": m["content"]} for m in messages],
        )
        response = r.choices[0].message.content
        return response
    except Exception as e:
        print(f"An error occurred: {e}")
        return "Sorry, I can't process your request right now."

# Function to get a response to a user's prompt
def get_response(prompt: str):
    # Add the user's message to the chat history
    messages.append({"role": "user", "content": prompt})
    
    # Get the assistant's response and add it to the chat history
    response = get_assistant_response(messages)
    messages.append({"role": "assistant", "content": response})
    
    # Display the updated chat history
    display_chat_history(messages)
    
    return response