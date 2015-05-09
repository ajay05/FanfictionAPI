__author__ = 'jwsm'

from bs4 import BeautifulSoup
from src import urls

import requests


class Category(object):
    """
    Represents a category, as found at http://www.fanfiction.net/medium/category
    Do not access member variables directly
    """

    def __init__(self, url, html=None):
        """
        Construct a category from its url. The html arg is intended for testing purposes.

        Args:
            url (str): The url of the category to construct
        """
        self._url = urls.normalize_url(url)

        if html:
            self._html = BeautifulSoup(html)
        else:
            self._html = BeautifulSoup(requests.get(self._url).text)

        self._num_pages = None
        self._current_page = None
        self._params = {'p': str(self.current_page_number())}
        self._param_keys = {
            'censorid': 'r',
            '_genreid1': 'g',
            'timerange': 't',
            'sortid': 'srt',
            'languageid': 'lan',
            'length': 'len',
            'statusid': 's',
            'verseid1': 'v1',
            'characterid1': 'c',
            'withpairing': 'pm',
        }
        self._filters = {}

    def num_pages(self):
        """
        Find the number of pages in the category

        Returns:
            int: Number of pages in the category
        """
        if not self._num_pages:
            nav_bar = self._html.find('center')

            # if there are no links to more pages
            if nav_bar is None:
                self._num_pages = 1
                return self._num_pages

            last_url = nav_bar.find('a', text='Last')

            # there is no link to 'Last'
            if last_url is None:
                self._num_pages = 2
                return self._num_pages

            self._num_pages = urls.extract_page_number(last_url['href'])
        return self._num_pages

    def current_page_number(self):
        """
        Get the number of the current page.

        Returns:
            int: page number
        """
        if not self._current_page:
            self._current_page = urls.extract_page_number(self._url)
        return self._current_page

    def next_page(self):
        """
        Get the next page in the category, or None if on the last page

        Returns:
            Category: next page in category
        """
        if self.current_page_number() == self.num_pages():
            return None
        return self.get_page(self.current_page_number() + 1)

    def previous_page(self):
        """
        Get the previous page in the category, or None if on the first page

        Returns:
            Category: previous page in the category
        """
        if self.current_page_number() == 1:
            return None
        return self.get_page(self.current_page_number() - 1)

    def get_page(self, page_number):
        """
        Get an arbitrary page in a category, given the page number

        Args:
            page_number (int): number of the desired page

        Returns:
            Category: the desired page
        """

        params = urls.parameters(self._url)

        self._params['p'] += 1
        self._url = self.build_filtered_url()
        if len(params) == 0:
            new_url = self._url + '?&p=' + str(page_number)

        else:
            new_url = self._url.replace('p=' + str(self.current_page_number()), 'p=' + str(page_number))

        return Category(new_url)

    def _get_filter_options(self, filter_name):
        """
        Scrape what values a given filter can take

        Example output:
        {'Rating: All': 10,
         '(? Ratings Guide)': -1,
         'Rated K -> T': 102,
        }

        Args:
            filter_name (str): name of filter, as used by fanfiction.net source

        Returns:
            {str: int}: Mapping from filter value to corresponding url query param argument
        """
        if filter_name not in self._filters:
            options = self._html.find(attrs={'name': filter_name}).contents[1:]
            values = urls.get_param_args(options)
            self._filters[filter_name] = values

        return self._filters[filter_name]

    def sort_by_options(self):
        """
        Returns:
            {str: int}: possible values for Sort By filter
        """
        return self._get_filter_options('sortid')

    def time_range_options(self):
        """
        Returns:
            {str: int}: possible values for Time Range filter
        """
        return self._get_filter_options('timerange')

    def genre_options(self):
        """
        Returns:
            {str: int}: possible values for Genre filter
        """
        return self._get_filter_options('_genreid1')

    def ratings(self):
        """
        Returns:
            {str: int}: possible values for Ratings filter
        """
        return self._get_filter_options('censorid')

    def languages(self):
        """
        Returns:
            {str: int}: possible values for Languages filter
        """
        return self._get_filter_options('languageid')

    def length(self):
        """
        Returns:
            {str: int}: possible values for Length filter
        """
        return self._get_filter_options('length')

    def status(self):
        """
        Returns:
            {str: int}: possible values for Status filter
        """
        return self._get_filter_options('statusid')

    def worlds(self):
        """
        Returns:
            {str: int}: possible values for Worlds filter
        """
        return self._get_filter_options('verseid1')

    def characters(self):
        """
        Returns:
            {str: int}: possible values for Characters filter
        """
        chars = self._get_filter_options('characterid1')
        chars[0] = chars[0][:-4].strip()
        return chars

    def _set_filter(self, filter_name, option, selection=None, with_filter=True):
        """
        Set a filter for the Category by modifying the query params

        Args:
            filter_name (str): The name of the filter to set, as used in fanfiction.net's source
            option (str): The value that the filter should take. Possibly options may be found by calling
                          the appropriate accessor method
            selection (str): 'A', 'B', 'C', or 'D'. Which option to set
            with_filter (boolean): if True, method will set the With filter. If not, method will set the
                                   Without filter
        """
        selection_dict = {
            'A': '1',
            'B': '2',
            'C': '3',
            'D': '4',
        }

        if option not in self._get_filter_options(filter_name):
            raise ValueError('%s is not recognized' % option)

        key = self._param_keys[filter_name]

        if not with_filter:
            key = '_' + key

        if selection:
            key += selection_dict[selection]

        self._params[key] = self._get_filter_options(filter_name)[option]

    def set_sorting_method(self, option):
        """
        Set the Sort By filter

        Args:
            option (str): the name of the sorting method to use
        """
        self._set_filter('sortid', option)

    def set_time_range(self, option):
        """
        Set the Time Range filter

        Args:
            option (str): the name of the time range to use
        """
        self._set_filter('timerange', option)

    def set_genre_filter(self, genre, selection, with_filter=True):
        """
        Set the Genre filter
        If with_filter is False, selection must be None.

        Args:
            genre (str): the name of the genre to use
            selection (str): 'A' or 'B', to select the appropriate genre filter
            with_filter (boolean): if True, sets With filter. If False, sets Without filter
        """
        if selection != 'A' and selection != 'B':
            raise ValueError('selection arg should be \'A\' or \'B\'')

        if selection and not with_filter:
            raise ValueError('Without Genre filter has only one option')

        self._set_filter('_genreid1', genre, selection, with_filter)

    def set_rating_filter(self, rating):
        """
        Set the Rating filter

        Args:
            rating (str): the ratings to include
        """
        self._set_filter('censorid', rating)

    def set_language_filter(self, language):
        """
        Set the Language filter

        Args:
            language (str): the language to include
        """
        self._set_filter('languageid', language)

    def set_length_filter(self, length):
        """
        Set the Length filter

        Args:
            length (str): the length to use
        """
        self._set_filter('length', length)

    def set_status_filter(self, status):
        """
        Set the Status filter

        Args:
            status (str): the length to use
        """
        self._set_filter('statusid', status)

    def set_world_filter(self, world, with_filter=True):
        """
        Set the World filter

        Args:
            world (str): the world to use
            with_filter (boolean): if True, sets With filter. Else: sets Without filter
        """
        self._set_filter('verseid1', world, with_filter)

    def set_character_filter(self, character, selection, with_filter=True):
        """
        Set the Character filter
        if with_filter is False, selection must be 'A' or 'B'

        Args:
            character (str): the name of the character to use
            selection (str): 'A', 'B', 'C', or 'D', to select the appropriate filter
            with_filter (boolean): if True, sets With filter. Else, sets Without filter
        """
        if selection not in ['A', 'B', 'C', 'D']:
            raise ValueError("Character selection must be 'A', 'B', 'C', or 'D'")
        if not with_filter:
            if selection not in ['A', 'B']:
                raise ValueError('Character filter only has two options')

        self._set_filter('characterid1', character, selection, with_filter)

    def set_with_pairing_filter(self, setting, with_filter=True):
        """
        Set the With_pairing filter

        Args:
            setting (Boolean): if True, filter is set. If False, turned off
            with_filter (Boolean): if True, With filter is used, If False, Without filter is used
        """
        key = 'pm'

        if not with_filter:
            key = '_' + key

        if setting is True:
            self._params[key] = '1'
        else:
            self._params.pop(key, None)

    def build_filtered_url(self):
        """
        Get the new url, based on all the applied filters

        Returns:
            str: category url
        """
        url = self._url
        if '?' in url:
            url = url.split('?')[0]
        url += '?'

        for param in self._params.keys():
            url += '&' + param + '=' + self._params[param]

        self._url = url
        return url

    def clear_filters(self):
        """
        Remove all filters, except for page number
        """
        self._params = {'p': str(self.current_page_number())}
