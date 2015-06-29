__author__ = 'jwsm'

'''Tests for CategoryListing class'''

from FanfictionAPI import categorylisting
import unittest


class TestCategory(unittest.TestCase):

    def setUp(self):
        self.category_url = 'https://www.fanfiction.net/game/Legend-of-Zelda/'
        self.category_src = open('categories/category.html', 'r').read()
        self.category = categorylisting.CategoryListing(self.category_url, self.category_src)

        self.single_page_url = 'https://www.fanfiction.net/game/Double-Dragon/'
        self.single_page_src = open('categories/single_page_category.html', 'r')
        self.single_page_category = categorylisting.CategoryListing(self.single_page_url, self.single_page_src)

        self.double_page_url = 'https://www.fanfiction.net/game/Lego/'
        self.double_page_src = open('categories/double_page_category.html', 'r')
        self.double_page_category = categorylisting.CategoryListing(self.double_page_url, self.double_page_src)

    def test_num_pages(self):
        self.assertEqual(self.category.num_pages(), '910', "page count is incorrect")

    def test_num_pages_with_only_one_page(self):
        self.assertEqual(self.single_page_category.num_pages(), 1, 'page count is incorrect')

    def test_two_pages(self):
        self.assertEqual(self.double_page_category.num_pages(), 2, 'page count is incorrect')

    def test_genres(self):
        self.category.set_genre_filter('Adventure', 'A')
        self.assertIn('g1=6', self.category.build_filtered_url())

    def test_ratings(self):
        self.category.set_rating_filter('Rated T')
        self.assertIn('r=3', self.category.build_filtered_url())

    def test_time_range(self):
        self.category.set_time_range('Updated within 24 hours')
        self.assertIn('t=1', self.category.build_filtered_url())

    def test_languages(self):
        self.category.set_language_filter('Deutsch')
        self.assertIn('lan=4', self.category.build_filtered_url())

    def test_length(self):
        self.category.set_length_filter('> 1K words')
        self.assertIn('len=1', self.category.build_filtered_url())

    def test_status(self):
        self.category.set_status_filter('Complete')
        self.assertIn('s=2', self.category.build_filtered_url())

    def test_worlds(self):
        self.category.set_world_filter('Four Swords', False)
        self.assertIn('_v1=159', self.category.build_filtered_url())
        self.category.set_world_filter('Four Swords', True)
        self.assertIn('v1=159', self.category.build_filtered_url())

    def test_characters(self):
        self.category.set_character_filter('Link', 'B', False)
        self.assertIn('_c2=1315', self.category.build_filtered_url())

    def test_with_pairing_filter(self):
        self.category.set_with_pairing_filter(True, False)
        self.assertIn('_pm=1', self.category.build_filtered_url())


if __name__ == '__main__':
    unittest.main()
