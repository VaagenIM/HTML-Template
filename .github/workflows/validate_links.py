import re
import glob
import pytest
import urllib.parse

from pathlib import Path

ROOT_FOLDER = str(Path(__file__).parents[2]).replace('\\', '/')
FILES = [file.replace('\\', '/') for file in glob.glob(f'{ROOT_FOLDER}/**/*.*', recursive=True)]
CONTENTS = [open(file, 'r').read() for file in FILES if file.lower().endswith('.html')]


def validate_paths(rel_paths: list) -> bool:
    is_valid = True
    for path in rel_paths:
        path = urllib.parse.unquote(path)
        is_url = re.match(r'^(#|\/$|https?:\/\/)', path, flags=re.IGNORECASE)
        is_file = any(path.split('/')[-1] in file.split('/') for file in FILES)
        if not is_url and not is_file:
            print(f'ERROR: File not found: {path}')
            is_valid = False
    return is_valid


def regex(attr: str) -> str:
    """Returns <*{attr}="(*CAPTURE*)"*>"""
    return r'\<[^\>]*' + attr + r'="([^\"]*)"[^\>]*>'


@pytest.mark.skipif(CONTENTS == [], reason='Missing content')
def test_validate_links():
    rel_paths = [re.findall(regex('href'), content, flags=re.IGNORECASE) for content in CONTENTS][0]
    rel_paths += [re.findall(regex('src'), content, flags=re.IGNORECASE) for content in CONTENTS][0]
    assert validate_paths(rel_paths)
