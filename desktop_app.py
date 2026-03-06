import webview
from app import app
import threading

def start_server():
    app.run(host="127.0.0.1", port=5000)

if __name__ == '__main__':
    t = threading.Thread(target=start_server)
    t.daemon = True
    t.start()

    webview.create_window("Digital Audio Notary", "http://127.0.0.1:5000")
    webview.start()