from App import create_app
from config.config import Config

app = create_app(Config)


if __name__ == '__main__':
    app.run()
    # app.run(debug=True)