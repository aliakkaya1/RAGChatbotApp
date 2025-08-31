RAG AI Chatbot (iOS + FastAPI)
Hey there. So this is a complete AI chatbot app i built, it's got everything from the python server to the iOS interface. The whole point was to mess around with RAG (Retrieval-Augmented Generation), which is a pretty cool way to make a chatbot that actually knows what its talking about because you give it specific documents to read.

The "Hybrid" System - whats the deal?
I split the project into two main parts, just to keep the main app fast.

load_data.py (The heavy lifting): This script is the one you run yourself to get the bot's knowledge. It scrapes the websites, calls the OpenAI API to make the embeddings (this is the part that costs money), and saves the finished "brain" into a folder. It's slow, you only run it when you need to update things.

main.py (The actual server): This is the fast part. it just loads the files that the other script already made. So the server starts up quick and is ready to go.

Tech I Used,
Backend: Python, FastAPI, LangChain, OpenAI, FAISS

Frontend: Swift, SwiftUI

How to Get This Running
Okay so first, you need a few things on your machine: Python 3.9+, Xcode 15, and git.

1. Get the code:
Just clone the repo like you normally would.

git clone <your-repository-url>
cd <your-repository-name>

2. Backend Setup:

a. The python environment thing:
This keeps all the packages in one spot, its good practice.

python3 -m venv venv
source venv/bin/activate

b. Install all the stuff:
This will install everything from the requirements file.

pip install -r requirements.txt

c. Your API key:
The app wont work without an OpenAI API key.

make a new file, call it .env.

Open it up and paste your key in, like this:

OPENAI_API_KEY="sk-..."
Running the App
You need two terminals. one for the backend, and xcode for the frontend.

1. First, build the bot's brain:
You gotta run the data loader script first. this builds the knowledge base files from the web links.

python3 load_data.py

2. Run the server:
In your terminal, start the FastAPI server and just leave it running in the background.


uvicorn main.app --reload
It should be running on http://127.0.0.1:8000.

3. Run the iOS App

Open the .xcodeproj file in Xcode.

Pick a simulator.

Hit the Play button (Cmd+R).

And yeah, it should just work after that. you can start chatting with the bot.