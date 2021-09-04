from back import app, api

if __name__ == "__main__":
    api.register(app)
    app.run(port=8000)
