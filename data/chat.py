from dataclasses import dataclass, field
from enum import Enum
import os
from typing import List
from util.fs import get_bootstrap_dir
from dataclasses_json import DataClassJsonMixin
import time

class ChatRole(Enum):
    USER = 'user'
    ASSISTANT = 'assistant'

@dataclass
class ChatItem(DataClassJsonMixin):
    message: str
    role: ChatRole

@dataclass
class ChatHistory(DataClassJsonMixin):
    last_saved: float
    messages: List[ChatItem]

def load_chat_history(chatID: str):
    boot_dir = get_bootstrap_dir()
    chat_dir = os.path.join(boot_dir, "chat")
    filename = os.path.join(chat_dir, f"{chatID}.json")
    if not os.path.exists(filename):
        raise ValueError(f"No chat history found for: {chatID}")
    
    with open(filename, "r") as file:
        history = ChatHistory.from_json(file.read())
        return history

def save_chat_history(chatID: str, history: ChatHistory):
    history.last_saved = time.time()
    boot_dir = get_bootstrap_dir()
    chat_dir = os.path.join(boot_dir, "chat")
    filename = os.path.join(chat_dir, f"{chatID}.json")
    with open(filename, "w") as file:
        file.write(history.to_json())

def get_latest_chat_id():
    boot_dir = get_bootstrap_dir()
    chat_dir = os.path.join(boot_dir, "chat")
    if not os.path.exists(chat_dir):
        raise FileNotFoundError("Chat directory does not exist.")

    chat_files = [f for f in os.listdir(chat_dir) if f.endswith('.json')]
    if not chat_files:
        raise FileNotFoundError("No chat files found in the chat directory.")

    # Assuming the filenames are timestamps, the lowest number would be the earliest timestamp
    earliest_chat_file = min(chat_files, key=lambda x: int(x.split('.')[0]))
    return os.path.splitext(earliest_chat_file)[0]

def new_chat():
    boot_dir = get_bootstrap_dir()
    chat_dir = os.path.join(boot_dir, "chat")
    if not os.path.exists(chat_dir):
        os.makedirs(chat_dir)
    timestamp = str(int(time.time()))
    filename = os.path.join(chat_dir, f"{timestamp}.json")
    new_history = ChatHistory(last_saved=time.time(), messages=[])
    with open(filename, "w") as file:
        file.write(new_history.to_json())
    return new_history


