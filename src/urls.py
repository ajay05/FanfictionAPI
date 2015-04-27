__author__ = 'jwsm'

'''
This file contains utility functions for validating and
manipulating urls. For internal use only. Not part of the
public API.
'''

import re

# like an enum
Fanfic = "Fanfic"

fanfiction_base_url = "http://www.fanfiction.net"

fanfiction_base_regex = '^https?://(www|m)\.fanfiction\.net'
story_partial_regex = '/s/\d+/\d+/.'
user_partial_regex = '/u/\d+/.'

compiled_fanfic_regex = re.compile(fanfiction_base_regex + story_partial_regex)


def is_url(string):
    return re.compile('^https?://').match(string)


def classify_url(url):
    """
    Determines the sort of page the input url links to. It is assumed that
    the user is on fanfiction.net.

    Arg:
        url (str): The url to classify

    Returns:
        str: a string (defined in urls.py) representing the type of page the url is linking to

        Possible results:
        Fanfic: An actual fanfic
    """

    if compiled_fanfic_regex.match(url):
        return Fanfic
    return None


def normalize_url(url):
    """
    Convert a url into a standard format. Https will be converted to http,
    and mobile links will be converted to regular links.

    Arg:
        url (str): The url to normalize

    Returns:
        str: the resultant url
    """

    https_regex = re.compile('^https://.')
    mobile_url_regex = re.compile('^https?://m\..')

    if mobile_url_regex.match(url):
        url = url.replace('://m.', '://www.', 1)
    if https_regex.match(url):
        url = url.replace('https://', 'http://', 1)
    return url
