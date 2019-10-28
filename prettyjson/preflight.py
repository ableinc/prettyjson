import sys, getpass, json


class Preflight:
    def _determine_os(self):
        return sys.platform
    
    def _determine_os_ext(self):
        option = {
            'win32': '.exe',
            'darwin': '.app' 
        }.get(sys.platform)
        return option
    
    def _get_machine_name(self):
        return getpass.getuser()
    
    def get_preflight_settings(self):
        return {
            'OS': self._determine_os(),
            'OS_EXT': self._determine_os_ext(),
            'NAME': self._get_machine_name()
        }
    
    def write_preflight_settings(self):
        with open('./settings.json', 'w', encoding='utf8') as settings:
            settings.write(json.dumps(self.get_preflight_settings(), indent=2, sort_keys=True))