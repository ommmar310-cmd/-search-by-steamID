import sqlite3

# --- CONFIGURATION ---
DB_NAME = "my_steam_games.db"

def normalize_text(text):
    """
    Standardizes text so 'Part II' matches 'Part 2'.
    """
    text = text.lower()
    # Replace Roman Numerals with standard numbers for better matching
    text = text.replace(" ii ", " 2 ").replace(" iii ", " 3 ").replace(" iv ", " 4 ").replace(" v ", " 5 ")
    # Handle edge cases at the end of strings
    if text.endswith(" ii"): text = text[:-3] + " 2"
    if text.endswith(" iii"): text = text[:-4] + " 3"
    if text.endswith(" iv"): text = text[:-3] + " 4"
    if text.endswith(" v"): text = text[:-2] + " 5"
    return text

# --- MAIN EXECUTION ---
print(f"--- OPENING DATABASE: {DB_NAME} ---")

try:
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # Fetch all data once
    c.execute('''SELECT accounts.label, accounts.password, games.name 
                 FROM games 
                 JOIN accounts ON games.account_id = accounts.id''')
    all_data = c.fetchall()
    conn.close()
except Exception as e:
    print(f"Error: {e}")
    print("Make sure you ran 'update_db.py' first!")
    exit()

while True:
    user_input = input("\nEnter game name to search (or 'q' to quit): ").strip()
    
    if user_input.lower() == 'q':
        break
    
    # Prepare the search term
    search_query = normalize_text(user_input)
    
    found_count = 0
    print(f"\nSearching for exact sequence: '{search_query}'...")
    
    for row in all_data:
        acc_label, acc_pass, original_game_name = row
        
        # Prepare the game name from database
        normalized_game_name = normalize_text(original_game_name)
        
        # "If this sequence exists inside the name, show it."
        if search_query in normalized_game_name:
            print(f"✅ FOUND IN: {acc_label}")
            print(f"🔑 PASSWORD: {acc_pass}")
            
            print(f"🎮 MATCHED GAME: {original_game_name}")
            print("-" * 30)
            found_count += 1     
    if found_count == 0:
        print(f"❌ No game found containing '{user_input}'")
