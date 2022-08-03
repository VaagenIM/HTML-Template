import re
import glob

from pathlib import Path

ROOT_FOLDER = str(Path(__file__).parents[2]).replace('\\', '/')
FILES = [file.replace('\\', '/') for file in glob.glob(f'{ROOT_FOLDER}/**/*.*', recursive=True)]
CONTENTS = [open(file, 'r').read() for file in FILES if file.lower().endswith('.html')]


def validate_relative_path(rel_path: str) -> bool:
    """Raises FileNotFoundError if the given path is not valid or an URL"""
    is_link = re.match(r'^https?://', rel_path, flags=re.IGNORECASE)
    abspath = f'{ROOT_FOLDER}/{rel_path}'
    if is_link or abspath in FILES:
        return True
    raise FileNotFoundError(f'Could not find the linked resource: {rel_path}')


def regex(attr: str) -> str:
    """Returns <*{attr}="(*CAPTURE*)"*>"""
    return r'\<[^\>]*' + attr + r'="([^\"]*)"[^\>]*>'


def test_href():
    for content in CONTENTS:
        paths = re.findall(regex('href'), content, flags=re.IGNORECASE)
        [validate_relative_path(path) for path in paths]


def test_src():
    for content in CONTENTS:
        paths = re.findall(regex('src'), content, flags=re.IGNORECASE)
        [validate_relative_path(path) for path in paths]
