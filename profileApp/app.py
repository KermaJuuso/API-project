from flask import Flask, render_template, request, jsonify
from riot_api import get_puuid, get_region, get_summoner_info, init_matchs_history, get_match_preview, get_champion_mastery, get_match_data

app = Flask(__name__)

@app.route('/')
def index():
    """Homepage"""
    return render_template('index.html')

@app.route('/profile', methods=['POST'])
def profile():
    game_name = request.form.get('gameName')
    tag_line = request.form.get('tagLine')
    server = request.form.get('region')


    print(f"Game Name: {game_name}, Tag Line: {tag_line}, Region: {server}")

    try:
        region = get_region(server)
        puuid = get_puuid(region, game_name, tag_line)
        summoner_profile = get_summoner_info(server, puuid)
        match_history = init_matchs_history(region, puuid)
        history_preview = get_match_preview(match_history)
        mastery = get_champion_mastery(puuid, server)

        return render_template(
            'profile.html',
            puuid=puuid,
            iconfile=summoner_profile['profileIcon'],
            level=summoner_profile['summonerLevel'],
            gameName=game_name,
            tagLine=tag_line,
            matches=history_preview,
            topChampions=mastery)

    except Exception as e:
        return render_template('error.html', message=str(e))
    
@app.route('/match/<match_id>')
def match_details(match_id):
    try: 
        match_data = get_match_data(match_id)
        
        return render_template(
            'matchDetails.html', 
            match_id=match_id,
            match=match_data)
    
    except Exception as e:
        return render_template('error.html', message=str(e))

    


if __name__ == "__main__":
    app.run(debug=True)