<<<<<<< HEAD
import webview
from app import app

if __name__ == '__main__':
    webview.create_window("Digital Audio Notary", "http://127.0.0.1:5000")
    app.run(host="127.0.0.1", port=5000)
=======
import webview
from app import app

if __name__ == '__main__':
    webview.create_window("Digital Audio Notary", "http://127.0.0.1:5000")
    app.run(host="127.0.0.1", port=5000)
>>>>>>> ff7d1f8aeb76fd3585a1b833f713ba1743e2d869
    webview.start()