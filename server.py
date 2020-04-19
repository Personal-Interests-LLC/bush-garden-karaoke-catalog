from config import app
import os

app.config.from_object(os.environ['APP_SETTINGS'])

@app.route('/')
def main():
    return 'Shalom!'


if __name__ == '__main__':
    app.run()
