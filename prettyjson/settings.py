import sys, json, os, getpass
try:
    from preflight import Preflight
    from defaults import settings_dir, settings_filename
except ImportError:
    from prettyjson.preflight import Preflight
    from prettyjson.defaults import settings_filename, settings_dir


class Settings:
    def __init__(self, args):
        self.args = args
        self.organized_args = []
        self.settings = {}
        self._organize()

    def _organize(self):
        def replacer(arg):
            return arg.replace('--', '').upper()
        half = int(len(self.args) / 2)
        for index, arg in enumerate(range(0, half)):
            if index >= 1:
                arg = index + 1
            value = arg if self.args[arg].find('--') != -1 else (arg + 1)
            self.organized_args.append([replacer(self.args[value]), self.args[value + 1]])
        self._convert_to_json()

    def _convert_to_json(self):
        for setting in self.organized_args:
            self.settings[setting[0]] = setting[1]   

    def setItems(self):
        def json_dump(settings):
            return json.dumps(settings, indent=2, sort_keys=True)
        prev_settings = None
        if os.path.isfile(settings_filename):
            prev_settings = json.loads(open(settings_filename, encoding='utf8').read())
            for key, value in self.settings.items():
                prev_settings[key] = value
        self.settings = json_dump(prev_settings) if prev_settings is not None else json_dump(self.settings)
        with open(settings_filename, 'w') as settings:
            settings.write(self.settings)


def getItems(get: bool = False):
    if not os.path.isfile(settings_filename):
        _settings.write_preflight_settings()
        print(f'Settings:\n{_settings.get_preflight_settings()}')
    else:
        with open(settings_filename, 'r', encoding='utf8') as settings:
            content = json.dumps(json.loads(settings.read()), indent=2, sort_keys=True)
            if get:
                return content
            else:
                print(f'Settings:\n{content}')


def resetSettings():
    try:
        os.remove(settings_filename)
    except OSError:
        pass
    

def help_dialog():
    print(
        '''
pjsettings [option]

Options         Value
get             Get current settings
rm              Reset settings to defaults

pjsettings [arguments]

Arguments       Value
--app           Google Chrome, Firefox, Safari, etc
--name          Username for prettyjson
--os            OSX or Windows
--keepclose     Do not open files by default (default: False)

Example: pjsettings --app Google Chrome --os OSX --name prettyjsoncreator
         pjsettings get

Note: Any setting will be saved. The options above are used by PrettyJson.
        '''
    )


def cli():
    args = sys.argv[1:]
    prettyJsonSettings = None
    
    if args.count('--help') != 0:
        help_dialog()
        sys.exit()
    elif args[0].lower() == 'get':
        getItems()
        sys.exit()
    elif args[0].lower() == 'rm':
        resetSettings()
        sys.exit()
    elif len(args) == 1:
        sys.exit()

    try:
        prettyJsonSettings = Settings(args)
        prettyJsonSettings.setItems()
    except AttributeError as ae:
        print(ae, 'type --help for details')
    except IndexError:
        print('at least one argument is required. type --help for details')
    except (FileNotFoundError, ValueError):
        print(f'{args[0]} not found')


if __name__ == '__main__':
    cli()