Project Overview: AI Chatbot with Voice Synthesis
This project implements an interactive AI chatbot with text-to-speech capabilities. The chatbot is designed to engage users in conversations, leveraging natural language processing and speech synthesis technologies. The application is built using Python and integrates various APIs and libraries to provide a seamless and responsive user experience.

Features
Interactive Chatbot:

Utilizes the Groq API for natural language processing and conversation handling.
Maintains conversational context using memory buffers, enabling coherent multi-turn conversations.
Text-to-Speech (TTS) Integration:

Converts chatbot responses to speech using the Edge TTS library.
Allows customization of speech parameters, including rate, volume, and pitch.
Environment Configuration:

Uses environment variables to manage API keys and other configurations securely.
Components
Environment Setup:

.env file to store environment variables such as the Groq API key.
dotenv library to load these variables into the application.
Chatbot Functionality:

groq and langchain libraries for language processing and conversation management.
Customizable conversation memory using ConversationBufferWindowMemory.
Prompt Template:

Templates to structure the conversation prompts and maintain a consistent interaction flow.
Voice Synthesis:

edge_tts library to convert text responses to speech.
Function to filter out specific text patterns (e.g., actions or emotions denoted by *) from being converted to speech.
