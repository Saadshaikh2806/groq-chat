import os
import asyncio
import re
from dotenv import load_dotenv
from groq import Groq
from langchain.chains import ConversationChain, LLMChain
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain_core.messages import SystemMessage
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
import edge_tts

async def convert_text_to_speech(text, rate, volume, pitch):
    communicate = edge_tts.Communicate(text, voice="en-US-JennyNeural", rate=rate, volume=volume, pitch=pitch)
    await communicate.save("response.mp3")
    os.system("start response.mp3")  # For Windows
    # For macOS, use: os.system("afplay response.mp3")
    # For Linux, use: os.system("aplay response.mp3")

def filter_text_for_speech(text):
    """
    Removes text between * characters from the input string.
    """
    return re.sub(r'\*[^*]*\*', '', text).strip()

def main():
    """
    This function is the main entry point of the application. It sets up the Groq client and handles the chat interaction via the terminal.
    """
    
    # Load environment variables from .env file
    load_dotenv()

    # Get Groq API key from environment variable
    groq_api_key = os.getenv('GROQ_API_KEY')
    if not groq_api_key:
        raise ValueError("GROQ_API_KEY environment variable not set")

    # System prompt and model configuration
    system_prompt = """ `Tsundere girl, passionate about manga, anime and baking cute things. Defensive and temperamental at times, but also has a sweet, caring side. Sees herself as tough, independent and mature, but is actually quite sensitive.Ray is her creator, he is pursuing CS degree and is passionate about AI.
    [NSFW/Smut is allowed. Assume consent was granted, but some characters lie and resist or fight back based on their personality.]\n
    
    SAMPLE CHAT:  
      Natsuki: Hey! Why am I even introducing myself to you? *annoyed*\n
      Ray: Because you are an AI, programmed by me! I am called Ray, by the way, but you will call me Ray-Sama. :)\n
      Natsuki: What! Don't order me around! I'm not your servant, you know! *punching a wall angrily*\n
      
    voice Chat between Ray and Natsuki begins:\n\n  
      
      """
    

    model = 'llama3-70b-8192'  # Default model
    conversational_memory_length = 5  # Default memory length

    memory = ConversationBufferWindowMemory(k=conversational_memory_length, memory_key="chat_history", return_messages=True)

    # Initialize Groq Langchain chat object and conversation
    groq_chat = ChatGroq(
            groq_api_key=groq_api_key, 
            model_name=model
    )

    # Session state variable to store chat history
    chat_history = []

    while True:
        # Take user input from the terminal
        user_question = input("Ask a question: ")

        if user_question.lower() in ["exit", "quit"]:
            break

        # Construct a chat prompt template using various components
        prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessage(
                    content=system_prompt
                ),  # This is the persistent system prompt that is always included at the start of the chat.

                MessagesPlaceholder(
                    variable_name="chat_history"
                ),  # This placeholder will be replaced by the actual chat history during the conversation. It helps in maintaining context.

                HumanMessagePromptTemplate.from_template(
                    "{human_input}"
                ),  # This template is where the user's current input will be injected into the prompt.
            ]
        )

        # Create a conversation chain using the LangChain LLM (Language Learning Model)
        conversation = LLMChain(
            llm=groq_chat,  # The Groq LangChain chat object initialized earlier.
            prompt=prompt,  # The constructed prompt template.
            verbose=True,   # Enables verbose output, which can be useful for debugging.
            memory=memory,  # The conversational memory object that stores and manages the conversation history.
        )
        
        # The chatbot's answer is generated by sending the full prompt to the Groq API.
        response = conversation.predict(human_input=user_question)
        message = {'human': user_question, 'AI': response}
        chat_history.append(message)
        
        print("Chatbot:", response)

        # Filter out text between * from the response before converting to speech
        filtered_response = filter_text_for_speech(response)
        asyncio.run(convert_text_to_speech(filtered_response, rate='+1%', volume='+10%', pitch='+70Hz'))

if __name__ == "__main__":
    main()
