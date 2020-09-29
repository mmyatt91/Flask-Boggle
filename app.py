from flask import Flask, request, render_template, jsonify, session
from flask_debugtoolbar import DebugToolbarExtension
from boggle import Boggle

app = Flask(__name__)
app.config["SECRET_KEY"] = "QMyMan21"
toolbar = DebugToolbarExtension(app)

boggle_game = Boggle()

@app.route("/")
def homepage():
    """Display the Board"""
    board = boggle_game.make_board()
    session['board'] = board
    highscore = session.get("highscore", 0)
    nplays = session.get("nplays", 0)

    return render_template("main.html", board=board, highscore=highscore,
    nplays=nplays)

@app.route("/check-word")
def check_word():
    """Check Validity of Word"""
    word = request.args["word"]
    board = session["board"]
    res = boggle_game.check_valid_word(board, word)

    return jsonify({'result': res})

@app.route("/post-score", methods=["POST"])
def post_score():
    """Accept score, update plays, update high score, if needed"""
    score = request.json["score"]
    highscore = session.get("highscore", 0)
    nplays = session.get ("nplays", 0)

    session['nplays'] = nplays + 1
    session['highscore'] = max(score, highscore)

    return jsonify(brokeRecord=score > highscore)