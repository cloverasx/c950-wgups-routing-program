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

    @staticmethod
    def abbreviate_common_address_suffixes(s):
        suffixes = {
            "street": "st",
            "avenue": "ave",
            "boulevard": "blvd",
            "drive": "dr",
            "court": "ct",
            "circle": "cir",
            "place": "pl",
            "road": "rd",
            "lane": "ln",
            "trail": "trl",
            "parkway": "pkwy",
            "highway": "hwy",
            "north": "n",
            "south": "s",
            "east": "e",
            "west": "w",
            "station": "sta",
            "loop": "lp",
            "valley": "vly",
        }
        for suffix, abbreviation in suffixes.items():
            s = s.replace(suffix, abbreviation)
        return s

    @staticmethod
    def clean_string(s):
        # Note: I was having problems finding the data in the xlsx file and found
        # that this could clean up the data.
        s = str(s)
        s = StringUtils.remove_commas(s)
        s = StringUtils.clean_whitespace(s)
        s = StringUtils.convert_to_lowercase(s)
        s = StringUtils.abbreviate_common_address_suffixes(s)
        return s
