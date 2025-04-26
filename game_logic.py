from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
import numpy as np
import re

class ContextoGame:
    def __init__(self, word_list, target_word):
        self.word_list = word_list
        self.target_word = target_word.lower()
        self.guesses = []
        
        # Initialize embedding model (lightweight multilingual model)
        self.embeddings = HuggingFaceEmbeddings(model_name="distiluse-base-multilingual-cased-v2")
        
        # Create a vector store for the word list using FAISS
        self.vector_store = FAISS.from_texts(word_list, self.embeddings)
        
        # Precompute embeddings for the word list
        self.word_embeddings = {word: self.embeddings.embed_query(word) for word in word_list}
        
        # Cache the target word embedding
        self.target_embedding = self.embeddings.embed_query(self.target_word)
        # Cache embeddings for guesses
        self.guess_cache = {}

    def get_similarity(self, guess):
        guess = guess.lower()
        # Check if guess is in the cache
        if guess in self.guess_cache:
            guess_embedding = self.guess_cache[guess]
        else:
            guess_embedding = self.embeddings.embed_query(guess)
            self.guess_cache[guess] = guess_embedding
        
        # Compute cosine similarity
        dot_product = np.dot(guess_embedding, self.target_embedding)
        norm = np.linalg.norm(guess_embedding) * np.linalg.norm(self.target_embedding)
        similarity = dot_product / norm if norm != 0 else 0
        return similarity

    def is_valid_word(self, word):
        # Simple heuristic: a valid word should contain only letters (English or Thai) and spaces
        # English letters (a-z, A-Z) or Thai characters (U+0E00–U+0E7F)
        pattern = r'^[a-zA-Z\u0E00-\u0E7F\s]+$'
        return bool(re.match(pattern, word))

    def rank_guess(self, guess):
        if not guess.strip():
            return None, None, "Guess cannot be empty"

        guess = guess.lower()
        similarity = self.get_similarity(guess)
        # Compute absolute rank by comparing against all words in the vector store, including the guess
        all_similarities = []
        # Add the guess to the list of words to rank
        guess_embedding = self.guess_cache[guess]
        all_words = self.word_list + [guess] if guess not in [w.lower() for w in self.word_list] else self.word_list
        
        for word in all_words:
            if word.lower() == guess.lower():
                word_embedding = guess_embedding
            else:
                word_embedding = self.word_embeddings.get(word)
                if word_embedding is None:
                    # This shouldn't happen, but just in case
                    word_embedding = self.embeddings.embed_query(word)
                    self.word_embeddings[word] = word_embedding
            dot_product = np.dot(word_embedding, self.target_embedding)
            norm = np.linalg.norm(word_embedding) * np.linalg.norm(self.target_embedding)
            word_similarity = dot_product / norm if norm != 0 else 0
            all_similarities.append((word, word_similarity))
        
        # Sort by similarity (descending)
        sorted_similarities = sorted(all_similarities, key=lambda x: x[1], reverse=True)
        # Find the rank of the guess (guaranteed to exist since we added the guess)
        rank = next(i + 1 for i, (word, _) in enumerate(sorted_similarities) if word.lower() == guess.lower())
        
        # Penalize gibberish words
        if not self.is_valid_word(guess):
            # Apply a rank penalty (e.g., push rank to a high value)
            rank = max(rank, 5000)  # Ensure gibberish ranks low (far from target)

        self.guesses.append((guess, rank))
        return similarity, rank, "Valid guess"

    def is_correct(self, guess):
        return guess.lower() == self.target_word

    def get_top_words(self, n=10):
        # Use RAG to retrieve the top N closest words to the target
        results = self.vector_store.similarity_search_with_score(self.target_word, k=n)
        top_words = [(doc.page_content, i + 1) for i, (doc, _) in enumerate(results)]
        return top_words