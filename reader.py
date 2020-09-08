import feedparser
import urllib.request
from markdownify import markdownify
from rich.console import Console
from rich.markdown import Markdown
console = Console()

# Configuration
sub_arXivs = [
'astro-ph.SR',
'astro-ph.EP',
'astro-ph.IM',
'cond-mat.dis-nn',
'cond-mat.str-el',
'cond-mat.stat-mech'
]

out_dir = '/Users/ajermyn/Dropbox/Notes/arXiv/'
pdf_dir = out_dir + 'pdf/'
record_file = out_dir + 'processed'
interest_file = out_dir + 'interested.md'

# Parsing logic
keys = ['id', 'title', 'link', 'summary', 'authors']
def extract_name_from_link(link):
	print(link)
	print(link.split('>'))
	link = link.split('>')[1]
	link = link.split('<')[0]
	return link

def parse_entry(entry):
	title = entry['title']
	title = title.split('arXiv')[0][:-1]

	link = entry['link']
	abstract = markdownify(entry['summary'])
	authors = entry['authors'][0]['name'].split(',')
	authors = [extract_name_from_link(author) for author in authors if 'arxiv.org' in author]

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
	feed = feedparser.parse('http://arxiv.org/rss/' + sub_arXiv)

	for entry in feed.entries:
		formatted_entry, authors, link = parse_entry(entry)
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
				urllib.request.urlretrieve(pdf_link, pdf_dir + fname + '.pdf')
				print(pdf_dir + fname + '.pdf')

			record_fi.write(link + '\n')
			record_fi.flush()
			interest_fi.flush()

record_file.close()
interest_fi.close()