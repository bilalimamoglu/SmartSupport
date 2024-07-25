# src/utils/memory.py

import os
import json

class MemoryManager:
    def __init__(self, memory_file='memory.json'):
        """
        Initialize the MemoryManager with a file to store memory data.

        :param memory_file: The file path where memory data will be stored.
        """
        self.memory_file = memory_file
        self.short_term_memory = []
        self.long_term_memory = []
        self.load_memory()

    def load_memory(self):
        """
        Load memory data from the specified file.
        """
        if os.path.exists(self.memory_file):
            with open(self.memory_file, 'r') as f:
                self.long_term_memory = json.load(f)
        else:
            self.long_term_memory = []

    def save_to_memory(self, conversation_history):
        """
        Save conversation history to the memory file.

        :param conversation_history: The conversation history to save.
        """
        with open(self.memory_file, 'w') as f:
            json.dump(conversation_history, f)

    def update_short_term_memory(self, input_text):
        """
        Update the short-term memory with the latest input text.

        :param input_text: The input text to add to short-term memory.
        """
        self.short_term_memory.append(input_text)
        if len(self.short_term_memory) > 10:  # limit short-term memory to the last 10 inputs
            self.short_term_memory.pop(0)

    def get_short_term_memory(self):
        """
        Retrieve the current short-term memory.

        :return: The short-term memory list.
        """
        return self.short_term_memory

    def get_long_term_memory(self):
        """
        Retrieve the current long-term memory.

        :return: The long-term memory list.
        """
        if os.path.exists(self.memory_file):
            with open(self.memory_file, 'r') as f:
                return json.load(f)
        return []
