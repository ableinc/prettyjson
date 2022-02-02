# PrettyJson

PrettyJson is a CLI tool for displaying JSON files in a pretty-printed format, written in and for Python 3.


# How to Use
1. Install
```bash
python3 setup.py install
```
2. Help dialog

```bash
pj --help
```

```bash
pjdisplay --help
```

```bash
pjsettings --help
```

# Details
1. PrettyJson 
    All pretty-printed JSON will be opened in Google Chrome by default (this can be changed). If multiple files are given prettyjson then you will be prompted to answer if you'd like to open all files or just save them to memory. 

    This is a data visualizer tool.
    CLI command: prettyjson --help

2. PrettyJson Display
    For already existing pretty-printed JSONs you can run this tool to open the file(s) in your recommended format (via Settings).

    CLI command: pjopen --help

3. PrettyJson Settings
    These are the settings that both PrettyJson and PrettyJson Display will use to prettify your data. These settings are saved to 
    OSX - /Users/[username]/.prettyjson
    Windows: C:\Users\Program Files\.prettyjson

    CLI command: pjsettings --help

 

