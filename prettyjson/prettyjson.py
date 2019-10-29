import sys, subprocess, json, os, shlex, io, re, random
from datetime import datetime
try:
    from preflight import Preflight
    from defaults import settings_dir, settings_filename
except ImportError:
    from prettyjson.preflight import Preflight
    from prettyjson.defaults import settings_filename, settings_dir


class PrettyJson:
    def __init__(self, args):
        self.data = []
        self.pretty_data = []
        self.new_filepaths = []
        self._set_defaults(args)
        self.settings = self._get_settings()
        self.open_file()
    
    def _set_defaults(self, args):
        try:
            self.filepath = args[0]
            self.indent = int(args[1])
            self.verbose = False if args[2] == 'False' else True
        except IndexError:
            self.filepath = args[0]
            self.indent = 4
            self.verbose = True
        finally:
            if ',' in self.filepath:
                self.filepath = re.sub('\s', '', args[0]).split(',')
            else:
                self.filepath = [self.filepath]
    
    def _get_settings(self):
        try:
            from settings import getItems
        except ImportError:
            from prettyjson.settings import getItems

        return json.loads(getItems(True))

    def open_file(self):
        for fp in self.filepath:
            if not os.path.isfile(fp):
                raise FileNotFoundError(f'{self.filepath} is not a file.')
            with open(fp, encoding='utf8', mode='r') as obj:
                self.data.append(obj.read())

    def structure_data(self):
        for data in self.data:
            obj = json.dumps(json.loads(data, encoding='utf8'), indent=self.indent, sort_keys=True)
            self.pretty_data.append(obj)
    
    def write_pretty_json(self):
        for index, pdata in enumerate(self.pretty_data):
            str_val = f'_{index}'
            value = str_val if index > 0 else ''
            filename = f'{datetime.now().date()}_prettyjson{value}.json'
            if os.path.isfile(filename):
                filename = f'{datetime.now().date()}_prettyjson{value}_{random.randint(0, 100)}.json'
            new_file_path = self.filepath[index].replace(os.path.basename(self.filepath[index]), filename)
            self.new_filepaths.append(new_file_path)
            with open(new_file_path, mode='w', encoding='utf8') as prettyjson:
                prettyjson.write(pdata)
            if self.verbose:
                print(f'PrettyJson saved as {new_file_path}')

    def open_pretty_json(self):
        try:
            if bool(self.settings['KEEPCLOSE']):
                return
            for newfp in self.new_filepaths:
                if self.settings['OS'] == 'darwin':
                    cmd = f'open -a "{self.settings["APP"]}.{self.settings["OS_EXT"]}" {newfp}'
                else:
                    cmd = f'start "{self.settings["APP"]}.{self.settings["OS_EXT"]}" {newfp}'
                args = shlex.split(cmd)
                if self.verbose:
                    print(f'Opening {newfp}...')
                subprocess.run(args)
        except KeyError as ke:
            print(f'[!] Please update settings [!]\nNo setting found for {ke}.\nType pjsettings --help for more info.')
        finally:
            if bool(self.settings['KEEPCLOSE']):
                if self.verbose:
                    print('Will not open pretty-print file.')


def help_dialog():
    print(
        '''
prettyjson filepath(s) [option] [option]

Options         Value
indent          Integer (default: 4)
verbose         Boolean (default: true)

Example: prettyjson /path/to/file 2 False
         prettyjson filepath.json, filepath2.json, filepath3.json 2 False

Note: Seperate multiple files by comma and space.
        '''
    )


def cli():
    args = sys.argv[1:]
    settings = Preflight()
    settings.write_preflight_settings()
    try:
        if args.count('--help') != 0:
            help_dialog()
            sys.exit()
        elif len(args) == 0:
            raise IndexError
        
        prettyJson = PrettyJson(args)
        prettyJson.structure_data()
        prettyJson.write_pretty_json()
        if ',' in args[0] and len(args[0].split(',')) > 1:
            user = input('open all files? (y/N) ')
            if user.lower() == 'y':
                prettyJson.open_pretty_json()
            else:
                print('Multiple files have been saved.')
        else:
            prettyJson.open_pretty_json()
    except AttributeError as ae:
        print(ae)
    except IndexError:
        print('at least one argument is required. type --help for details')
    except (FileNotFoundError, ValueError) as ee:
        print(f'{args[0]} not found')


if __name__ == '__main__':
    cli()
