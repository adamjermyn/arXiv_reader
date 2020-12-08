import urllib.request as libreq
import feedparser
import sys
import time
from markdownify import markdownify
from rich.console import Console
from rich.markdown import Markdown
from datetime import datetime
console = Console()

# Configuration
sub_arXivs = [
'astro-ph.SR',
'astro-ph.EP',
'astro-ph.HR',
'astro-ph.IM',
'cond-mat.dis-nn',
'cond-mat.str-el',
'cond-mat.stat-mech',
'quant-ph'
]

out_dir = '/Users/ajermyn/Dropbox/Notes/arXiv/'
pdf_dir = out_dir + 'pdf/'
record_file = out_dir + 'processed'
interest_file = out_dir + 'interested/' + datetime.now().strftime("%m_%d_%Y") + '.md'
days_to_parse = 2
if len(sys.argv) > 1:
    days_to_parse = int(sys.argv[1])
now_time = time.mktime(time.gmtime())

def query_sub_arXiv(arxiv, page):
    query = 'http://export.arxiv.org/api/query?search_query=cat:' + arxiv + '&sortBy=submittedDate&start=' + str(page) + '&max_results=30'
    query = str(query)
    with libreq.urlopen(query) as url:
        response = url.read()
    feed = feedparser.parse(response)
    return feed

# Parsing logic
keys = ['id', 'title', 'link', 'summary', 'authors']
def extract_name_from_link(link):
    link = link.split('>')[1]
    link = link.split('<')[0]
    return link

def parse_entry(entry):
    title = entry['title'].replace('\n ','')
    link = entry['link']
    abstract = markdownify(entry['summary'])
    authors = list(n['name'] for n in entry['authors'])

    s = ['# ' + title, abstract, '- ' + ', '.join(authors), '- ' + link]
    s = '\n'.join(s)

    return s, authors, link

def format_pdf_name(authors, link):
    arXiv_id = link.split('/')[-1]
    if len(authors) == 1:
        return authors[0] + ' ' + arXiv_id
    elif len(authors) == 2:
        return authors[0] + ' & ' + authors[1] + ' ' + arXiv_id
    else:
        return authors[0]  + '+ ' + arXiv_id

# Get record of all previously-processed entries
records = set()
record_fi = open(record_file, 'r')
for line in record_fi:
    s = line.strip()
    records.add(s)
record_fi.close()

# Parse new entries
interest_fi = open(interest_file, 'a')
record_fi = open(record_file, 'a')

for sub_arXiv in sub_arXivs:
    done = False
    for page in range(100):
        feed = query_sub_arXiv(sub_arXiv, page)
        for entry in feed.entries:
            formatted_entry, authors, link = parse_entry(entry)

            published_time = entry['published_parsed']
            published_time = time.mktime(published_time)

            if now_time - published_time > 24*3600*days_to_parse:
                done = True
                break


            if link not in records:

                console.print(Markdown(formatted_entry))
                console.print('')
                choice = int(console.input('Options: (1) Discard, (2) Save abstract, (3) Save PDF for later reading: '))
                console.print('')

                if choice == 2 or choice == 3:
                    interest_fi.write(formatted_entry + '\n')
                if choice == 3:
                    pdf_link = link.replace('abs','pdf') + '.pdf'
                    fname = format_pdf_name(authors, link)
                    libreq.urlretrieve(pdf_link, pdf_dir + fname + '.pdf')

                records.add(link)
                record_fi.write(link + '\n')
                record_fi.flush()
                interest_fi.flush()
        if done:
            break

record_fi.close()
interest_fi.close()
