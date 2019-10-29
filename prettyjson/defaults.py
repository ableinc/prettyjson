import sys, getpass

settings_filename = f'/Users/{getpass.getuser()}/.prettyjson/settings.json' if sys.platform == 'darwin' else f'C:\Program Files\.prettyjson/settings.json'
settings_dir = f'/Users/{getpass.getuser()}/.prettyjson/' if sys.platform == 'darwin' else f'C:\Program Files\.prettyjson'
