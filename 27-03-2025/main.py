from Frontend.GUI import (
    GraphicalUserInterface,
    SetAssistantStatus,
    ShowTextToScreen,
    TempDirectoryPath,
    SetMicrophoneStatus,
    AnswerModifier,
    QueryModifier,
    GetMicrophoneStatus,
    GetAssistantStatus
)
from Backend.Model import FirstLayerDMM
from Backend.RealtimeSearchEngine import RealtimeSearchEngine
from Backend.Automation import Automation
from Backend.SpeechToText import SpeechRecognition
from Backend.Chatbot import ChatBot
from Backend.TextToSpeech import TextToSpeech
from dotenv import dotenv_values
from asyncio import run
from time import sleep
import subprocess
import threading
import json
import os
import sys

# Initialize environment variables with defaults
env_vars = dotenv_values(".env")
Username = env_vars.get("Username", "User")  # Default if not found
Assistantname = env_vars.get("Assistantname", "Assistant")  # Default if not found
DefaultMessage = f'{Username}. I am doing well. How may I help you?'

# Global process list for proper cleanup
subprocesses = []

Functions = ["open", "close", "play", "system", "content", "google search", "youtube search"]

def ensure_data_directory():
    """Ensure Data directory exists"""
    if not os.path.exists('Data'):
        os.makedirs('Data')
        # Create empty ChatLog.json if it doesn't exist
        with open('Data/ChatLog.json', 'w', encoding='utf-8') as f:
            json.dump([], f)

def ShowDefaultChatIfNoChats():
    """Initialize chat files with default message if empty"""
    ensure_data_directory()
    try:
        with open('Data/ChatLog.json', "r+", encoding='utf-8') as file:
            if len(file.read()) < 5:
                file.seek(0)
                file.truncate()
                json.dump([], file)
                
                with open(TempDirectoryPath('Database.data'), 'w', encoding='utf-8') as db_file:
                    db_file.write("")
                
                with open(TempDirectoryPath('Responses.data'), "w", encoding='utf-8') as res_file:
                    res_file.write(DefaultMessage)
    except Exception as e:
        print(f"Error initializing chat files: {e}")

def ReadChatLogJson():
    """Read and parse chat log JSON file"""
    try:
        with open('Data/ChatLog.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def ChatLogIntegration():
    """Format chat log for display in GUI"""
    json_data = ReadChatLogJson()
    formatted_chatlog = ""
    for entry in json_data:
        if entry["role"] == "user":
            formatted_chatlog += f"{Username}: {entry['content']}\n"
        elif entry["role"] == "assistant":
            formatted_chatlog += f"{Assistantname}: {entry['content']}\n"

    with open(TempDirectoryPath('Database.data'), 'w', encoding='utf-8') as file:
        file.write(AnswerModifier(formatted_chatlog))

def ShowChatsOnGUI():
    """Display chats in the GUI"""
    try:
        with open(TempDirectoryPath('Database.data'), "r", encoding='utf-8') as file:
            data = file.read()
            if data.strip():
                with open(TempDirectoryPath('Responses.data'), "w", encoding='utf-8') as file:
                    file.write(data)
    except FileNotFoundError:
        pass

def InitialExecution():
    """Initialize application state"""
    SetMicrophoneStatus("False")
    ShowTextToScreen("")
    ShowDefaultChatIfNoChats()
    ChatLogIntegration()
    ShowChatsOnGUI()

def cleanup_processes():
    """Clean up any running subprocesses"""
    for proc in subprocesses:
        try:
            proc.terminate()
        except:
            pass

def MainExecution():
    """Main execution logic for processing user queries"""
    TaskExecution = False
    ImageExecution = False
    ImageGenerationQuery = ""

    SetAssistantStatus("Listening...")
    Query = SpeechRecognition()
    if not Query:  # If speech recognition failed
        SetAssistantStatus("Available...")
        return False
        
    ShowTextToScreen(f"{Username}: {Query}")
    SetAssistantStatus("Thinking...")
    Decision = FirstLayerDMM(Query)

    print(f"\nDecision: {Decision}\n")

    G = any(i.startswith("general") for i in Decision)
    R = any(i.startswith("realtime") for i in Decision)

    Merged_query = " and ".join(
        [" ".join(i.split()[1:]) for i in Decision if i.startswith("general") or i.startswith("realtime")]
    )

    # Check for image generation request
    for query in Decision:
        if "generate" in query:
            ImageGenerationQuery = str(query)
            ImageExecution = True
    
    # Check for automation tasks
    for query in Decision:
        if not TaskExecution and any(query.startswith(func) for func in Functions):
            run(Automation(list(Decision)))
            TaskExecution = True

    # Handle image generation
    if ImageExecution:
        image_data_path = os.path.join('Frontend', 'Files', 'ImageGeneration.data')
        with open(image_data_path, "w") as file:
            file.write(f"{ImageGenerationQuery},True")

        try:
            p1 = subprocess.Popen(
                ['python', os.path.join('Backend', 'ImageGeneration.py')],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE,
                shell=False
            )
            subprocesses.append(p1)
        except Exception as e:
            print(f"Error starting ImageGeneration.py: {e}")
    
    # Process general and realtime queries
    if G and R:
        SetAssistantStatus("Searching...")
        Answer = RealtimeSearchEngine(QueryModifier(Merged_query))
        ShowTextToScreen(f"{Assistantname}: {Answer}")
        SetAssistantStatus("Answering...")
        TextToSpeech(Answer)
        return True
    else:
        for query in Decision:
            if "general" in query:
                SetAssistantStatus("Thinking...")
                QueryFinal = query.replace("general", "")
                Answer = ChatBot(QueryModifier(QueryFinal))
                ShowTextToScreen(f"{Assistantname}: {Answer}")
                SetAssistantStatus("Answering...")
                TextToSpeech(Answer)
                return True
            elif "realtime" in query:
                SetAssistantStatus("Searching...")
                QueryFinal = query.replace("realtime ", "")
                Answer = RealtimeSearchEngine(QueryModifier(QueryFinal))
                ShowTextToScreen(f"{Assistantname}: {Answer}")
                SetAssistantStatus("Answering...")
                TextToSpeech(Answer)
                return True
            elif "exit" in query.lower():
                Answer = "Okay, Bye!"
                ShowTextToScreen(f"{Assistantname}: {Answer}")
                SetAssistantStatus("Answering...")
                TextToSpeech(Answer)
                cleanup_processes()
                sys.exit(0)

def FirstThread():
    """Background thread for processing user input"""
    while True:
        try:
            CurrentStatus = GetMicrophoneStatus()
            if CurrentStatus == "True":
                MainExecution()
            else:
                AIStatus = GetAssistantStatus()
                if "Available..." not in AIStatus:
                    SetAssistantStatus("Available...")
                sleep(0.1)
        except Exception as e:
            print(f"Error in FirstThread: {e}")
            sleep(1)

def SecondThread():
    """GUI thread"""
    try:
        GraphicalUserInterface()
    except Exception as e:
        print(f"Error in GUI thread: {e}")

if __name__ == "__main__":
    # Initialize the application
    InitialExecution()

    # Register cleanup function
    import atexit
    atexit.register(cleanup_processes)

    # Start threads
    try:
        thread1 = threading.Thread(target=FirstThread, daemon=True)
        thread2 = threading.Thread(target=SecondThread)
        
        thread1.start()
        thread2.start()
        
        # Wait for GUI thread to complete
        thread2.join()
    except KeyboardInterrupt:
        cleanup_processes()
    except Exception as e:
        print(f"Main execution error: {e}")
        cleanup_processes()