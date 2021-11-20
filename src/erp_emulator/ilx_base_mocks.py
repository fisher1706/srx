from __main__ import app

@app.route('/')
def home():
    return "<h1>This is ILX mock server for automation tests<h1>"