# miniweb/utils/cli.py

import sys
from miniweb.utils.config import load_config_from_args
from miniweb.templates.engine import init_template_engine, render_template
from miniweb.orm import models
from miniweb.core.server import App

def main():
    """
    Точка входа для команды запуска сервера.
    Разбирает CLI, инициализирует все подсистемы и стартует HTTP-сервер.
    """
    # 1. Загружаем параметры из аргументов
    config = load_config_from_args()

    # 2. Настраиваем ORM (подключение к БД и создание таблиц)
    models.connect(config["DB_PATH"])
    models.Model.create_all()

    # 3. Инициализируем шаблонизатор Jinja2
    init_template_engine(
        enabled=config["TEMPLATES_ENABLED"],
        templates_dir="templates"  # при необходимости можно сделать настраиваемым
    )

    # 4. Создаём экземпляр приложения и регистрируем демонстрационные маршруты
    app = App()

    # Простой синхронный маршрут
    @app.route("/")
    def index(request):
        if config["TEMPLATES_ENABLED"]:
            return render_template("index.html", {})
        return "Hello, world! (Templates disabled)"

    # Асинхронный маршрут, демонстрирующий работу ORM
    @app.route("/items")
    async def list_items(request):
        items = models.Item.all()  # предполагаем, что модель Item описана в miniweb.orm.models
        if config["TEMPLATES_ENABLED"]:
            return render_template("items.html", {"items": items})
        return "\n".join(str(item) for item in items)

    # 5. Запуск сервера
    app.run(
        host=config["HOST"],
        port=config["PORT"],
        debug=config["DEBUG"]
    )

if __name__ == "__main__":
    # Позволяет запускать напрямую: python -m miniweb.utils.cli
    main()