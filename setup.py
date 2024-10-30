import os


def create_directory_structure():
    # Define the base directory structure
    dirs = [
        'app',
        'app/auth',
        'app/main',
        'app/static/css',
        'app/static/js',
        'app/templates',
        'app/templates/auth',
        'app/templates/admin',
        'app/templates/customer',
        'app/templates/professional',
        'instance'
    ]

    # Create directories
    for dir_path in dirs:
        os.makedirs(dir_path, exist_ok=True)

    # Create empty __init__.py files
    init_files = [
        'app/__init__.py',
        'app/auth/__init__.py',
        'app/main/__init__.py'
    ]

    for file_path in init_files:
        open(file_path, 'a').close()


if __name__ == '__main__':
    create_directory_structure()