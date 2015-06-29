__author__ = "akotian"

''' Tests for Author class '''

import sys
sys.path.append('../FanfictionAPI')
from FanfictionAPI.author import Author
from FanfictionAPI.fanfic import Fanfic
import unittest


class TestAuthor(unittest.TestCase):

  def setUp(self):
    self.author_url = 'https://www.fanfiction.net/u/4223235/G01den-Unicorn-11'
    self.author_file_name = 'golden_unicorn.html'
    self.author_file_html = open(self.author_file_name, 'r').read()
    self.author = Author(self.author_url, self.author_file_html)

  def test_get_fanfics(self):  
    self.assertIsInstance(next(self.author.get_fanfics()), Fanfic, 'Correct type returned')

  def test_get_favorite_fanfics(self):  
    self.assertIsInstance(next(self.author.get_favorite_fanfics()), Fanfic, 'Correct type returned')

  def test_get_favorite_authors(self):  
    self.assertIsInstance(next(self.author.get_favorite_authors()), Author, 'Correct type returned')

  def test_is_beta_reader(self):  
    expected = 1 
    self.assertEqual(self.author.is_beta_reader(), expected, "Correct result")

  def test_get_join_date(self):  
    expected = '08-26-12' 
    self.assertEqual(self.author.get_join_date(), expected, "Correct join date")

  def test_get_last_profile_update(self):  
    expected = '04-18-15' 
    self.assertEqual(self.author.get_last_profile_update(), expected, "Correct updated date")

  def test_get_id(self):  
    expected = '4223235' 
    self.assertEqual(self.author.get_id(), expected, "Correct id")

  def test_get_country(self):  
    expected = 'USA' 
    self.assertEqual(self.author.get_country(), expected, "Correct country")

if __name__ == '__main__':
    unittest.main()

