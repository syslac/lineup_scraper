import cssselect
import lxml
import json
from io import StringIO, BytesIO
import os
import re

def null_output(arg1, arg2, arg3):
    return

def standard_wget(url, filename):
    import wget
    try:
        return wget.download(url, None, null_output)
    except Exception as e:
        return null_output

def fake_user_agent(url, filename):
    hUA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0'
    command = 'wget -U \''+hUA+'\' '+url+' >/dev/null 2>&1'
    os.system(command)
    return filename

def no_cert(url, filename):
    command = 'wget --no-check-certificate '+url+' >/dev/null 2>&1'
    os.system(command)
    return filename

def extract_text(el, param):
    return el.text

def extract_attr(el, param):
    return el.get(param)

def preprocess_id(data):
    return [data]

def preprocess_tolmin(data):
    return [re.sub("^tolminator2024_", "", data, 0, re.IGNORECASE)]

def preprocess_leyendas(data):
    return [re.sub("\s+leyendas del rock 2023$", "", data, 0, re.IGNORECASE)]

def preprocess_rockstadt(data):
    return [re.sub("\(.*?\)", "", data)]

def preprocess_metaldays(data):
    data = re.sub("^\(\'", "", data)
    data = re.sub("\'\)$", "", data)
    try:
        full_json = json.loads(data)
        artists_list = full_json['appsWarmupData']['14271d6f-ba62-d045-549b-ab972ae1f70e']['comp-kwthmmhs_galleryData']['items']
        return_list = []
        for k in artists_list:
            return_list.append(k['metaData']['title'])
        return return_list

    except json.JSONDecodeError as e:
        print(e.msg)
    except Exception as f:
        print(f)


downloaders = {
    'standard' : standard_wget,
    'fake' : fake_user_agent,
    'no_cert' : no_cert
}

extractors = {
    'text' : extract_text,
    'attr' : extract_attr,
}

preprocessors = {
    'id' : preprocess_id,
    'tolmin' : preprocess_tolmin,
    'leyendas' : preprocess_leyendas,
    'metaldays' : preprocess_metaldays,
    'rockstadt' : preprocess_rockstadt,
}

festivals = [
    {
        'title': 'Rock Castle Open Air',
        'url': 'https://www.rockcastle.cz/cs/kapely', 
        'filename' : '',
        'downloader' : 'standard',
        'selector' : 'div.band-logo img',
        'extractor' : 'attr',
        'attr' : 'title',
        'preprocess' : 'id'
    },
    {
        'title': 'Masters of Rock',
        'url': 'https://www.mastersofrock.cz/cs/kapely/', 
        'filename' : '',
        'downloader' : 'standard',
        'selector' : 'div.band-item img',
        'extractor' : 'attr',
        'attr' : 'title',
        'preprocess' : 'id'
    },
    {
        'title': 'Metalfest Open Air',
        'url' : 'https://www.metalfest.cz/cs/kapely',
        'filename' : '',
        'downloader' : 'standard',
        'selector' : 'div.band-item img',
        'extractor' : 'attr',
        'attr' : 'title',
        'preprocess' : 'id'
    },
    {
        'title': 'Summerbreeze',
        'url' : 'https://www.summer-breeze.de/de/bands',
        'filename' : '',
        'downloader' : 'standard',
        'selector' : 'h3.teaser__title',
        'extractor' : 'text',
        'attr' : '',
        'preprocess' : 'id'
    },
    {
        'title': 'Sabaton Open Air',
        'url' : '', #'https://sabatonopenair.net/running-order-2022/',
        'filename' : '',
        'downloader' : 'standard',
        'selector' : 'a.pp-post-link',
        'extractor' : 'attr',
        'attr' : 'title',
        'preprocess' : 'id'
    },
    {
        'title': 'Hellfest',
        'url' : 'https://en.concerts-metal.com/concert_-_Hellfest_2024-144699.html', 
        'filename' : '',
        'downloader' : 'standard',
        'selector' : 'table font a',
        'extractor' : 'text',
        'attr' : '',
        'preprocess' : 'id'
    },
    {
        'title': 'Tons of Rock',
        'url' : 'https://goeventweb-static.greencopper.com/2617ccea62e34209b95dc7bf8a0294f3/tonsofrockwebwidget-2024/data/eng/events.json',
        'filename' : 'events.json',
        'downloader' : 'fake',
        'selector' : 'json',
        'extractor' : 'attr',
        'attr' : 'title',
        'preprocess' : 'id'
    },
    {
        'title': 'Metaldays',
        'url' : 'https://www.metaldays.net/2023',
        'filename' : '',
        'downloader' : 'standard',
        'selector' : 'script#wix-warmup-data',
        'extractor' : 'text',
        'attr' : '',
        'preprocess' : 'metaldays'
    },
    {
        'title': 'Barcelona Rock Fest',
        'url' : 'https://en.concerts-metal.com/concert_-_Rock_Fest_Barcelona_2024-158288.html', #'https://www.barcelonarockfest.com/bandas',
        'filename' : '',
        'downloader' : 'standard',
        'selector' : 'table font a',
        'extractor' : 'text',
        'attr' : '',
        'preprocess' : 'id'
    },
    {
        'title': 'Graspop',
        'url': 'https://www.graspop.be/en/line-up/a-z', 
        'filename' : '',
        'downloader' : 'standard',
        'selector' : 'h4.artist__name',
        'extractor' : 'text',
        'attr' : '',
        'preprocess' : 'id'
    },
    {
        'title': 'Novarock',
        'url': 'https://www.novarock.at/lineup/',
        'filename' : '',
        'downloader' : 'standard',
        'selector' : 'h3.item__title',
        'extractor' : 'text',
        'attr' : '',
        'preprocess' : 'id'
    },
    {
        'title': 'Tuska',
        'url': 'https://www.tuska.fi/en/lineup',
        'filename' : '',
        'downloader' : 'standard',
        'selector' : 'li.views-row img',
        'extractor' : 'attr',
        'attr' : 'alt',
        'preprocess' : 'id'
    },
    {
        'title': 'Brutal Assault',
        'url' : 'https://brutalassault.cz/cs/line-up',
        'filename' : 'line-up',
        'downloader' : 'fake',
        'selector' : 'strong.band_lineup_title',
        'extractor' : 'text',
        'attr' : '',
        'preprocess' : 'id'
    },
    {
        'title': 'Sweden Rock',
        'url': 'https://www.swedenrock.com/en/festival/artists/artists2024',
        'filename' : '',
        'downloader' : 'standard',
        'selector' : 'div#band_container>div>div>div>span>span',
        'extractor' : 'text',
        'attr' : '',
        'preprocess' : 'id'
    },
    {
        'title': 'Leyendas del Rock',
        'url': 'https://www.dodmagazine.es/festivales/leyendas-del-rock/', #temporary, official should be 'leyendasdelrock.es',
        'filename' : '',
        'downloader' : 'standard',
        'selector' : 'span#span-612-162860-1 li',
        'extractor' : 'text',
        'attr' : '',
        'preprocess' : 'id'
    },
    {
        'title': 'Basin Fire Fest',
        'url': 'https://basin.cz/cs/line-up', 
        'filename' : 'line-up',
        'downloader' : 'fake',
        'selector' : 'strong.band_lineup_title',
        'extractor' : 'text',
        'attr' : '',
        'preprocess' : 'id'
    },
    {
        'title': 'Baltic Open Air',
        'url': 'https://www.baltic-open-air.de/en/line-up/', 
        'filename' : '',
        'downloader' : 'standard',
        'selector' : 'h4.heading',
        'extractor' : 'text',
        'attr' : '',
        'preprocess' : 'id'
    },
    {
        'title': 'Alcatraz Open Air',
        'url': 'https://en.concerts-metal.com/concert_-_Alcatraz_Metal_Festival_2024-148619.html', #temporary, official should be 'https://www.alcatraz.be/en/line-up', but has logos only in an image
        'filename' : '',
        'downloader' : 'standard',
        'selector' : 'table font a',
        'extractor' : 'text',
        'attr' : '',
        'preprocess' : 'id'
    },
    {
        'title': 'RockHarz',
        'url': 'https://www.rockharz-festival.com/bands',
        'filename' : '',
        'downloader' : 'standard',
        'selector' : 'div.band_item a',
        'extractor' : 'attr',
        'attr' : 'title',
        'preprocess' : 'id'
    },
    {
        'title': 'Copenhell',
        'url': 'https://goeventweb-static.greencopper.com/a2f876e83709491a8349f246f8216187/copenhellwebwidget-2023/data/dan/events.json',
        'filename' : 'events.json',
        'downloader' : 'fake',
        'selector' : 'json',
        'extractor' : 'attr',
        'attr' : 'title',
        'preprocess' : 'id'
    },
    {
        'title': 'Resurrection Fest',
        'url': 'https://en.concerts-metal.com/concert_-_Resurrection_Fest_2024-144831.html', #'https://www.resurrectionfest.es/',
        'filename' : '',
        'downloader' : 'standard',
        'selector' : 'table font a',
        'extractor' : 'text',
        'attr' : '',
        'preprocess' : 'id'
    },
    {
        'title': 'Rockstadt Open Air',
        'url': 'https://rockstadtextremefest.ro/', 
        'filename' : '',
        'downloader' : 'standard',
        'selector' : 'section[data-id="5a1407c"] h5.entry-title a',
        'extractor' : 'text',
        'attr' : '',
        'preprocess' : 'rockstadt'
    },
    {
        'title': 'Tolminator',
        'url': 'https://tolminator.com/lineup/',
        'filename' : '',
        'downloader' : 'standard',
        'selector' : 'h3.elementor-heading-title',
        'extractor' : 'text',
        'attr' : '',
        'preprocess' : 'id'
    },
    {
        'title': 'Wolfszeit',
        'url': 'https://www.wolfszeit-festival.de/bands',
        'filename' : '',
        'downloader' : 'standard',
        'selector' : 'div.info-element-title span',
        'extractor' : 'text',
        'attr' : '',
        'preprocess' : 'id'
    },
    {
        'title': 'Dong Open Air',
        'url': 'https://www.dongopenair.de/en/bands/index',
        'filename' : 'index',
        'downloader' : 'no_cert',
        'selector' : 'div.bandteaser a',
        'extractor' : 'text',
        'attr' : '',
        'preprocess' : 'id'
    },
]

def get_line_up(url, filename, downloader, selector, extractor, attr, preprocessor):
    local_fname = downloader(url, filename)
    #return

    from lxml import etree
    parser = etree.HTMLParser()
    try:
        tree = etree.parse(local_fname, parser)

        if selector == 'json':
            f = open(local_fname) or die('Invalid json file')
            try:
                artists_list = json.load(f)
                return_list = []
                for k in artists_list:
                    return_list.append(artists_list[k][attr])
            except json.JSONDecodeError as e:
                print(e.msg)
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
                return_list.extend(preprocessor(extractor(e, attr)))

        os.remove(local_fname)
        return return_list

    except Exception as e:
        return [];

def normalize_lowercase(name):
    try:
        name = name.lower()
        import re
        name = re.sub("^\s+", "", name)
        name = re.sub("\s+$", "", name)
        name = re.sub("\s+", "_", name)
        name = re.sub("-+", "_", name)
        name = re.sub("_+", "_", name)

        name = re.sub("_", " ", name)
        return name
    except Exception as e:
        return ""

def print_bands_list(bands_set):
    print(sorted(bands_set))

def print_bands_with_festivals(matrix):
    sorted_bands = [k for k in matrix.keys()]
    sorted_bands.sort()
    for b in sorted_bands:
        print(b + " : " + ','.join([ festivals[i]['title'] for i in matrix[b]]))

def print_csv(matrix):
    out_file = open('presences.csv', 'w', encoding='utf-8') or die('unable to open output file')
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
        f['attr'],
        preprocessors[f['preprocess']])
    new_set = set([normalize_lowercase(b) for b in raw_list])
    for b in new_set:
        if b in presence_matrix:
            presence_matrix[b].append(i)
        else:
            presence_matrix[b] = [i]
    bands_list = bands_list.union(new_set)
    i = i + 1

print_csv(presence_matrix)

