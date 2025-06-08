from miniweb.utils.config import load_config_from_args
from miniweb.templates.engine import init_template_engine, render_template
from miniweb.orm.models import Model
from miniweb.core.server import App
from demo import Book as Item

def main():
    config = load_config_from_args()

    Model.connect(config["DB_PATH"])
    Model.create_all()

    init_template_engine(
        enabled=config["TEMPLATES_ENABLED"],
        templates_dir="templates"
    )

    app = App()

    @app.route("/")
    def index(request):
        if config["TEMPLATES_ENABLED"]:
            return render_template("index.html", {})
        return "Hello, world! (Шаблонизатор отключен)"


    @app.route("/items")
    async def list_items(request):
        items = Item.all()
        if config["TEMPLATES_ENABLED"]:
            return render_template("items.html", {"items": items})
        return "\n".join(str(item) for item in items)


    app.run(
        host=config["HOST"],
        port=config["PORT"],
        debug=config["DEBUG"]
    )

if __name__ == "__main__":
    main()