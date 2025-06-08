# miniweb/templates/engine.py

from jinja2 import Environment, FileSystemLoader, TemplateNotFound
from typing import Optional

# Глобальные переменные модуля
_env: Optional[Environment] = None
_templates_enabled: bool = True

def init_template_engine(enabled: bool = True, templates_dir: str = "templates") -> None:
    """
    Инициализирует движок шаблонов Jinja2 или отключает его.

    :param enabled: флаг включения шаблонизатора
    :param templates_dir: директория с файлами-шаблонами
    """
    global _env, _templates_enabled
    _templates_enabled = enabled

    if not enabled:
        # явно сбрасываем окружение, шаблонизация недоступна
        _env = None
        return

    # Создаём Jinja2-окружение с файловым загрузчиком
    _env = Environment(
        loader=FileSystemLoader(templates_dir),
        autoescape=True        # безопасность HTML-шаблонов
    )

def render_template(template_name: str, context: dict) -> str:
    """
    Рендерит указанный шаблон с переданным контекстом.

    :param template_name: имя файла шаблона (например, "index.html")
    :param context: данные для подстановки в шаблон
    :return: итоговый текст (HTML)
    :raises RuntimeError: если шаблонизатор отключён или не инициализирован
    :raises FileNotFoundError: если шаблон не найден в каталоге
    """
    if not _templates_enabled:
        raise RuntimeError("Шаблонизатор отключён настройками приложения")
    if _env is None:
        raise RuntimeError("Шаблонное окружение не инициализировано")

    try:
        template = _env.get_template(template_name)
    except TemplateNotFound:
        raise FileNotFoundError(f"Шаблон «{template_name}» не найден")

    # Выполняем рендер и возвращаем строку
    return template.render(**context)