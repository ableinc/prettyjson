import subprocess, io, shlex, sys, os.path, os


class OpenPrettyJson:
    def __init__(self, args):
        self.args = args
        self.filepath = args[0]
        try:
            self.verbose = args[1]
        except IndexError:
            self.verbose = True
        self._data_check()
    
    def _data_check(self):
        if not os.path.isfile(self.filepath):
            print(f'{self.filepath} is not a file in {os.curdir}.')
            raise FileNotFoundError

    def open(self):
        cmd = f'open -a "Google Chrome.app" {self.filepath}'
        args = shlex.split(cmd)
        if self.verbose:
            print('Opening PrettyJson...')
        proc = subprocess.Popen(args, encoding='utf8', stdout=subprocess.PIPE)
        for line in io.TextIOWrapper(proc.stdout):
            print(line)


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