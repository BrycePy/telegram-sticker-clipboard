from flask import Flask, jsonify, request, Response
from flask_cors import CORS
import requests
import auth_token
import json
from functools import lru_cache
import os

from sticker_downloader import StickerDownloader
from sticker_downloader import File as StickerFile

downloader = StickerDownloader(auth_token.TELEGRAM)

app = Flask(__name__)
CORS(app, send_wildcard=True)

@app.after_request
def apply_caching(response):
    response.headers["cache-control"] = "public, max-age=3600, immutable"
    return response

@lru_cache(maxsize=1000)
def packProxyPing(packName):
    params = {'name': packName}
    res = downloader._api_request('getStickerSet', params)
    if res is None:
        return None
    stickers = res['result']['stickers']
    return jsonify(stickers)

@app.route('/pack', methods=['POST'])
def packProxy():
    return packProxyPing(request.json['packName'])

@app.route('/sticker/<file_id>')
@lru_cache(maxsize=10000)
def stickerProxy(file_id):
    cache_path = os.path.join('cache', file_id)
    cache_path_header = os.path.join('cache', file_id+"-headers")
    if os.path.isfile(cache_path) and os.path.isfile(cache_path_header):
        with open(cache_path, 'rb') as f:
            content = f.read()

        with open(cache_path_header, 'r') as f:
            headers = json.load(f)
        
        return Response(content, 200, {'content-type': 'image/webp'})

    file_path = downloader._api_request('getFile', {'file_id': file_id})['result']['file_path']
    url = 'https://api.telegram.org/file/bot{}/{}'.format(auth_token.TELEGRAM, file_path)

    resp = requests.get(url)
    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    headers = [(name, value) for (name, value) in resp.raw.headers.items()
               if name.lower() not in excluded_headers]

    with open(cache_path, 'wb') as f:
        f.write(resp.content)

    with open(cache_path_header, 'w') as f:
        json.dump(headers, f)

    response = Response(resp.content, resp.status_code, {'content-type': 'image/webp'})
    return response