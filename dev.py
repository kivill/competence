#!/usr/bin/env python3
from app import app

def run():
    app.run(host='127.0.0.1', port=5000, debug=True, use_reloader=True, threaded=True)


if __name__ == '__main__':
    run()