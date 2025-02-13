# League of Legends Player Lookup

This is a Flask-based web application that allows users to search for League of Legends player profiles. The app fetches data from the Riot Games API to display profile information, match history, and champion details. It also allows users to view detailed information about each match.

## Features
- Search for a player by their game name and tag line.
- View the player's profile information (summoner level, profile icon).
- Show the player's 20 most recent match results.
- View detailed match information, including champion data, match summary, and individual player stats (e.g., kills, deaths, assists, minions killed).
- Match history data is cached using Redis for faster access.

## Technologies Used
- **Flask**: The web framework for building the application.
- **Riot Games API**: Provides access to player profile and match data.
- **Redis**: Used for caching match history to improve performance.
- **Docker**: Docker Desktop is used for containerization, including running Redis in a container.

## How It Works
1. **Profile Search**: Enter a League of Legends player’s game name and tag line in the search form.
2. **Match History**: After searching for a player, the app fetches the 20 most recent match results using the Riot Games API. This data is cached in Redis to reduce API calls and load times.
3. **Match Details**: Click on a match from the history to view detailed information about the match, including team summaries, individual player stats, and more.

## Setup Instructions
1. **Docker**: Install Docker Desktop if you plan to use Redis via Docker.
2. **Riot API Key**: You will need a Riot Games API key to access player data. Store your key in a `.env` file in the root directory of the project with the following format:
   ```env
   API_KEY=your_api_key


### Running the App

1. **Clone this repository**:
   ```bash
   git clone https://github.com/yourusername/lol-player-lookup.git
   cd lol-player-lookup
2. **Install the required dependencies**: Ensure Docker Desktop is running on your machine.
    ```bash
    pip install -r requirements.txt

3. **Start Redis**:
    ```bash
    docker run -p 6379:6379 redis
4. **Run the Flask app**:
    ```bash
    pyhton app.py
