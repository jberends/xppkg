from lxml import etree
import yaml

__author__ = 'jochem'


_airlinecode_file = 'Airline_codes-All.html'
_airlinecode_wiki_url = 'http://en.wikipedia.org/wiki/Airline_codes-All'

_airline_table_xpath = '/html/body/div[3]/div[3]/div[4]/center/table'
_airline_table_header_xpath = '/html/body/div[3]/div[3]/div[4]/center/table/tr[1]'

_airline_code_dict_filename = 'airlinecodes-dicts.yaml'
_airline_icao_list_filename = 'airlinecodes-icaolist.yaml'
_airline_icao_desc_list_filename = 'airlinecodes-icao-desc-list.yaml'


def retrieve_html(url, filename_to_store):
    pass


def parse_from_html_as_dict(html_file, table_xpath, header_xpath):
    """
    parses the html file to look for airline codes, looking for xpath
    """
    with open(html_file,'r') as fd:
        parser = etree.XMLParser(recover=True)
        html_etree = etree.parse(fd, parser)
    table_elements = html_etree.xpath(table_xpath)[0]
    header_elements = html_etree.xpath(header_xpath)[0]

    #now to dict
    key_list = [unicode(el.text).strip() for el in header_elements]
    dicts = []
    for row in table_elements:
        dict = {}
        if row.tag == 'tr':
            for key, column in zip(key_list, row):
                if row.text.strip() is not None or unicode(row.text).strip is not key:
                    dict.update( { key: unicode(column.text).strip() } )
        if dict:
            dicts.append(dict)
    return dicts

if __name__ == '__main__':
    dicts = parse_from_html_as_dict(_airlinecode_file, _airline_table_xpath, _airline_table_header_xpath)

    # dict list
    yaml.dump(dicts, open(_airline_code_dict_filename, 'w'))

    # icao list
    yaml.dump([str(d[u'ICAO']) for d in dicts], open(_airline_code_dict_filename, 'w'))
