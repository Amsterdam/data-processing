import errno
import json
import os
import urllib

import argparse
from requests.packages.urllib3.util import Retry
from requests.adapters import HTTPAdapter
from requests import Session, exceptions
from bs4 import BeautifulSoup


def create_dir_if_not_exists(directory):
    """
    Create directory if it does not yet exists.

    Args:
        Specify the name of directory, for example: `dir/anotherdir`

    Returns:
        Creates the directory if it does not exists, of return the error message.
    """
    try:
        os.makedirs(directory)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise


def getPage(url):
    """
    Get parsed text data from url's.
    Wait for 1 second for slow networks.
    Retry 5 times.
    """
    print('Get: ', url)
    s = Session()
    host_url = '{0.scheme}://{0.netloc}'.format(urllib.parse.urlsplit(url))
    s.mount(host_url, HTTPAdapter(
        max_retries=Retry(total=5, status_forcelist=[500, 503])
    ))
    result = s.get(url, timeout=1)
    assert result.status_code == 200
    data = result.text
    return data


def getRows(url, headers, row):
    """
    Get all rows from tables, add them into a dict and add host url to wiki urls.
    """
    dokuwiki_url = '{0.scheme}://{0.netloc}'.format(urllib.parse.urlsplit(url))
    item = []
    cells = row.find_all(['th', 'td'])
    for cell in cells:
        value = cell.get_text().strip()
        if cell.a:
            url_name = cell.a['href']
            if url_name[:5] == '/doku':
                url_name = dokuwiki_url + url_name
            value = {"naam": value, "url": url_name}
        item.append(value)
    items = dict(zip(headers, item))
    return items


def getHeaders(row):
    headers = []
    if row['class'][0] == 'row0':
        html_headers = row.find_all(['th', 'td'])
        for header in html_headers:
            headers.append(header.get_text().strip())
    # print(headers)
    return headers


def parseHtmlTable(url, html_doc, name='', headertype='h3'):
    """
    Retrieve one html page to parse tables and H3 names from.
    Args:
        - htmldoc: wiki url
        - name: name of the page
        - headertype: h1, h2, or h3 type of the titles used above each table. h3 is not used.
    Result:
        {table_title: h3 text, [{name: value}, ..]}
        if no name is specified:
        [{cluster: title of the page},{name: value}, ...]
    """
    data = []
    soup = BeautifulSoup(html_doc, 'html.parser')
    tables = soup.find_all([headertype, 'table'])
    if name == '':
        cluster_names = [title.text.strip() for title in soup.find_all('h2')]
    tablecount = 0
    for table in tables:
        if table.name == headertype:
            table_title = table.text
        if table.name == 'table':
            new_table = []
            rows = table.find_all('tr')
            for row in rows:
                if row['class'][0] == 'row0':
                    headers = getHeaders(row)
                else:
                    item = getRows(url, headers, row)
                    if name == '':
                        item['Cluster'] = cluster_names[tablecount]
                    else:
                        item['Applicatie'] = name
                    # print(item)
                    new_table.append(item)
            if name:
                data.append({table_title: new_table})
                print('Parsed table: ', table_title)
            else:
                data.append(new_table)
                print('Parsed table')
            tablecount += 1
    return data


def getApplicationURLs(filename, header_name_urls):
    """
    Get all url's of application urls from the cluster page.

    Args:
    - filename: name of the json file where the result is output to.
    - header_name_urls: insert the name of the column header where the wiki urls are listed in.

    Result:
    - list of name of the application and the page url.
    """
    with open(filename, 'r') as infile:
        data = json.load(infile)
        list_of_wikilinks = []
        for cluster in data:
            for i in range(len(cluster)):
                try:
                    if cluster[i][header_name_urls]['url']:
                        list_of_wikilinks.append(cluster[i][header_name_urls])
                except:
                    continue
        print('Found: %d wiki urls'.format(len(list_of_wikilinks)))
        return list_of_wikilinks


def getApplicationHTMLPages(url, application_urls):
    """
    Input: a list of {name: , url: } to iterate over.
    """
    total_applications = []
    for application in application_urls:
        application_html_doc = getPage(application["url"])
        print('Loaded wiki page: ', application["naam"])
        data = parseHtmlTable(url, application_html_doc, application["naam"])
        total_applications.append(
            {"applicatie": application["naam"],
             "gegevens": data}
        )
    return total_applications


def saveFile(data, folder, name):
    """
    Save file as json and return the full path.
    """
    create_dir_if_not_exists(folder)
    filename = "{}{}".format(name, '.json')
    fullpath = os.path.join(folder, filename)
    with open(fullpath, 'w') as outfile:
        json.dump(data, outfile, indent=4)
    print('Saved: ', fullpath)
    return fullpath


def parser():
    """
    Parser function to run arguments from commandline and to add description to sphinx docs.
    To see possible styling options: https://pythonhosted.org/an_example_pypi_project/sphinx.html
    """
    description = """
    Get main wiki page containing all links to related pages to parse this into 2 json files with all the table data.

    The script needs to be able to access dokuwiki.datapunt.amsterdam.nl.

    Example command line:
        ``python download_tables_from_dokuwiki_to_json.py "https://dokuwiki.datapunt.amsterdam.nl/doku.php?id=start:gebruik:systeem" output informatievoorziening clusters applications``
    """

    parser = argparse.ArgumentParser(
                        description=description)
    parser.add_argument('url',
                        type=str,
                        help="""
                        Full url of the main webpage containing the wiki url links to the subpages in quotes,
                        For example:
                        "https://dokuwiki.datapunt.amsterdam.nl/doku.php?id=start:gebruik:systeem"
                        """)
    parser.add_argument('output_folder',
                        type=str,
                        help='Specify the desired output folder path, for example: output')
    parser.add_argument('header_name_urls',
                        type=str,
                        help="""
                        Specify the name of the field where the wiki urls are defined.
                        For example: "informatievoorziening"
                        """)
    parser.add_argument('main_page_name',
                        type=str,
                        help='Specify the desired filename, for example: clusters.json')
    parser.add_argument('sub_pages_name',
                        type=str,
                        help='Specify the desired filename for all retreived tables, for example: applications.json')
    return parser


def main():
    args = parser().parse_args()

    html_doc = getPage(args.url)
    tables_main_page = parseHtmlTable(args.url, html_doc)
    main_page_path = saveFile(tables_main_page, args.output_folder, args.main_page_name)

    list_sub_pages_urls = getApplicationURLs(main_page_path, args.header_name_urls)

    tables_sub_pages = getApplicationHTMLPages(args.url, list_sub_pages_urls)
    saveFile(tables_sub_pages, args.output_folder, args.sub_pages_name)


if __name__ == '__main__':
    main()
