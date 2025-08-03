from mcp.server.fastmcp import FastMCP
from spotipy.oauth2 import SpotifyOAuth
import spotipy
import os, json


scope = "user-read-playback-state,user-modify-playback-state"

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=os.getenv("SPOTIFY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
        scope=scope,
    )
)

mcp = FastMCP("spotify")

@mcp.tool()
async def spotify_devices() -> str:
    """可以查詢你的所有 spotify 裝置，取得個別裝置的 id 與名稱"""

    devices = sp.devices()["devices"]
    if not devices:
        return "No devices found."
    return json.dumps(devices)

@mcp.tool()
async def spotify_search(query: str) -> str:
    """可以搜尋 spotify 上的音樂，並取 3 首音樂的曲名、藝人名、
    專輯名以及播放時需要的 rui

    Args:
        query: 搜尋關鍵字
    """

    results = sp.search(q=query, type="track", limit=3)
    items = results["tracks"]["items"]
    tracks = []
    for i, item in enumerate(items):
        tracks.append({
            "no": i,
            "name": item["name"],
            "artists": item["artists"],
            "uri": item["uri"],
            "album": item["album"]["name"]
        })
    if not tracks:
        return "No tracks found."
    return json.dumps(tracks)

@mcp.tool()
async def spotify_play(uri: str, device_id: str) -> str:
    """可以播放 spotify 上的音樂

    Args:
        uri: 音樂的 uri
        device_id: 播放裝置的 id
    """
    sp.start_playback(device_id=device_id, uris=[uri])
    return f"Playing {uri} on device {device_id}"

@mcp.tool()
async def spotify_pause(device_id: str) -> str:
    """可以暫停 spotify 上的音樂

    Args:
        device_id: 播放裝置的 id
    """
    sp.pause_playback(device_id=device_id)
    return f"Paused playback on device {device_id}"

@mcp.tool()
async def spotify_resume(device_id: str) -> str:
    """可以恢復 spotify 上的音樂

    Args:
        device_id: 播放裝置的 id
    """
    sp.start_playback(device_id=device_id)
    return f"Resumed playback on device {device_id}"

@mcp.tool()
async def spotify_now_playing() -> str:
    """可以查詢 spotify 上正在播放的音樂"""
    current_playback = sp.current_playback()
    if not current_playback:
        return "No music is currently playing."
    
    track = current_playback["item"]
    if not track:
        return "No music is currently playing."
    
    return json.dumps({
        "name": track["name"],
        "artists": track["artists"],
        "album": track["album"]["name"],
        "uri": track["uri"]
    })  

if __name__ == "__main__":
    try:
        # 執行伺服器
        mcp.run(transport='stdio')
    except KeyboardInterrupt:
        print("結束程式")
