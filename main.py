import chess.pgn
import jsonpickle
import os
from flask import Flask, request
from flask_cors import CORS

#UPLOAD_FOLDER = 'C:/Users/DeLL/PycharmProjects/chess-pgn-parser'
UPLOAD_FOLDER = ''
ALLOWED_EXTENSIONS = {'pgn'}


app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class PgnObject:
    source = ""
    to = ""
    fen = ""

    def __init__(self, source, to, fen):
        self.source = source
        self.to = to
        self.fen = fen


def getSubStrings(uci, position):
    return [uci[i:i+2] for i in range(position, len(uci) - 1, 2)]

@app.route("/", methods=["GET", "POST"])
def pgnToFen():


    if request.method == 'POST':
        file = request.files['file']
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))

        pgn = open(file.filename)

        first_game = chess.pgn.read_game(pgn)

        board = first_game.board()

        pgnData = []

        index = 0

        for move in first_game.mainline_moves():
            board.push(move)
            uciMove = board.uci(move)

            pieceMove = getSubStrings(uciMove,0)
            source = pieceMove[0]
            to = pieceMove[1]

            fen = board.fen()
            objToSend= PgnObject(source, to, fen)
            pgnData.append(objToSend)
            index = index + 1

            pgnDataJSON = jsonpickle.encode(pgnData)


        return pgnDataJSON

    else:
        return 0

if __name__=="__main__":
    app.run(host="0.0.0.0",debug=True)



