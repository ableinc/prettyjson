import subprocess, io, shlex, sys, os.path, os
try:
    from settings import getItems
except ImportError:
    from prettyjson.settings import getItems


class OpenPrettyJson:
    def __init__(self, args):
        self._set_defaults(args)
        self.settings = getItems(True)
        self._data_check()
    
    def _set_defaults(self, args):
        try:
            self.filepath = args[0]
            self.verbose = False if args[1] == 'False' else True
        except IndexError:
            self.filepath = args[0]
            self.verbose = True
        finally:
            if ',' in self.filepath:
                self.filepath = re.sub('\s', '', args[0]).split(',')
            else:
                self.filepath = [self.filepath]
        
    def _data_check(self):
        for fp in self.filepath:
            if not os.path.isfile(fp):
                print(f'{fp} is not a file.')
                raise FileNotFoundError

    def open(self):
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
pjdisplay filepath [option] 

Options         Value
verbose         Boolean (default: true)

Example: pjdisplay /path/to/file False
        '''
    )


def cli():
    args = sys.argv[1:]
    if args.count('--help') != 0:
        help_dialog()
        sys.exit()
    elif len(args) == 0:
        sys.exit()

    try:
        OpenPrettyJson(args).open()
    except IndexError:
        help_dialog()
    except TypeError as te:
        print(te)
    except FileNotFoundError:
        help_dialog()


if __name__ == '__main__':
    cli()