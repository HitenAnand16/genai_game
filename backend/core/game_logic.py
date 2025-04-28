# game_logic.py

class Node:
    def __init__(self, word):
        self.word = word
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None
        self.words = set()  # for duplicate checking

    def add_word(self, word):
        if word in self.words:
            return False  # Duplicate - Game Over
        new_node = Node(word)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
        self.words.add(word)
        return True

    def get_history(self):
        history = []
        current = self.head
        while current:
            history.append(current.word)
            current = current.next
        return history

# Global counter
global_counter = {}

# In-memory cache
cache = {}

# Profanity filter
bad_words = {"fuck", "shit", "bitch", "asshole", "bastard", "dick"}

def check_profanity(word):
    return any(bad_word in word.lower() for bad_word in bad_words)
