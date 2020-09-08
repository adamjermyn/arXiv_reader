import feedparser
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

out_dir = '~/Dropbox/Notes/arXiv/'
pdf_dir = out_dir + 'pdf/'



feeds = [feedparser.parse('http://arxiv.org/rss/' + sub_arXiv) for sub_arXiv in sub_arXivs]

keys = ['id', 'title', 'link', 'summary', 'authors']
def extract_name_from_link(link):
	link = link.split('>')[1]
	link = link.split('<')[0]
	return link

def format_entry(entry):
	title = entry['title']
	title = title.split('arXiv')[0][:-1]

	link = entry['link']
	abstract = markdownify(entry['summary'])
	authors = entry['authors'][0]['name'].split(',')
	authors = [extract_name_from_link(author) for author in authors]

	s = ['# ' + title, '- ' + abstract, '- ' + ', '.join(authors), '', '- ' + link]
	s = '\n'.join(s)

	return s, link

for sub_arXiv in sub_arXivs:
	feed = feedparser.parse('http://arxiv.org/rss/' + sub_arXiv)

	for entry in feed.entries[:1]:
		formatted_entry, link = format_entry(entry)

		console.print(Markdown(formatted_entry))
