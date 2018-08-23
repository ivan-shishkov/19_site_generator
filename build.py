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


def make_site_articles(articles_info, articles_dir,
                       article_template, markdown_converter, output_dir):
    for article_info in articles_info:
        article_html = markdown_converter.reset().convert(
            source=load_text_data(
                filepath=os.path.join(articles_dir, article_info['source']),
            ),
        )
        article_html_dir = os.path.join(
            output_dir,
            os.path.dirname(article_info['destination']),
        )

        if not os.path.exists(article_html_dir):
            os.mkdir(article_html_dir)

        article_template.stream(
            content=article_html,
            title=article_info['title'],
        ).dump(fp=os.path.join(
            output_dir,
            article_info['destination'],
        ))


def make_site(site_config_info, articles_dir, templates_dir,
              article_template_filename, index_page_template_filename,
              output_dir):
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    markdown_converter = get_markdown_converter()

    make_site_articles(
        articles_info=site_config_info['articles'],
        articles_dir=articles_dir,
        article_template=get_template(
            templates_dir,
            article_template_filename,
        ),
        markdown_converter=markdown_converter,
        output_dir=output_dir,
    )


def main():
    site_config_info = load_json_data('config.json')

    add_destination_filepath(
        articles_info=site_config_info['articles']
    )

    make_site(
        site_config_info=site_config_info,
        articles_dir='articles',
        templates_dir='templates',
        article_template_filename='article.html',
        index_page_template_filename='index.html',
        output_dir='rendered_site',
    )


if __name__ == '__main__':
    main()
