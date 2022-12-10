import cssselect
import lxml
import json
from io import StringIO, BytesIO
import os

def null_output(arg1, arg2, arg3):
    return

def standard_wget(url, filename):
    import wget
    return wget.download(url, None, null_output)

def fake_user_agent(url, filename):
    hUA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0'
    command = 'wget -U \''+hUA+'\' '+url+' >/dev/null 2>&1'
    os.system(command)
    return filename

def extract_text(el, param):
    return el.text

def extract_attr(el, param):
    return el.get(param)

downloaders = {
    'standard' : standard_wget,
    'fake' : fake_user_agent
}

extractors = {
    'text' : extract_text,
    'attr' : extract_attr,
}

festivals = [
    {
        'title': 'Rock Castle Open Air',
        'url': ''
    },
    {
        'title': 'Masters of Food',
        'url': 'https://www.mastersofrock.cz/cs/kapely/',
        'filename' : '',
        'downloader' : 'standard',
        'selector' : 'div.band-item img',
        'extractor' : 'attr',
        'attr' : 'title',
    },
    {
        'title': 'Metalfest Open Air',
        'url' : 'https://www.metalfest.cz/cs/kapely',
        'filename' : '',
        'downloader' : 'standard',
        'selector' : 'div.band-item img',
        'extractor' : 'attr',
        'attr' : 'title',
    },
    {
        'title': 'Summerbreeze',
        'url' : 'https://www.summer-breeze.de/de/bands',
        'filename' : '',
        'downloader' : 'standard',
        'selector' : 'h3.teaser__title',
        'extractor' : 'text',
        'attr' : '',
    },
    {
        'title': 'Sabaton Open Air',
        'url': ''
    },
    {
        'title': 'Hellfest',
        'url': ''
    },
    {
        'title': 'Tons of Rock',
        'url' : 'https://goeventweb-static.greencopper.com/7c0cd8a0b51a4c268a553ef8153aff6e/tonsofrock-2022/data/nor/artists.json',
        'filename' : 'artists.json',
        'downloader' : 'fake',
        'selector' : 'json',
        'extractor' : 'attr',
        'attr' : 'title',
    },
    {
        'title': 'Metaldays',
        'url' : 'https://www.metaldays.net/2022',
        'filename' : '',
        'downloader' : 'standard',
        'selector' : 'img.gallery-item-visible',
        'extractor' : 'attr',
        'attr' : 'alt',
    },
    {
        'title': 'Barcelona Rock Fest',
        'url': ''
    },
    {
        'title': 'Graspop',
        'url': 'https://www.graspop.be/en/line-up/a-z',
        'filename' : '',
        'downloader' : 'standard',
        'selector' : 'h4.artist__name',
        'extractor' : 'text',
        'attr' : '',
    },
    {
        'title': 'Novarock',
        'url': 'https://www.novarock.at/lineup/',
        'filename' : '',
        'downloader' : 'standard',
        'selector' : 'h3.item__title',
        'extractor' : 'text',
        'attr' : '',
    },
    {
        'title': 'Tuska',
        'url': 'https://www.tuska.fi/en/lineup',
        'filename' : '',
        'downloader' : 'standard',
        'selector' : 'li.views-row img',
        'extractor' : 'attr',
        'attr' : 'alt',
    },
    {
        'title': 'Brutal Assault',
        'url' : 'https://brutalassault.cz/cs/line-up',
        'filename' : 'line-up',
        'downloader' : 'fake',
        'selector' : 'strong.band_lineup_title',
        'extractor' : 'text',
        'attr' : '',
    },
    {
        'title': 'Sweden Rock',
        'url': 'https://www.swedenrock.com/en/festival/artists/sweden-rock-2023',
        'filename' : '',
        'downloader' : 'standard',
        'selector' : 'div#band_container>div>div>div>span>span',
        'extractor' : 'text',
        'attr' : '',
    },
    {
        'title': 'Leyendas del Rock',
        'url': '',
        'filename' : '',
        'downloader' : '',
        'selector' : 'figure>img',
        'extractor' : 'attr',
        'attr' : 'alt',
    },
    {
        'title': 'Basin Fire Fest',
        'url': 'https://basin.cz/cs/line-up',
        'filename' : 'line-up',
        'downloader' : 'fake',
        'selector' : 'strong.band_lineup_title',
        'extractor' : 'text',
        'attr' : '',
    },
    {
        'title': 'Baltic Open Air',
        'url': 'https://www.baltic-open-air.de/en/line-up',
        'filename' : '',
        'downloader' : 'standard',
        'selector' : 'h4.heading',
        'extractor' : 'text',
        'attr' : '',
    },
    {
        'title': 'Alcatraz Open Air',
        'url': 'https://www.alcatraz.be/en/line-up/',
        'filename' : '',
        'downloader' : 'standard',
        'selector' : 'h4.card-title',
        'extractor' : 'text',
        'attr' : '',
    },
]

def get_line_up(url, filename, downloader, selector, extractor, attr):
    local_fname = downloader(url, filename)

    from lxml import etree
    parser = etree.HTMLParser()
    tree = etree.parse(local_fname, parser)

    if selector == 'json':
        f = open(local_fname) or die('Invalid json file')
        artists_list = json.load(f)
        return_list = []
        for k in artists_list:
            return_list.append(artists_list[k][attr])
        f.close()
    else:
        try:
            expression = cssselect.HTMLTranslator().css_to_xpath(selector)
        except cssselect.SelectorError:
            print('Invalid selector')
            os.remove(local_fname)
            exit()

        res = tree.xpath(expression)
        return_list = []
        for e in res:
            return_list.append(extractor(e, attr))

    os.remove(local_fname)
    return return_list

def normalize_lowercase(name):
    name = name.lower()
    import re
    name = re.sub("^\s+", "", name)
    name = re.sub("\s+$", "", name)
    name = re.sub("\s+", "_", name)
    name = re.sub("-+", "_", name)
    name = re.sub("_+", "_", name)
    name = re.sub("\s+Leyendas del Rock 2023$", "", name)

    name = re.sub("_", " ", name)
    return name

def print_bands_list(bands_set):
    print(sorted(bands_set))

def print_bands_with_festivals(matrix):
    sorted_bands = [k for k in matrix.keys()]
    sorted_bands.sort()
    for b in sorted_bands:
        print(b + " : " + ','.join([ festivals[i]['title'] for i in matrix[b]]))

def print_csv(matrix):
    out_file = open('2023.csv', 'w', encoding='utf-8') or die('unable to open output file')
    csv_header = ";"
    for f in festivals:
        csv_header = csv_header + f['title'] + ";"
    out_file.write(csv_header+'\n')
    sorted_bands = [k for k in matrix.keys()]
    sorted_bands.sort()
    for b in sorted_bands:
        csv_line = b + ";"
        for i in range(len(festivals)):
            if i in matrix[b]:
                csv_line = csv_line + "1" + ";"
            else:
                csv_line = csv_line + "0" + ";"
        out_file.write(csv_line+'\n')
    out_file.close()


bands_list = set([])
presence_matrix = dict()

i = 0
for f in festivals:
    print('Processing '+f['title'])
    if f['url'] == '':
        i = i + 1
        continue
    raw_list = get_line_up(
        f['url'],
        f['filename'],
        downloaders[f['downloader']],
        f['selector'],
        extractors[f['extractor']],
        f['attr'])
    new_set = set([normalize_lowercase(b) for b in raw_list])
    for b in new_set:
        if b in presence_matrix:
            presence_matrix[b].append(i)
        else:
            presence_matrix[b] = [i]
    bands_list = bands_list.union(new_set)
    i = i + 1

print_csv(presence_matrix)

