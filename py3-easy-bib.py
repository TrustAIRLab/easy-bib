import sys
import os
import pandas as pd

save_suffix = '_generated_py3.bib'

def build_ref_key(bib_item):
    # generate ref key
    author_list = bib_item['author'].split(' and ')
    ref_key = ''
    for a in author_list:
        name_part = a.split(' ')
        ref_key += name_part[-1][0]
    ref_key += str(bib_item['year'])[2:]

    return ref_key

def process_title(df):
    df['title'] = df['title'].str.replace("<dollar-inline>", "$")


def build_bib(mode='normal'):
    venue_fullname = pd.read_csv('venue_fullname.txt', sep='$')

    conference = pd.read_csv('conference.txt', sep='$')
    process_title(conference)


    ref_key_dict = {}
    for i in range(conference.shape[0]):
        print(i)

        ref_key = build_ref_key(conference.loc[i])
        if ref_key in ref_key_dict:
            ref_key_dict[ref_key] += 1
            ref_key += str(ref_key_dict[ref_key])
        else:
            ref_key_dict[ref_key] = 1

        f = open(mode + save_suffix, 'a')

        # type of bib
        f.write("@inproceedings{"+ref_key+',')
        f.write('\n')
        # author
        f.write("author = {"+conference.loc[i, 'author']+"},")
        f.write('\n')
        # title
        f.write("title = {{"+conference.loc[i, 'title']+"}},")
        f.write('\n')
        # venue
        venue = conference.loc[i, 'venue']
        if mode == 'normal':
            if venue == 'WWW_old':
#                proceedings = 'Proceedings of the '+ str(conference.loc[i, 'year']) + ' ' +\
#                            venue_fullname.loc[venue_fullname.venue==venue, 'fullname'].values[0] + ' (WWW)'
                proceedings = venue_fullname.loc[venue_fullname.venue==venue, 'fullname'].values[0] + ' (WWW)'
            elif venue == 'KDD_old':
                proceedings = venue_fullname.loc[venue_fullname.venue==venue, 'fullname'].values[0] + ' (KDD)'
            elif venue == 'ICWSM_old':
                proceedings = venue_fullname.loc[venue_fullname.venue==venue, 'fullname'].values[0] + ' (ICWSM)'
            elif venue == 'NeurIPSCT':
                proceedings = venue_fullname.loc[venue_fullname.venue==venue, 'fullname'].values[0]
            else:
#                proceedings = 'Proceedings of the '+ str(conference.loc[i, 'year']) + ' ' +\
#                            venue_fullname.loc[venue_fullname.venue==venue, 'fullname'].values[0] + ' (' + venue + ')'
                proceedings = venue_fullname.loc[venue_fullname.venue==venue, 'fullname'].values[0] + ' (' + venue + ')'
        elif mode == 'simple':
            if venue == 'WWW_old':
#                proceedings = "Proc.\ "+'WWW'
                proceedings = 'WWW'
            else:
#                proceedings = "Proc.\ "+venue
                proceedings = venue

        f.write("booktitle = {{"+proceedings+"}},")
        f.write('\n')

        if type(conference.loc[i, 'pages'])!=float:
            f.write("pages = {"+conference.loc[i, 'pages']+"},")
            f.write('\n')
        if mode == 'normal':
            # publisher
            if type(conference.loc[i, 'publisher'])!=float:
                f.write("publisher = {"+conference.loc[i, 'publisher']+"},")
                f.write('\n')
        elif mode == 'simple':
            # publisher
            f.write("publisher = {},")
            f.write('\n')
        # year
        f.write("year = {"+str(conference.loc[i, 'year'])+"}")
        f.write('\n')
        f.write("}")
        f.write('\n')
        f.write('\n')
        f.close()

    journal = pd.read_csv('journal.txt', sep='$')
    process_title(journal)
    
    for i in range(journal.shape[0]):
        print(i)

        ref_key = build_ref_key(journal.loc[i])
        if ref_key in ref_key_dict:
            ref_key_dict[ref_key] += 1
            ref_key += str(ref_key_dict[ref_key])
        else:
            ref_key_dict[ref_key] = 1

        f = open(mode+save_suffix, 'a')

        # type of bib
        f.write("@article{"+ref_key+',')
        f.write('\n')
        # author
        f.write("author = {"+journal.loc[i, 'author']+"},")
        f.write('\n')
        # title
        f.write("title = {{"+journal.loc[i, 'title']+"}},")
        f.write('\n')
        venue = journal.loc[i, 'venue']
        # journal
        proceedings = venue_fullname.loc[venue_fullname.venue==venue, 'fullname'].values[0]
        f.write("journal = {{"+proceedings+"}},")
        f.write('\n')
#        # volume
#        if type(journal.loc[i, 'volume'])!=float:
#            f.write("volume = {"+str(journal.loc[i, 'volume'])+"},")
#            f.write('\n')
#        # number
#        if type(journal.loc[i, 'number'])!=float:
#            f.write("number = {"+str(journal.loc[i, 'number'])+"},")
#            f.write('\n')
#        # pages
#        if type(journal.loc[i, 'pages'])!=float:
#            f.write("pages = {"+journal.loc[i, 'pages']+"},")
#            f.write('\n')
        # publisher
        if type(journal.loc[i, 'publisher'])!=float:
            f.write("publisher = {"+journal.loc[i, 'publisher']+"},")
            f.write('\n')
        # year
        f.write("year = {"+str(journal.loc[i, 'year'])+"}")
        f.write('\n')
        f.write("}")
        f.write('\n')
        f.write('\n')
        f.close()

    arxiv = pd.read_csv('arxiv.txt', sep='$')
    process_title(arxiv)
    
    for i in range(arxiv.shape[0]):
        print(i)

        ref_key = build_ref_key(arxiv.loc[i])
        if ref_key in ref_key_dict:
            ref_key_dict[ref_key] += 1
            ref_key += str(ref_key_dict[ref_key])
        else:
            ref_key_dict[ref_key] = 1

        f = open(mode+save_suffix, 'a')

        # type of bib
        f.write("@article{"+ref_key+',')
        f.write('\n')
        # author
        f.write("author = {"+arxiv.loc[i, 'author']+"},")
        f.write('\n')
        # title
        f.write("title = {{"+arxiv.loc[i, 'title']+"}},")
        f.write('\n')
        # journal
        f.write("journal = {{"+arxiv.loc[i, 'venue']+"}},")
        f.write('\n')
        # year
        f.write("year = {"+str(arxiv.loc[i, 'year'])+"}")
        f.write('\n')
        f.write("}")
        f.write('\n')
        f.write('\n')
        f.close()

    book = pd.read_csv('book.txt', sep='$')
    process_title(book)
    
    for i in range(book.shape[0]):
        print(i)

        ref_key = build_ref_key(book.loc[i])
        if ref_key in ref_key_dict:
            ref_key_dict[ref_key] += 1
            ref_key += str(ref_key_dict[ref_key])
        else:
            ref_key_dict[ref_key] = 1

        f = open(mode+save_suffix, 'a')

        # type of bib
        f.write("@book{"+ref_key+',')
        f.write('\n')
        # author
        f.write("author = {"+book.loc[i, 'author']+"},")
        f.write('\n')
        # title
        f.write("title = {{"+book.loc[i, 'title']+"}},")
        f.write('\n')
        # publisher
        f.write("publisher = {"+book.loc[i, 'publisher']+"},")
        f.write('\n')
        # year
        f.write("year = {"+str(book.loc[i, 'year'])+"}")
        f.write('\n')
        f.write("}")
        f.write('\n')
        f.write('\n')
        f.close()
    
    website = pd.read_csv('website.txt', sep='$')

    for i in range(website.shape[0]):

        print(i)
        ref_key = website.loc[i, 'key']

        f = open(mode+save_suffix, 'a')

        f.write("@misc{"+ref_key+',')
        f.write('\n')

#        f.write("title = {"+website.loc[i, 'title']+"},")
#        f.write('\n')
        f.write(r"howpublished = {\url{"+website.loc[i, 'url']+"}},")
        f.write('\n')
#        f.write("note = {}")
#        f.write('\n')
        f.write("}")
        f.write('\n')
        f.write('\n')
        f.close()


mode = sys.argv[1]

if os.path.exists(mode+save_suffix):
    os.remove(mode+save_suffix)

build_bib(mode)
