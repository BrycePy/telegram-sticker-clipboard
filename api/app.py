from flask import Flask, jsonify, request, Response
from flask_cors import CORS
import requests
import auth_token

from sticker_downloader import StickerDownloader
from sticker_downloader import File as StickerFile

downloader = StickerDownloader(auth_token.TELEGRAM)

app = Flask(__name__)
CORS(app)

@app.route('/pack', methods=['POST'])
def packProxy():
    pack_name = request.json['packName']
    data = downloader.get_sticker_set(pack_name)
    data['files'] = [f.name for f in data['files']]
    response = jsonify(data)
    return response

@app.route('/sticker/<filename>')
def stickerProxy(filename):
    url = f"https://api.telegram.org/file/bot{auth_token.TELEGRAM}/stickers/{filename}"
    print(url)

    resp = requests.get(url)
    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    headers = [(name, value) for (name, value) in resp.raw.headers.items()
               if name.lower() not in excluded_headers]

    response = Response(resp.content, resp.status_code, headers)
    return response