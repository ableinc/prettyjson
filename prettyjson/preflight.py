import sys, getpass, json
import os.path as path
import os
try:
    from defaults import settings_dir, settings_filename
except ImportError:
    from prettyjson.defaults import settings_filename, settings_dir


class Preflight:
    def __init__(self):
        if not path.isdir(settings_dir):
            os.makedirs(settings_dir)
    
    def _determine_os(self):
        return sys.platform
    
    def _determine_os_ext(self):
        option = {
            'win32': 'exe',
            'darwin': 'app' 
        }.get(sys.platform)
        return option
    
    def _get_machine_name(self):
        return getpass.getuser()
    
    def _get_default_app(self):
        return 'Google Chrome'
    
    def get_preflight_settings(self):
        return {
            'OS': self._determine_os(),
            'OS_EXT': self._determine_os_ext(),
            'NAME': self._get_machine_name(),
            'APP': self._get_default_app(),
            'KEEPCLOSE': False
        }
    
    def write_preflight_settings(self):
        if not path.isfile(settings_filename):
            with open(settings_filename, 'w', encoding='utf8') as settings:
                settings.write(json.dumps(self.get_preflight_settings(), indent=2, sort_keys=True))