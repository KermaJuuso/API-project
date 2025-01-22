from flask import Flask, render_template, request, jsonify
from riot_api import get_puuid, get_match_history

app = Flask(__name__)

@app.route('/')
def index():
    """Homepage"""
    return render_template('index.html')

@app.route('/profile', methods=['POST'])
def profile():
    game_name = request.form.get('gameName')
    tag_line = request.form.get('tagLine')
    region = request.form.get('region')

    print(f"Game Name: {game_name}, Tag Line: {tag_line}, Region: {region}")

    try:
        puuid = get_puuid(region, game_name, tag_line)
        matches = get_match_history(region, puuid)

        return render_template(
            'profile.html',
            puuid=puuid,
            gameName=game_name,
            tagLine=tag_line,
            matches=matches)

    except Exception as e:
        return render_template('error.html', message=str(e))


if __name__ == "__main__":
    app.run(debug=True)