import sqlite3

conn = sqlite3.connect("players.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS players (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    aim INTEGER,
    sense INTEGER,
    reaction INTEGER,
    luck INTEGER,
    rating INTEGER
)
""")
conn.commit()

def get_player(user_id, username):
    cursor.execute("SELECT * FROM players WHERE user_id=?", (user_id,))
    player = cursor.fetchone()
    if not player:
        cursor.execute("""
        INSERT INTO players VALUES (?, ?, 50, 50, 50, 50, 1000)
        """, (user_id, username))
        conn.commit()
        return get_player(user_id, username)
    return player

def update_rating(user_id, rating):
    cursor.execute("UPDATE players SET rating=? WHERE user_id=?", (rating, user_id))
    conn.commit()