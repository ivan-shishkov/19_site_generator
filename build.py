import os.path


def load_text_data(filepath):
    if not os.path.exists(filepath):
        return None
    with open(filepath, 'r') as file:
        return file.read()


def main():
    pass


if __name__ == '__main__':
    main()
