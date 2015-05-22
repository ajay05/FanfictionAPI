__author__ = 'jwsm'

from src import beta
import unittest


class TestBetas(unittest.TestCase):

    def setUp(self):
        self.beta_list = beta.BetaList('https://www.fanfiction.net/betareaders/game/Final-Fantasy-X/',
                                           open('betas_src/beta_page_base.html', 'r').read())

    def test_language_filter(self):
        self.beta_list.set_language_filter('English')
        self.assertIn('languageid=1', self.beta_list.build_filtered_url())

    def test_genre_filter(self):
        self.beta_list.set_genre_filter('Romance')
        self.assertIn('genreid=2', self.beta_list.build_filtered_url())

    def test_rating_filter(self):
        self.beta_list.set_rating_filter('Fiction K >> T')
        self.assertIn('rating=3', self.beta_list.build_filtered_url())

    def test_page_number(self):
        new_page = self.beta_list.get_page(5)
        self.assertIn('&ppage=5', new_page.build_filtered_url())


if __name__ == '__main__':
    unittest.main()

