from os import listdir
from os.path import isfile, join
import urllib.request
from markdownify import markdownify
from rich.console import Console
from rich.markdown import Markdown
console = Console()

# Configuration
email_dir = '/Users/ajermyn/Dropbox/Notes/arXiv/emails/'

out_dir = '/Users/ajermyn/Dropbox/Notes/arXiv/'
pdf_dir = out_dir + 'pdf/'
record_file = out_dir + 'processed'
interest_file = out_dir + 'interested.md'

# Parsing logic
keys = ['id', 'title', 'link', 'summary', 'authors']
def extract_name_from_link(link):
	link = link.split('>')[1]
	link = link.split('<')[0]
	return link

def parse_entry(entry):
	title = entry['title']

	link = entry['link']
	abstract = markdownify(entry['summary'])
	authors = entry['authors']

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

emails = [join(email_dir, f) for f in listdir(email_dir) if isfile(join(email_dir, f))]


for fname in emails:
	fi = open(fname)
	email = '\n'.join([line for line in fi])
	fi.close()
	entries = email.split('------------------------------------------------------------------------------')[6:-1]

	entries = [e.split('\n') for e in entries]
	entries = [[line for line in e if len(line) > 0 and '%%--%%' not in line and '%-%' not in line] for e in entries]

	data = []
	for e in entries:
		d = {}

		title = ''
		found = False
		for line in e:
			if 'Authors' in line:
				break
			if 'Title' in line:
				found = True
				title = title + line[7:]
			elif found:
				title = title + line
		d['title'] = title.replace('  ', ' ')

		link = e[-1]
		link = link.split(',')[0]
		link = link.lstrip('\\\\')
		link = link.strip()
		link = link.lstrip('(')
		link = link.lstrip()
		d['link'] = link

		authors = []
		found = False
		for line in e:
			if 'Categories' in line:
				break
			if 'Authors' in line:
				found = True
				authors.append(line[8:])
			elif found:
				authors.append(line)
		authors = ' '.join(authors)
		authors = authors.split(',')
		authors = [a.lstrip().strip().replace('  ', ' ').replace('  ', ' ') for a in authors if len(a) > 0]
		d['authors'] = authors

		abstract = ''
		found = 0
		for line in e:
			print(line)
			if 'kb)' in line:
				break
			if '\\\\' in line:
				found += 1
				if found == 2:
					abstract = abstract + line[8:]
			elif found == 2:
				abstract = abstract + ' ' + line
		d['summary'] = abstract.lstrip().strip()
		data.append(d)

	entries = data

	for entry in entries:
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

			records.add(link)
			record_fi.write(link + '\n')
			record_fi.flush()
			interest_fi.flush()

record_fi.close()
interest_fi.close()