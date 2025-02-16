from flask import Flask, render_template, request, jsonify
from flask_caching import Cache
from riot_api import get_puuid, get_region, get_summoner_info, init_matchs_history, get_match_preview, get_champion_mastery, handle_match_data
import os

# Initialize Flask app
app = Flask(__name__)

# Configure Redis-based caching
# TODO Move to another file in future
app.config['CACHE_TYPE'] = 'RedisCache'
app.config['CACHE_REDIS_HOST'] = 'localhost'
app.config['CACHE_REDIS_PORT'] = 6379
app.config['CACHE_DEFAULT_TIMEOUT'] = 1200 # Cache timeout in seconds
cache = Cache(app)


# Homepage route
@app.route('/')
def index():
    """Homepage"""
    return render_template('index.html')


# Profile route
@app.route('/profile', methods=['POST'])
def profile():
    game_name = request.form.get('gameName')
    tag_line = request.form.get('tagLine')
    server = request.form.get('region')


    print(f"Game Name: {game_name}, Tag Line: {tag_line}, Region: {server}")

    try:
        # Convert server to Riot API region format
        region = get_region(server)

        # Get summoner's PUUID (unique identifier)
        puuid = get_puuid(region, game_name, tag_line)

        # Fetch summoner profile details
        summoner_profile = get_summoner_info(server, puuid)

        # Generate cache key for match history
        cache_key = f"match_history_{puuid}"
        match_history = cache.get(cache_key)

        # If match history is not found in cache, fetch and store it
        if not match_history:
            match_history = init_matchs_history(region, puuid)

            cache.set(cache_key, match_history)

        # Generate match preview and champion mastery details
        match_previews = get_match_preview(match_history)
        mastery = get_champion_mastery(puuid, server)

        # Render profile page with retrieved data
        return render_template(
            'profile.html',
            puuid=puuid,
            iconfile=summoner_profile['profileIcon'],
            level=summoner_profile['summonerLevel'],
            gameName=game_name,
            tagLine=tag_line,
            matches=match_previews,
            topChampions=mastery)

    except Exception as e:
        return render_template('error.html', message=str(e))
    

# Match details route
@app.route('/match/<match_id>')
def match_details(match_id):
    try: 
        match_id = int(match_id) # Ensure match_id is an integer
        puuid = request.args.get('puuid') # Get user's PUUID from query params

        # Retrieve match history from cache
        cache_key = f"match_history_{puuid}"
        match_history = cache.get(cache_key)

        if not match_history:
            raise Exception("Match history not found in cache. Please refresh your profile.")
        
        # Get specific match data from cached match history
        match_data = match_history[match_id]
        
        # Process match data for rendering
        match_overview = handle_match_data(match_data)

        # Render match details page
        return render_template(
            'matchDetails.html', 
            match_id=match_id,
            match=match_overview)
    
    except Exception as e:
        return render_template('error.html', message=str(e))

    
if __name__ == "__main__":
    app.run(debug=True)