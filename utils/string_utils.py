import re


class StringUtils:
    @staticmethod
    def remove_commas(s):
        return s.replace(",", "")

    @staticmethod
    def clean_whitespace(s):
        return re.sub(r"\s+", " ", s.strip())

    @staticmethod
    def convert_to_lowercase(s):
        return s.lower()
