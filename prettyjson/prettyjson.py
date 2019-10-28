import sys, subprocess, json, os, shlex, io
from datetime import datetime
try:
    from preflight import Preflight
except ImportError:
    from prettyjson.preflight import Preflight


class PrettyJson:
    def __init__(self, filepath, indent=4, verbose=True):
        self.filepath = filepath
        self.indent = indent
        self.verbose = verbose
        self.data = None
        self.pretty_data = None
        self.new_filepath = None
        self.settings = _get_settings()
        self.open_file()
    
    def _get_settings(self):
        from settings import getItems
        return dict(getItems(True))

    def open_file(self):
        if not os.path.isfile(self.filepath):
            raise FileNotFoundError(f'{self.filepath} is not a file.')
        with open(self.filepath, encoding='utf8', mode='r') as obj:
            self.data = obj.read()

    def structure_data(self):
        unsanitized = json.loads(self.data)
        obj = json.dumps(unsanitized, indent=self.indent, sort_keys=True)
        self.pretty_data = obj
    
    def write_pretty_json(self):
        filename = f'{datetime.now().date()}_prettyjson.json'
        new_file_path = self.filepath.replace(os.path.basename(self.filepath), filename)
        self.new_filepath = new_file_path
        with open(new_file_path, mode='w', encoding='utf8') as prettyjson:
            prettyjson.write(self.pretty_data)
        if self.verbose:
            print(f'PrettyJson saved as {self.new_filepath}')

    def open_pretty_json(self):
        try:
            if self.settings['OS'] == 'darwin':
                cmd = f'open -a "{self.settings["APP"]}.{self.settings["OS_EXT"]}" {self.new_filepath}'
            else:
                cmd = f'start "{self.settings["APP"]}.{self.settings["OS_EXT"]}" {self.new_filepath}'
            args = shlex.split(cmd)
            if self.verbose:
                print(f'Opening {self.new_filepath}...')
            subprocess.run(args)
            # proc = subprocess.Popen(args, encoding='utf8', stdout=subprocess.PIPE)
            # for line in io.TextIOWrapper(proc.stdout.readlines()):
            #     print(line)
        except KeyError:
            pass


def help_dialog():
    print(
        '''
prettyjson filepath [option] [option]

Options         Value
indent          Integer (default: 4)
verbose         Boolean (default: true)

Example: prettyjson /path/to/file 2 False
        '''
    )


def check_none_values(args):
    none_values = []
    for index, arg in enumerate(args):
        if index == 0 and arg == None:
            raise AttributeError('Filepath is required. You provided none.')
        if arg is None:
            none_values.append(arg)
    return args, none_values


def cli():
    args = sys.argv[1:]
    prettyJson = None
    if args.count('--help') != 0:
        help_dialog()
        sys.exit()
    settings = Preflight()
    settings.write_preflight_settings()
    try:
        values, none_values = check_none_values(args)
        if len(values) == 3:
            prettyJson = PrettyJson(args[0], args[1], args[2])
        elif len(values) == 2:
            prettyJson = PrettyJson(args[0], args[1])
        else:
            prettyJson = PrettyJson(args[0])
        
        prettyJson.structure_data()
        prettyJson.write_pretty_json()
        prettyJson.open_pretty_json()
    except AttributeError as ae:
        print(ae)
    except IndexError:
        print('at least one argument is required. type --help for details')
    except (FileNotFoundError, ValueError):
        print(f'{args[0]} not found')


if __name__ == '__main__':
    cli()
