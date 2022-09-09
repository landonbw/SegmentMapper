import requests

def query_endpoint(point, id, access_token):
    url = f"https://www.strava.com/api/v3/{point}/{id}?access_token={access_token}"
    resp = requests.get(url)
    if resp.status_code == 200:
        return resp.json()
    return None

def _activity_lookup(aid, access_token):
    return query_endpoint('activities', aid, access_token)

def _segment_lookup(sid, access_token):
    return query_endpoint('segments', sid, access_token)

def _segment_effort(id, access_token):
    return query_endpoint('segment_efforts', id, access_token)

def _activities(n, page, access_token):
    url = f"https://www.strava.com/api/v3/athlete/activities?per_page={n}&page={page}&access_token={access_token}"
    resp = requests.get(url)
    if resp.status_code == 200:
        return resp.json()
    return None


