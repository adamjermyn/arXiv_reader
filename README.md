# arXiv_reader
An interactive python package for reading the daily arXiv posting, either via RSS, email, or the arXiv API.

## Configuration
The configuration is stored in `reader.py` in the following lines:
```
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
```
The `sub_arXivs` list stores the arXiv categories you want arXiv_reader to check. `pdf_dir` is the directory arXiv_reader will use to store papers you tell it to download. `record_file` is the path to a file where arXiv_reader stores a list of all papers it has shown you, to avoid showing the same paper twice. `interest_file` stores a summary (title, abstract, authors, link) of each paper you've indicated interest in. This is stored with markdown formatting.

A similar configuration is available in `email_reader.py`:
```
# Configuration
email_dir = '/Users/ajermyn/Dropbox/Notes/arXiv/emails/'

out_dir = '/Users/ajermyn/Dropbox/Notes/arXiv/'
pdf_dir = out_dir + 'pdf/'
record_file = out_dir + 'processed'
interest_file = out_dir + 'interested.md'
```
Here `email_dir` is the directory storing the `mbox`-formatted emails from the arXiv.

## Usage
Call arXiv_reader using
```
python reader.py
```
The reader will then run and print the arXiv listing for a paper you haven't yet seen in the arXiv RSS feed for your specified categories. It then asks you to either (1) discard the entry, (2) save the entry to the `interest_file`, or (3) save the entry to the `interest_file` **and** save the pdf to the `pdf_dir`. 

The email reader is called much the same way:
```
python email_reader.py
```

The API reader is called as
```
python api_reader.py [days to look back]
```
If no option is specified the API reader will only consider new postings from within the last two days.
Otherwise an integer should be specified which gives the number of days to look back.

Note that all three readers use the same format for storing processed and of-interest papers, so you can use them interchangeably and be assured that you won't see the same paper twice.
