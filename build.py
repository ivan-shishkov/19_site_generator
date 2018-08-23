import os.path
import json

from jinja2 import Environment, FileSystemLoader


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


def main():
    pass


if __name__ == '__main__':
    main()
