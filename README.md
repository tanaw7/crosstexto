# Crosstexto: Cross-lingual Contexto Game (Using RAG)

## An attempt (still doesn't work quite right yet #TODO)

A Python-based web application that replicates the gameplay of [Contexto](https://contexto.me/), a word-guessing game where players guess a hidden word based on semantic similarity. Crosstexto extends this concept by adding cross-lingual support for English and Thai, using `langchain` with Retrieval-Augmented Generation (RAG) for word similarity computation.

## Features
- **Gameplay:** Guess a hidden word by entering words. Each guess is ranked based on its semantic closeness to the target word (lower rank = closer).
- **Cross-Lingual Support:** Guess in English or Thai interchangeably (e.g., target "queen" can be guessed as "queen" or "พระราชินี").
- **Web Interface:** Styled to resemble the official Contexto game, with a dark theme, input box, and color-coded guess list.
- **Color Coding:** Guesses are color-coded based on rank (green for close, yellow/orange for medium, red for far).
- **Recent Guess Highlight:** The most recent guess is displayed at the top, separately from the sorted guess list.
- **Gibberish Detection:** Basic heuristic to penalize nonsense words (e.g., "gdiofoidsnfuineuio") by assigning them a low rank.

## Tech Stack
- **Backend:** Flask (Python) for the web server.
- **Word Similarity:** `langchain` with `HuggingFaceEmbeddings` (`distiluse-base-multilingual-cased-v2`) and `FAISS` for vector search.
- **Frontend:** HTML/CSS with JavaScript for the web interface.
- **Dependencies:**
  - Flask
  - langchain
  - langchain-community
  - langchain-huggingface
  - sentence-transformers
  - faiss-cpu
  - numpy

## Project Structure
```
crosstexto/
├── app.py              # Flask backend and main application logic
├── game_logic.py       # Game logic, including word similarity and ranking
├── word_data.py        # Word list and target word selection (English and Thai)
├── templates/
│   └── index.html      # Frontend HTML/CSS/JavaScript for the game interface
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation (this file)
```

## Setup Instructions
1. **Clone the Repository** (if applicable):
   ```
   git clone <repository-url>
   cd crosstexto
   ```

2. **Create a Virtual Environment** (recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```
   pip install -r requirements.txt
   ```

4. **Run the Application**:
   ```
   python app.py
   ```
   The server will start at `http://127.0.0.1:5000`.

5. **Play the Game**:
   - Open your browser and go to `http://127.0.0.1:5000`.
   - Enter a word in the input box and press Enter to guess.
   - The most recent guess will appear at the top, with previous guesses sorted by rank below.
   - Guesses are color-coded: green (close, low rank), yellow/orange (medium), red (far, high rank).
   - Win by guessing the exact target word.

## Usage Notes
- **Cross-Lingual Guessing:** You can guess in English or Thai. For example, if the target is "queen," guessing "พระราชินี" (Thai for "queen") should rank high.
- **New Game:** Click the "New Game / เกมใหม่" button to start a new game with a different target word.
- **Known Issues:**
  - **Gibberish Words:** Nonsense words (e.g., "gdiofoidsnfuineuio") may still rank higher than expected. A basic heuristic penalizes such words, but further improvement (e.g., dictionary lookup) is needed.
  - **Color Gradient:** The color coding (green → yellow → orange → red) may need fine-tuning for better visual alignment with the official Contexto game.

## Future Improvements
- **Gibberish Detection:** Integrate a dictionary (e.g., `pyenchant` for English, a Thai dictionary) to better filter nonsense words.
- **Color Fine-Tuning:** Adjust the color gradient stops in `index.html` (`getColorForRank`) to better match the official Contexto game’s appearance.
- **Performance:** Switch to a lighter embedding model (e.g., `all-MiniLM-L6-v2`) for faster guess processing if needed.
- **Persistence:** Save game state (e.g., guesses, game number) to persist across server restarts.

## License
This project is for educational purposes and is not licensed for commercial use. The Contexto game concept, which inspired Crosstexto, belongs to its original creators.

## Acknowledgments
- Inspired by [Contexto](https://contexto.me/).
- Built with `langchain`, `sentence-transformers`, and Flask.