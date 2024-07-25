import os
import json

class MemoryManager:
    def __init__(self, memory_file='memory.json'):
        self.memory_file = memory_file
        self.short_term_memory = []
        self.long_term_memory = []
        self.load_memory()

    def load_memory(self):
        if os.path.exists(self.memory_file):
            with open(self.memory_file, 'r') as f:
                self.long_term_memory = json.load(f)
        else:
            self.long_term_memory = []

    def save_to_memory(self, conversation_history):
        with open(self.memory_file, 'w') as f:
            json.dump(conversation_history, f)

    def update_short_term_memory(self, input_text):
        self.short_term_memory.append(input_text)
        if len(self.short_term_memory) > 10:  # limit short-term memory to the last 10 inputs
            self.short_term_memory.pop(0)

    def get_short_term_memory(self):
        return self.short_term_memory

    def get_long_term_memory(self):
        if os.path.exists(self.memory_file):
            with open(self.memory_file, 'r') as f:
                return json.load(f)
        return []
