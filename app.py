from flask import Flask, render_template, request, jsonify
from game_logic import ContextoGame
from word_data import get_random_target_word, get_word_list
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

try:
    # Initialize game
    word_list = get_word_list()
    target_word = get_random_target_word()
    game = ContextoGame(word_list, target_word)
except Exception as e:
    logging.error(f"Failed to initialize game: {str(e)}")
    raise

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/guess', methods=['POST'])
def guess():
    global game
    try:
        guess = request.form['guess']
        logging.debug(f"Received guess: {guess}")
        similarity, rank, message = game.rank_guess(guess)
        logging.debug(f"Similarity: {similarity}, Rank: {rank}, Message: {message}")
        
        if rank is None:
            return jsonify({"error": message}), 400
        
        # Sort guesses by rank (ascending, so lower ranks are at the top)
        sorted_guesses = sorted(game.guesses, key=lambda x: x[1])
        
        if game.is_correct(guess):
            top_words = game.get_top_words()
            return jsonify({
                "correct": True,
                "target": game.target_word,
                "guesses": [{"word": g[0], "rank": g[1]} for g in sorted_guesses],
                "latest_guess": {"word": guess, "rank": rank},
                "top_words": [{"word": w[0], "rank": w[1]} for w in top_words]
            })
        
        return jsonify({
            "correct": False,
            "guess": guess,
            "rank": rank,
            "guesses": [{"word": g[0], "rank": g[1]} for g in sorted_guesses],
            "latest_guess": {"word": guess, "rank": rank}
        })
    except Exception as e:
        logging.error(f"Error processing guess: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/new_game', methods=['POST'])
def new_game():
    global game
    try:
        target_word = get_random_target_word()
        game = ContextoGame(word_list, target_word)
        return jsonify({"message": "New game started"})
    except Exception as e:
        logging.error(f"Failed to start new game: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    try:
        app.run(debug=True)
    except Exception as e:
        logging.error(f"Failed to start server: {str(e)}")
        raise