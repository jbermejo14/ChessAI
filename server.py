from flask import Flask, request, jsonify
import subprocess
import chess
import chess.engine

app = Flask(__name__)

@app.route("/move", methods=["POST"])
def get_best_move():
    data = request.get_json()
    fen = data.get("fen")

    if not fen:
        return jsonify({"error": "No FEN provided"}), 400

    # Path to your Stockfish binary
    engine_path = "/root/stockfish-bin"

    try:
        with chess.engine.SimpleEngine.popen_uci(engine_path) as engine:
            board = chess.Board(fen)
            result = engine.play(board, chess.engine.Limit(time=0.5))
            return jsonify({"best_move": result.move.uci()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)