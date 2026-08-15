import io
import os
import re

from flask import Flask, render_template, request, jsonify, send_file
import yt_dlp

app = Flask(__name__)

URL_RE = re.compile(r'^https?://', re.IGNORECASE)


def safe_filename(name: str) -> str:
    name = name or 'indirilen-dosya'
    return re.sub(r'[\\/*?:"<>|]', '_', name).strip()[:150]


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/download', methods=['POST'])
def download():
    data = request.get_json(silent=True) or {}
    url = (data.get('url') or '').strip()
    media_type = data.get('type', 'video')

    if not url or not URL_RE.match(url):
        return jsonify({'error': 'Geçerli bir link girin.'}), 400

    if media_type not in ('video', 'audio'):
        media_type = 'video'

    outtmpl = os.path.join(app.instance_path, '%(id)s.%(ext)s')
    os.makedirs(app.instance_path, exist_ok=True)

    if media_type == 'audio':
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'noplaylist': True,
            'format': 'bestaudio/best',
            'outtmpl': outtmpl,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
    else:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'noplaylist': True,
            'format': 'bv*+ba/best',
            'format_sort': ['codec:h264:aac'],
            'outtmpl': outtmpl,
            'merge_output_format': 'mp4',
        }

    filename = None
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            if media_type == 'audio':
                filename = os.path.splitext(filename)[0] + '.mp3'

        if not filename or not os.path.exists(filename):
            return jsonify({'error': 'Dosya oluşturulamadı.'}), 500

        with open(filename, 'rb') as f:
            file_bytes = f.read()

        title = safe_filename(info.get('title'))
        ext = os.path.splitext(filename)[1]
        download_name = f'{title}{ext}'
        mimetype = 'audio/mpeg' if media_type == 'audio' else 'video/mp4'

        return send_file(
            io.BytesIO(file_bytes),
            as_attachment=True,
            download_name=download_name,
            mimetype=mimetype,
        )
    except yt_dlp.utils.DownloadError:
        return jsonify({'error': 'Bu link desteklenmiyor veya video indirilemedi.'}), 400
    except Exception:
        return jsonify({'error': 'Beklenmeyen bir hata oluştu.'}), 500
    finally:
        if filename and os.path.exists(filename):
            try:
                os.remove(filename)
            except OSError:
                pass


if __name__ == '__main__':
    app.run(debug=True, port=5001)
