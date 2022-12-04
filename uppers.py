import hashlib

import httpx


def sha256(s):
    return hashlib.sha256(s.encode('utf-8')).hexdigest()


def calc_sign(coins, user_id, game_id):
    sign = sha256(f"leaderboard{coins}{user_id ^ game_id}ping")
    sign = sha256(f"{sign}catalog")
    return sign


def play(client, user_id, coins):
    if coins > 120:
        raise ValueError("Coins per game can not exceed 120")
    
    game_id = client.post("/start").json()["data"]["id"]
    
    r = client.post("/finish", json={
        "coins": coins,
        "id": game_id,
        "sign": calc_sign(coins, user_id, game_id),
        "tutorial": False,
        "victory": True
    }).json()
    
    if r["status"] != "ok":
        raise RuntimeError(r["message"])
    
    return True
    
    
def main():
    from sys import argv
    
    user_id, auth_token = int(argv[1]), argv[2]
    
    client = httpx.Client(
        base_url = "https://beeline-uppers.ru-prod2.kts.studio/api/game",
        headers = {
            "Authorization": f"Bearer {auth_token}"
        },
        timeout=7,
        verify=False
    )
        
    while True:
        try:
            play(client, user_id, 120)
        except Exception as e:
            print(f"Caught an exception! `{e}`. But THE COINS are more important...")


if __name__ == "__main__":
    main()
