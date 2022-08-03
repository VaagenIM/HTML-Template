import re
import glob

from pathlib import Path


ROOT_FOLDER = str(Path(__file__).parents[2]).replace('\\', '/')
FILES = [file.replace('\\', '/') for file in glob.glob(f'{ROOT_FOLDER}/**/*.*', recursive=True)]
CONTENTS = [open(file, 'r').read() for file in FILES if file.lower().endswith('.html')]


def verify_attr_value(value: str) -> bool:
    if re.match(r'^https?://', value, flags=re.IGNORECASE):
        return True
    elif f'{ROOT_FOLDER}/{value}' not in FILES:
        raise FileNotFoundError(f'Invalid link: {value}')
    return True


def regex(attr: str) -> str:
    """Returns <*{attr}="(*CAPTURE*)"*>"""
    return r'\<[^\>]*' + attr + r'="([^\"]*)"[^\>]*>'


def test_href(pytestconfig):
    for content in CONTENTS:
        paths = re.findall(regex('href'), content, flags=re.IGNORECASE)
        [verify_attr_value(path) for path in paths]


def test_src():
    for content in CONTENTS:
        paths = re.findall(regex('src'), content, flags=re.IGNORECASE)
        [verify_attr_value(path) for path in paths]
