import sys
import os
import argparse
import pandas as pd
import logging

# constants
DELIMITER = "$"
NEW_LINE = "\n"
SAVE_SUFFIX = "_generated_py3.bib"

# key tracker
REF_KEY_DICT = {}

# filenames
VENUE = "venue_fullname.txt"
CONFERENCE = "conference.txt"
JOURNAL = "journal.txt"
ARXIV = "arxiv.txt"
BOOK = "book.txt"
WEBSITE = "website.txt"


def build_ref_key(bib_item):

    author_list = bib_item["author"].strip().split(" and ")
    ref_key = ""
    for a in author_list:
        name_part = a.strip().split(" ")
        ref_key += name_part[-1][0]
    ref_key += str(bib_item["year"])[2:]

    return ref_key


def process_title(df):
    df["title"] = df["title"].str.replace("<dollar-inline>", "$")


def postprocess_refkey(ref_key):
    if ref_key in REF_KEY_DICT:
        REF_KEY_DICT[ref_key] += 1
        ref_key += str(REF_KEY_DICT[ref_key])
    else:
        REF_KEY_DICT[ref_key] = 1
    return ref_key


def identify_normal_proceedings(basename, venue):
    match venue:
        case "WWW_old":
            proceedings = basename + " (WWW)"
        case "KDD_old":
            proceedings = basename + " (KDD)"
        case "ICWSM_old":
            proceedings = basename + " (ICWSM)"
        case "NeurIPSCT":
            proceedings = basename
        case _:
            proceedings = basename + f" ({venue})"
    return proceedings


def build_conference(f, mode):

    venue_fullname = pd.read_csv(VENUE, sep=DELIMITER)
    conference = pd.read_csv(CONFERENCE, sep=DELIMITER)
    process_title(conference)

    for i in range(conference.shape[0]):

        ref_key = build_ref_key(conference.loc[i])

        if ref_key:
            ref_key = postprocess_refkey(ref_key)

            venue = conference.loc[i, "venue"]
            if mode == "normal":
                basename = venue_fullname.loc[
                    venue_fullname.venue == venue, "fullname"
                ].values[0]
                proceedings = identify_normal_proceedings(basename, venue)
            elif mode == "simple":
                if venue == "WWW_old":
                    proceedings = "WWW"
                else:
                    proceedings = venue

            bib_item = f"""@inproceedings{{{ref_key},{NEW_LINE}"""
            bib_item += f"""author = {{{conference.loc[i, "author"]}}},{NEW_LINE}"""
            bib_item += f"""title = {{{conference.loc[i, "title"]}}},{NEW_LINE}"""
            bib_item += f"""booktitle = {{{proceedings}}},{NEW_LINE}"""

            if not isinstance(conference.loc[i, "pages"], float):
                bib_item += f"""pages = {{{conference.loc[i, "pages"]}}},{NEW_LINE}"""

            if mode == "normal":
                if not isinstance(conference.loc[i, "publisher"], float):
                    bib_item += f"""publisher = {{{conference.loc[i, "publisher"]}}},{NEW_LINE}"""
            elif mode == "simple":
                bib_item += f"""publisher = {{}},{NEW_LINE}"""

            bib_item += f"""year = {{{conference.loc[i, "year"]}}}{NEW_LINE}"""
            bib_item += f"""}}{NEW_LINE}"""

            f.write(bib_item)
            f.write("\n")


def build_journal(f, mode):

    venue_fullname = pd.read_csv(VENUE, sep=DELIMITER)
    journal = pd.read_csv(JOURNAL, sep=DELIMITER)
    process_title(journal)

    for i in range(journal.shape[0]):

        ref_key = build_ref_key(journal.loc[i])

        if ref_key:
            ref_key = postprocess_refkey(ref_key)

            proceedings = venue_fullname.loc[
                venue_fullname.venue == journal.loc[i, "venue"], "fullname"
            ].values[0]

            bib_item = f"""@article{{{ref_key},{NEW_LINE}"""
            bib_item += f"""author = {{{journal.loc[i, "author"]}}},{NEW_LINE}"""
            bib_item += f"""title = {{{journal.loc[i, "title"]}}},{NEW_LINE}"""
            bib_item += f"""journal = {{{proceedings}}},{NEW_LINE}"""
            if not isinstance(journal.loc[i, "publisher"], float):
                bib_item += (
                    f"""publisher = {{{journal.loc[i, "publisher"]}}},{NEW_LINE}"""
                )
            bib_item += f"""year = {{{journal.loc[i, "year"]}}}{NEW_LINE}"""
            bib_item += f"""}}{NEW_LINE}"""
            f.write(bib_item)
            f.write("\n")


def build_arxiv(f, mode):
    arxiv = pd.read_csv(ARXIV, sep=DELIMITER)
    process_title(arxiv)

    for i in range(arxiv.shape[0]):

        ref_key = build_ref_key(arxiv.loc[i])

        if ref_key:
            ref_key = postprocess_refkey(ref_key)

            bib_item = f"""@article{{{ref_key},{NEW_LINE}"""
            bib_item += f"""author = {{{arxiv.loc[i, "author"]}}},{NEW_LINE}"""
            bib_item += f"""title = {{{arxiv.loc[i, "title"]}}},{NEW_LINE}"""
            bib_item += f"""journal = {{{{{arxiv.loc[i, "venue"] }}}}},{NEW_LINE}"""
            bib_item += f"""year = {{{arxiv.loc[i, "year"]}}}{NEW_LINE}"""
            bib_item += f"""}}{NEW_LINE}"""
            f.write(bib_item)
            f.write("\n")


def build_book(f, mode):
    book = pd.read_csv(BOOK, sep=DELIMITER)
    process_title(book)

    for i in range(book.shape[0]):

        ref_key = build_ref_key(book.loc[i])

        if ref_key:
            ref_key = postprocess_refkey(ref_key)

            bib_item = f"""@book{{{ref_key},{NEW_LINE}"""
            bib_item += f"""author = {{{book.loc[i, "author"]}}},{NEW_LINE}"""
            bib_item += f"""title = {{{book.loc[i, "title"]}}},{NEW_LINE}"""
            bib_item += f"""publisher = {{{book.loc[i, "publisher"]}}},{NEW_LINE}"""
            bib_item += f"""year = {{{book.loc[i, "year"]}}}{NEW_LINE}"""
            bib_item += f"""}}{NEW_LINE}"""
            f.write(bib_item)
            f.write("\n")


def build_website(f, mode):
    website = pd.read_csv(WEBSITE, sep=DELIMITER)
    for i in range(website.shape[0]):

        bib_item = f"""@misc{{{website.loc[i, "key"]},{NEW_LINE}"""
        bib_item += f"""howpublished = {{\\url{{{website.loc[i, "url"]}}}}}{NEW_LINE}"""
        bib_item += f"""}}{NEW_LINE}"""
        f.write(bib_item)
        f.write("\n")


def build(mode="normal"):
    with open(mode + SAVE_SUFFIX, "a") as f:
        build_conference(f, mode)
        build_journal(f, mode)
        build_arxiv(f, mode)
        build_book(f, mode)
        build_website(f, mode)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", default="normal", help="bibtex mode (simple/normal)")

    args = parser.parse_args()
    mode = args.mode
    if os.path.exists(mode + SAVE_SUFFIX):
        os.remove(mode + SAVE_SUFFIX)

    build(mode)
