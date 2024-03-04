from flask import Flask, Blueprint, request, jsonify
from enum import Enum
from api_common import Role, role_from_str

app = Flask(__name__)


class GameLogic:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.winner = Role.UNKNOWN
        self.lines = {Role.HUMAN: 0, Role.ARTIFICIAL_INTELLIGENCE: 0}
        self.predicted_winner = Role.UNKNOWN


game_logic = GameLogic()

@app.route("/set_lines/<role>/<lines>")
def set_lines(role, lines):
    print(role)
    print(lines)
    role_id = role_from_str(str=role)

    game_logic.lines[role_id] = int(lines)

    if game_logic.lines[Role.HUMAN] > game_logic.lines[Role.ARTIFICIAL_INTELLIGENCE]:
        game_logic.predicted_winner = Role.HUMAN
    elif game_logic.lines[Role.HUMAN] == game_logic.lines[Role.ARTIFICIAL_INTELLIGENCE]:
        game_logic.predicted_winner = Role.UNKNOWN
    else:
        game_logic.predicted_winner = Role.ARTIFICIAL_INTELLIGENCE
    
    if game_logic.lines[role_id] == 10:
        game_logic.winner = game_logic.predicted_winner
    
    return "OK"


@app.route("/reset")
def reset():
    game_logic.reset()
    return "OK"


@app.route("/stats")
def get_winner():
    return jsonify({"winner": str(game_logic.winner), "predicted_winner": str(game_logic.predicted_winner)})


app.run()