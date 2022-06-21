from flask import Flask
from bp_netflix.views import netflix_blueprint


def create_and_config_app(config_path):                     # Метод для создания app
    app = Flask(__name__)
    app.register_blueprint(netflix_blueprint)               # Регистрируем блюпринт main_blueprint
    app.config.from_pyfile(config_path)                     # Берем конфиги из файла конфигурации
    return app


app = create_and_config_app('config.py')


if __name__ == '__main__':
    app.run()
