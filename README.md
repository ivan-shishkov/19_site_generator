# Encyclopedia

This is an example of the website which was generated from Markdown source files with using of:

* Bootstrap 4
* Jinja2 template engine

Online version of the site is hosted on GitHub Pages and available [here](https://ivan-shishkov.github.io/19_site_generator/rendered_site/)

# Quickstart

All the site's templates is located in the `templates/` directory.

All the static files (styles, images, icons) is located in the `static/` directory.

All the Markdown source files with articles is located in the `articles/` directory.

Configuration info to generate site is is located in the `config.json` file.

To render site you need to launch the **build.py** script file.

For script launch need to install Python 3.5 and then install all dependencies:

```bash

$ pip install -r requirements.txt

```

Usage:

```bash

$ python3 build.py

```

Rendered site will be stored in the `rendered_site/` directory.

# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
