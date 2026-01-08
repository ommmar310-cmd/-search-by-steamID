import sqlite3
import requests

# --- CONFIGURATION ---
API_KEY = ""
DB_NAME = "my_steam_games.db"

# YOUR DATA LIST
ACCOUNTS_DB = [
    {"label": "", "password": "", "steam_identifier": "", "manual_games": []},
]

# --- FUNCTIONS ---

def init_db():
    """Create the tables if they don't exist."""
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # Create Accounts Table
    c.execute('''CREATE TABLE IF NOT EXISTS accounts 
                 (id INTEGER PRIMARY KEY, label TEXT, password TEXT, steam_identifier TEXT)''')
    # Create Games Table (linked to Accounts)
    c.execute('''CREATE TABLE IF NOT EXISTS games 
                 (id INTEGER PRIMARY KEY, account_id INTEGER, name TEXT,
                  FOREIGN KEY(account_id) REFERENCES accounts(id))''')
    conn.commit()
    conn.close()

def get_steam_id(user_input):
    if str(user_input).isdigit():
        return user_input
    url = f"http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key={API_KEY}&vanityurl={user_input}"
    try:
        r = requests.get(url, timeout=10)
        data = r.json()
        if data.get('response', {}).get('success') == 1:
            return data['response']['steamid']
        return None
    except:
        return None

def get_games_api(steam_id):
    url = f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={API_KEY}&steamid={steam_id}&format=json&include_appinfo=true"
    try:
        r = requests.get(url, timeout=10)
        data = r.json()
        game_names = []
        if "games" in data.get("response", {}):
            for game in data["response"]["games"]:
                game_names.append(game["name"])
        return game_names
    except:
        return []

# --- MAIN EXECUTION ---
print("--- STARTING DATABASE UPDATE ---")
init_db()

conn = sqlite3.connect(DB_NAME)
c = conn.cursor()

# 1. Clear old data to avoid duplicates (Full Refresh)
c.execute("DELETE FROM games")
c.execute("DELETE FROM accounts")
conn.commit()
print("Old data cleared. Fetching fresh data...\n")

for account in ACCOUNTS_DB:
    label = account['label']
    print(f"Processing: {label}...", end=" ")
    
    # Insert Account into DB
    c.execute("INSERT INTO accounts (label, password, steam_identifier) VALUES (?, ?, ?)",
              (label, account['password'], account['steam_identifier']))
    account_db_id = c.lastrowid
    
    current_games = []
    
    # A. Fetch from Steam API
    steam_id = get_steam_id(account['steam_identifier'])
    if steam_id:
        api_games = get_games_api(steam_id)
        if api_games:
            current_games.extend(api_games)
            
    # B. Add Manual Games
    if account['manual_games']:
        current_games.extend(account['manual_games'])
    
    # Remove duplicates
    current_games = list(set(current_games))
    
    # Insert Games into DB
    if current_games:
        for game_name in current_games:
            c.execute("INSERT INTO games (account_id, name) VALUES (?, ?)", (account_db_id, game_name))
        print(f"Success ({len(current_games)} games saved)")
    else:
        print("No games found.")

conn.commit()
conn.close()
print("\n--- DATABASE UPDATE COMPLETE ---")
print(f"Data saved to file: {DB_NAME}")
