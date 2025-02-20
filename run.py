from App import create_app
from config.default import Config

app = create_app(Config)


if __name__ == '__main__':
    app.run()
    # app.run(debug=True)