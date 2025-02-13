from flask import Flask, render_template, request, jsonify
from flask_caching import Cache
from riot_api import get_puuid, get_region, get_summoner_info, init_matchs_history, get_match_preview, get_champion_mastery, handle_match_data
import os

app = Flask(__name__)

app.config['CACHE_TYPE'] = 'RedisCache'
app.config['CACHE_REDIS_HOST'] = 'localhost'
app.config['CACHE_REDIS_PORT'] = 6379
app.config['CACHE_DEFAULT_TIMEOUT'] = 300
cache = Cache(app)


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

        cache_key = f"match_history_{puuid}"
        match_history = cache.get(cache_key)


        if not match_history:
            match_history = init_matchs_history(region, puuid)

            cache.set(cache_key, match_history)


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
        match_id = int(match_id)
        puuid = request.args.get('puuid')

        cache_key = f"match_history_{puuid}"
        match_history = cache.get(cache_key)

        if not match_history:
            raise Exception("Match history not found in cache. Please refresh your profile.")

        match_data = match_history[match_id]
        
        match_overview = handle_match_data(match_data)

        return render_template(
            'matchDetails.html', 
            match_id=match_id,
            match=match_overview)
    
    except Exception as e:
        return render_template('error.html', message=str(e))

    


if __name__ == "__main__":
    app.run(debug=True)