import requests, time, sys
from supabase import create_client, Client
from datetime import datetime, timezone

RIOT_API_KEY = 'RGAPI-85df1326-355c-4a7f-9f86-c71056c90fcf'
SUPABASE_URL = 'https://fdhixdlmphjxxhcutrwu.supabase.co'
SUPABASE_API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZkaGl4ZGxtcGhqeHhoY3V0cnd1Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjU0MTkxNDYsImV4cCI6MjA4MDk5NTE0Nn0.XMgClwYxzPRxWvHEs_FJ34L53ARyhHYnX5ZSqGfjklY'

REFRESH_COOLDOWN = 120

supabase: Client = create_client(SUPABASE_URL, SUPABASE_API_KEY)

RANKS = ['IRON', 'BRONZE', 'SILVER', 'GOLD', 'PLATINUM', 'EMERALD', 'DIAMOND', 'MASTER', 'GRANDMASTER', 'CHALLENGER']
SERVERS = ['BR1', 'EUN1', 'EUW1', 'JP1', 'KR', 'LA1', 'LA2', 'ME1', 'NA1', 'OC1', 'RU', 'SG2', 'TR1', 'TW2', 'VN2']

def main():
    global username
    global fullusername
    global tagline
    global server
    global region

    skipInit = False

    if sys.argv.__len__() == 1:
        print()
    if sys.argv.__len__() == 3:
        print()
        fullusername = sys.argv[1]
        server = sys.argv[2].upper()
        skipInit = True
    elif sys.argv.__len__() > 3:
        prRed("Too many arguments were added to the command line. Executing as normal...\n\n")
    elif sys.argv.__len__() < 3:
        prRed("Too few arguments were added to the command line. Executing as normal...\n\n")

    prLightPurple("Easy LP Tracker")
    print(" by ",end="")
    prCyan("Xoffy\n")
    prRed("This app is an experiment. Press 'CTRL+C' to exit.\nPlease note it can take a couple games to process LP gain properly.\n\n")
    
    try:
        if not skipInit:
            prCyan("Please enter your Riot username and tag:\n")
            fullusername = input()
        
        while '#' not in fullusername:
            prRed("Please ensure your full Riot username and tag are entered.\n")
            fullusername = input()
        splitusername = fullusername.split('#')
        username = splitusername[0]
        tagline = splitusername[1]
        
        if not skipInit:
            prCyan("Input your server, possible options are:\n")
            prPurple("BR1  EUN1  EUW1  JP1  KR  LA1  LA2  ME1  NA1  OC1  RU  SG2  TR1  TW2  VN2\n")
            server = input().upper()
            deleteLine()
        
        while server not in SERVERS:
            prRed("Given server is not valid, please re-enter server.\n")
            server = input().upper()
            deleteLine()
        
        if server == 'BR1' or server == 'LA1' or server == 'LA2' or server == 'NA1':
            region = 'AMERICAS'
        elif server == 'KR' or server == 'JP1':
            region = 'ASIA'
        elif server == 'EUN1' or server == 'EUW1' or server == 'ME1' or server == 'TR1' or server == 'RU':
            region = 'EUROPE'
        elif server == 'OC1' or server == 'SG2' or server == 'TW2' or server == 'VN2':
            region = 'SEA'
        else:
            region = 'UNKNOWN'

        prCyan(f"Your username is {fullusername} at {server} within {region}\n")
    except KeyboardInterrupt:
            prRed("Closing app...")
            exit(" Closed")

    getPUUID()

    while True:
        try:
            calculateData()
            fillMatches()
            countdown(int(REFRESH_COOLDOWN))
            deleteLine()
        except KeyboardInterrupt:
            prRed("Closing app...")
            exit(" Closed")

def getPUUID():
    global uuid

    response = requests.get(f'https://asia.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{username}/{tagline}?api_key={RIOT_API_KEY}')
    
    uuid = response.json()['puuid']

    response = (supabase.table("players").select("uuid").execute())

    uuidexists = False
    for x in response.data:
        if x['uuid'] == uuid: uuidexists = True

    if not uuidexists:
        supabase.table("players").insert({"uuid": uuid, "username": username, "tag": tagline}).execute()
        

def calculateData():
    response = requests.get(f"https://{server}.api.riotgames.com/lol/league/v4/entries/by-puuid/{uuid}?api_key={RIOT_API_KEY}")
    if not response.json():
        print("Summoner does not exist...\nTrying again in")
        plainCountdown(5)
        main()
    tier = response.json()[0]['tier']
    tierNo = response.json()[0]['rank']
    currentLP = response.json()[0]['leaguePoints']
    wins = response.json()[0]['wins']
    losses = response.json()[0]['losses']

    #currRank = tier + " " + tierNo + " - " + str(currentLP) + " LP"
    gamesPlayed = wins+losses
    winRate = (wins / gamesPlayed) * 100

    #print(currRank+" at "+str(round(winRate))+"% WR"+" with "+str(gamesPlayed)+" games played")

    if tier == "GOLD":
        prYellow("GOLD "+str(tierNo))
    elif tier == "PLATINUM":
        prCyan("PLATINUM "+str(tierNo))
    elif tier == "EMERALD":
        prGreen("EMERALD "+str(tierNo))
    elif tier == "DIAMOND":
        prLightPurple("DIAMOND "+str(tierNo))
    elif tier == "MASTER":
        prPurple("MASTER "+str(tierNo))
    elif tier == "GRANDMASTER":
        prRed("GRANDMASTER "+str(tierNo))
    elif tier == "CHALLENGER":
        prCyan("CHALLENGER "+str(tierNo))
    else:
        print(tier + " " + str(tierNo),end="")

    print(" - " + str(currentLP) + " LP at ",end="")
    if round(winRate) > 49:
        prGreen(str(round(winRate))+"% WR")
    else:
        prRed(str(round(winRate))+"% WR")
    
    print(" with "+str(gamesPlayed)+" games played")

    response = (supabase.table("player_details").select("uuid").execute())
    uuidexists = False
    for x in response.data:
        if x['uuid'] == uuid: uuidexists = True

    if not uuidexists:
        supabase.table("player_details").insert({"uuid": uuid, "last_updated": datetime.now(timezone.utc).isoformat(),
                                                 "tier": tier, "tierNo": tierNo, "currLP": currentLP, "wins": wins, "losses": losses, "games_played": gamesPlayed}).execute()
    else:
        supabase.table("player_details").update({"uuid": uuid, "last_updated": datetime.now(timezone.utc).isoformat(),
                                                 "tier": tier, "tierNo": tierNo, "currLP": currentLP, "wins": wins, "losses": losses, "games_played": gamesPlayed}).eq("uuid", uuid).execute()

def fillMatches():
    response = requests.get(f"https://{region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{uuid}/ids?type=ranked&start=0&count=1&api_key={RIOT_API_KEY}")
    matchID = response.json()[0]

    response = requests.get(f"https://{region}.api.riotgames.com/lol/match/v5/matches/{matchID}?api_key={RIOT_API_KEY}")
    #get player number in game
    count = 0
    for x in response.json()['metadata']['participants']:
        if x == uuid: break
        count+=1
    
    playerMatchInfo = response.json()['info']['participants'][count]
    win = playerMatchInfo['win']
    kills = playerMatchInfo['kills']
    deaths = playerMatchInfo['deaths']
    assists = playerMatchInfo['assists']
    role = playerMatchInfo['teamPosition']

    response = (supabase.table("player_details").select("*").eq("uuid", uuid).execute())

    query = supabase.table("matches").select("*")
    query = query.eq("associated_uuid", uuid)
    query = query.order("time_added", desc=True)

    secondresponse = query.execute()

    diffLP = calcRank(response.data, secondresponse.data)

    thirdresponse = (supabase.table("matches").select("match_id").execute())

    matchexists = False
    for x in thirdresponse.data:
        if x['match_id'] == matchID: matchexists = True

    if not matchexists:
        supabase.table("matches").insert({"match_id": matchID, "associated_uuid": uuid, "win": win, "kills": kills, "deaths": deaths, "assists": assists,
                                      "tier_after": response.data[0]['tier'], "tierNo_after": response.data[0]['tierNo'], "LP_after": response.data[0]['currLP'], "LP_diff": diffLP,
                                      "time_added": datetime.now(timezone.utc).isoformat(), "role": role}).execute()
        if diffLP >= 0:
            prCyan(str(datetime.now().strftime('%I:%M%p'))+" | ")
            print(f'Updated one new match! (+{diffLP} LP)')
        else:
            prCyan(str(datetime.now().strftime('%I:%M%p'))+" | ")
            print(f'Updated one new match! ({diffLP} LP)')
    else:
        prCyan(str(datetime.now().strftime('%I:%M%p'))+" | ")
        print('Matches up to date!')
    
def calcRank(a, b):
    if len(a) == 0 or len(b) == 0:
        return 0

    try:
        a_tier = a[0]['tier']
        b_tier = b[0]['tier_after']

        a_tierNo = a[0]['tierNo']
        b_tierNo = b[0]['tierNo_after']

        a_LP = a[0]['currLP']
        b_LP = b[0]['LP_after']
    except:
        return 0

    if a_tierNo == b_tierNo and a_tier == b_tier:
        return a_LP - b_LP
    
    return 100 - a_LP

def countdown(t):
    while t:
        try:
            mins, secs = divmod(t, 60)
            timer = '{:02d}:{:02d}'.format(mins, secs)
            print('  Waiting '+timer, end='\r')  # Overwrite the line each second
            time.sleep(1)
            t -= 1
        except KeyboardInterrupt:
            prRed("Closing app...")
            exit(" Closed")

    prCyan(str(datetime.now().strftime('%I:%M%p'))+" | ")
    print("Now checking again...")

def plainCountdown(t):
    while t:
        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        print('  '+timer, end='\r')  # Overwrite the line each second
        time.sleep(1)
        t -= 1

def deleteLine(): print('\033[1A' + '\033[K', end='')
def prRed(s): print("\033[91m{}\033[00m".format(s),end="")
def prGreen(s): print("\033[92m{}\033[00m".format(s),end="")
def prYellow(s): print("\033[93m{}\033[00m".format(s),end="")
def prLightPurple(s): print("\033[94m{}\033[00m".format(s),end="")
def prPurple(s): print("\033[95m{}\033[00m".format(s),end="")
def prCyan(s): print("\033[96m{}\033[00m".format(s),end="")
def prLightGray(s): print("\033[97m{}\033[00m".format(s),end="")
def prBlack(s): print("\033[90m{}\033[00m".format(s),end="")  # Corrected from 98 to 90 (standard ANSI)

if __name__ == "__main__":
    main()