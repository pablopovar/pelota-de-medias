import json, os, threading, time
from datetime import date, timedelta
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse
from urllib.request import Request, urlopen
ROOT = Path(__file__).parent; DATA_FILE = ROOT / "data" / "argentina-results.json"; API_URL = "https://v3.football.api-sports.io/fixtures"; LEAGUES_URL = "https://v3.football.api-sports.io/leagues"; LOCK = threading.Lock()
def normalize(item):
    fixture, league, teams, goals = item.get("fixture", {}), item.get("league", {}), item.get("teams", {}), item.get("goals", {})
    national = "Argentina" in {teams.get("home", {}).get("name"), teams.get("away", {}).get("name")}
    return {"id":fixture.get("id"),"date":fixture.get("date","")[:10],"competition":league.get("name","Argentina football"),"type":"national" if national else "club","time":fixture.get("status",{}).get("short","TBD"),"home":teams.get("home",{}).get("name","Home"),"away":teams.get("away",{}).get("name","Away"),"homeScore":goals.get("home") if goals.get("home") is not None else "–","awayScore":goals.get("away") if goals.get("away") is not None else "–"}
def fetch_initial_60_days():
    key=os.getenv("API_FOOTBALL_KEY")
    if not key: return None
    headers={"x-apisports-key":key}; start=(date.today()-timedelta(days=59)).isoformat(); end=date.today().isoformat()
    # Ask the provider for Argentina's actual competitions, then query each one directly.
    request=Request(f"{LEAGUES_URL}?country=Argentina&season={date.today().year}",headers=headers)
    with urlopen(request,timeout=30) as response: leagues=json.load(response).get("response",[])
    ids=sorted({str(item.get("league",{}).get("id")) for item in leagues if item.get("league",{}).get("id")})
    matches=[]
    for index, league_id in enumerate(ids):
        request=Request(f"{API_URL}?league={league_id}&season={date.today().year}&from={start}&to={end}",headers=headers)
        with urlopen(request,timeout=30) as response: matches.extend(normalize(item) for item in json.load(response).get("response",[]))
        if index < len(ids)-1: time.sleep(6.1) # stay below the free plan's 10 requests/minute limit
    request=Request(f"{API_URL}?team=26&from={start}&to={end}",headers=headers)
    with urlopen(request,timeout=30) as response: matches.extend(normalize(item) for item in json.load(response).get("response",[]))
    return {"updatedAt":date.today().isoformat(),"range":{"from":start,"to":end},"matches":list({match["id"]:match for match in matches if match["id"] is not None}.values())}
def load_data():
    if DATA_FILE.exists(): return json.loads(DATA_FILE.read_text())
    with LOCK:
        if DATA_FILE.exists(): return json.loads(DATA_FILE.read_text())
        data=fetch_initial_60_days()
        if data is None: return {"matches":[],"configurationRequired":True}
        DATA_FILE.parent.mkdir(parents=True,exist_ok=True); DATA_FILE.write_text(json.dumps(data)); return data
class Handler(SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed=urlparse(self.path)
        if parsed.path=="/api/results":
            data=load_data(); requested_date=parse_qs(parsed.query).get("date",[None])[0]
            if requested_date: data={**data,"matches":[item for item in data["matches"] if item["date"]==requested_date]}
            self.send_response(200);self.send_header("Content-Type","application/json");self.end_headers();self.wfile.write(json.dumps(data).encode());return
        return super().do_GET()
if __name__=="__main__": os.chdir(ROOT); ThreadingHTTPServer(("0.0.0.0",80),Handler).serve_forever()
