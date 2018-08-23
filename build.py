import os.path
import json
from pathlib import Path

from jinja2 import Environment, FileSystemLoader
import markdown


def load_text_data(filepath):
    if not os.path.exists(filepath):
        return None
    with open(filepath, 'r') as file:
        return file.read()


def load_json_data(filepath):
    if not os.path.exists(filepath):
        return None
    with open(filepath, 'r') as file:
        return json.load(file)


def get_template(templates_dir, template_filename):
    file_loader = FileSystemLoader(templates_dir)
    env = Environment(loader=file_loader)

    return env.get_template(template_filename)


def get_markdown_converter():
    return markdown.Markdown(
        extensions=['markdown.extensions.codehilite'],
    )


def add_destination_filepath(articles_info):
    for article_info in articles_info:
        base_filename, _ = Path(article_info['source']).name.split('.')
        article_html_filename = '{}.{}'.format(base_filename, 'html')

        article_info['destination'] = os.path.join(
            os.path.dirname(article_info['source']),
            article_html_filename,
        )


def main():
    pass


if __name__ == '__main__':
    main()
