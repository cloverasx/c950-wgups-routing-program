import re


def remove_commas(s):
    return s.replace(",", "")


def clean_whitespace(s):
    return re.sub(r"\s+", " ", s.strip())


def convert_to_lowercase(s):
    return s.lower()
