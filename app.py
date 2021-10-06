from flask import Flask, session, request, render_template,  make_response, flash, jsonify
from boggle import Boggle

app = Flask(__name__)
app.config['SECRET_KEY'] = "1234567abcdefgh"

boggle_game = Boggle()


@app.route('/')
def index():
    board = boggle_game.make_board()
    session['board'] = board
    bestscore =session.get("bestscore", 0)
    totalPlays = session.get("totalPlays", 0)

    return render_template('boogle-game.html', board=board, bestscore=bestscore, totalPlays=totalPlays)

@app.route("/check-word")
def check():
    word = request.args["word"]
    board = session["board"]
    response = boggle_game.check_valid_word(board, word)
    return jsonify({'result': response})


@app.route('/get-score', methods=["POST"])
def score():
    score = request.json["score"]
    bestscore = session.get("bestscore", 0)
    totalPlays = session.get("totalPlays", 0)

    session['totalPlays'] = totalPlays + 1
    session['bestscore'] = max(score, bestscore)

    return jsonify(highRecord=score > bestscore) 




