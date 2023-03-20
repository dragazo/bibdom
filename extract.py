import re

header_regex = re.compile(r'^\\bibitem{(\w+)}$')
main_regex = re.compile(r'^([^:]+): (.+), {\\it (.+)}, (.+)\.$')

def fixname(name: str):
    suffix = ''
    for end in [', Jr.']:
        if name.endswith(end):
            suffix = end
            name = name[:-len(end)]
            break
    pos = name.rindex(' ')
    return f'{name[:pos]}{name[pos:pos+2]}{name[pos+2:].lower()}{suffix}'.replace('~', ' ')

with open('main.tex', 'r') as f:
    lines = [x.strip() for x in f.readlines()]

with open('refs.bib', 'w') as f:
    refs = 0
    i = 0
    while i < len(lines):
        m = header_regex.match(lines[i])
        i += 1
        if not m: continue
        id = m[1]
        print(id)

        content = []
        while i < len(lines):
            if lines[i] == '': break
            content.append(lines[i])
            i += 1

        assert 1 <= len(content) <= 2
        if len(content) == 2:
            assert content[0].endswith('\\\\')
            content[0] = content[0][:-2]
            assert content[1].startswith('http')
        for line in content: assert '\\\\' not in line
        assert 'http' not in content[0]

        m = main_regex.match(content[0])
        assert m

        authors = ' and '.join([fixname(x) for x in m[1].replace(', Jr.', '%JR%').replace(',', ' and').replace('%JR%', ', Jr.').split(' and ')])
        title = m[2]
        publisher = m[3]
        extra = m[4]

        assert authors == authors.strip()
        assert title == title.strip()
        assert publisher == publisher.strip()
        assert extra == extra.strip()

        link_str = f',\n    howpublished = {{\\url{{{content[1]}}}}}' if len(content) == 2 else ''

        f.write(f'@article{{{id},\n    title = {{{title}}},\n    author = {{{authors}}},\n    journal = {{{publisher}}},\n    note = {{{extra}}}{link_str}\n}}\n')

        refs += 1

    print('refs', refs)
