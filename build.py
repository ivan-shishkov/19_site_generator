import os.path
import json
import os
from pathlib import Path
import shutil
import copy

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
    environment = Environment(
        autoescape=True,
        loader=file_loader,
    )
    return environment.get_template(template_filename)


def get_markdown_converter():
    return markdown.Markdown(
        extensions=['markdown.extensions.codehilite'],
    )


def add_article_destination_filepath(site_config_info):
    site_config_info_modified = copy.deepcopy(site_config_info)

    for article_info in site_config_info_modified['articles']:
        base_filename, _ = Path(article_info['source']).name.split('.')
        article_output_filename = '{}.{}'.format(
            base_filename.replace(' ', ''),
            'html',
        )
        article_info['destination'] = os.path.join(
            os.path.dirname(article_info['source']),
            article_output_filename,
        )
    return site_config_info_modified


def get_topic_articles(topic_info, articles_info):
    return {
        'title': topic_info['title'],
        'articles': [
            article_info
            for article_info in articles_info
            if article_info['topic'] == topic_info['slug']
        ],
    }


def get_table_of_contents(site_config_info):
    return [
        get_topic_articles(topic_info, site_config_info['articles'])
        for topic_info in site_config_info['topics']
    ]


def create_site_articles(articles_info, articles_dir, article_template,
                         markdown_converter, static_dir, output_dir):
    for article_info in articles_info:
        article_html = markdown_converter.reset().convert(
            source=load_text_data(
                filepath=os.path.join(articles_dir, article_info['source']),
            ),
        )
        article_output_dir = os.path.join(
            output_dir,
            os.path.dirname(article_info['destination']),
        )

        if not os.path.exists(article_output_dir):
            os.mkdir(article_output_dir)

        article_template.stream(
            content=article_html,
            title=article_info['title'],
            STATIC_URL=static_dir,
        ).dump(fp=os.path.join(output_dir, article_info['destination']))


def create_site_index_page(table_of_contents, index_page_template, static_dir,
                           output_dir):
    index_page_template.stream(
        topics=table_of_contents,
        STATIC_URL=static_dir,
    ).dump(fp=os.path.join(output_dir, 'index.html'))


def copy_static_files(source_dir, destination_dir):
    if os.path.exists(destination_dir):
        shutil.rmtree(destination_dir)

    shutil.copytree(
        src=source_dir,
        dst=destination_dir,
    )


def make_site(site_config_info, articles_dir, templates_dir,
              article_template_filename, index_page_template_filename,
              static_dir, output_dir):
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    create_site_articles(
        articles_info=site_config_info['articles'],
        articles_dir=articles_dir,
        article_template=get_template(
            templates_dir,
            article_template_filename,
        ),
        markdown_converter=get_markdown_converter(),
        static_dir=os.path.join('..', static_dir),
        output_dir=output_dir,
    )

    create_site_index_page(
        table_of_contents=get_table_of_contents(site_config_info),
        index_page_template=get_template(
            templates_dir,
            index_page_template_filename,
        ),
        static_dir=static_dir,
        output_dir=output_dir,
    )

    copy_static_files(
        source_dir=static_dir,
        destination_dir=os.path.join(output_dir, static_dir),
    )


def main():
    site_config_info = load_json_data('config.json')

    make_site(
        site_config_info=add_article_destination_filepath(site_config_info),
        articles_dir='articles',
        templates_dir='templates',
        article_template_filename='article.html',
        index_page_template_filename='index.html',
        static_dir='static',
        output_dir='rendered_site',
    )


if __name__ == '__main__':
    main()
