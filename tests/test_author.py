__author__ = "akotian"

''' Tests for Author class '''

import sys
sys.path.append('../src')
from author import Author
import json
import unittest

class TestAuthor(unittest.TestCase):

  def setUp(self):
    self.author_url = 'https://www.fanfiction.net/u/4223235/G01den-Unicorn-11'
    self.author_file_name = 'golden_unicorn.html'
    self.author_file_html = open(self.author_file_name, 'r').read()
    self.author = Author(self.author_url ,self.author_file_html)

  def test_get_fanfics(self):  
    expected = ["Side Quest", "/s/11210616/1/Side-Quest"], ["The Consuming Desert", "/s/10262834/1/The-Consuming-Desert"], ["A Day in the Life of a Guard Captain", "/s/11019190/1/A-Day-in-the-Life-of-a-Guard-Captain"], ["Tales from the Kokiri Forest", "/s/10834242/1/Tales-from-the-Kokiri-Forest"], ["A Sage's Hymn", "/s/10721967/1/A-Sage-s-Hymn"], ["Data's Discovery", "/s/10620568/1/Data-s-Discovery"], ["Growing Up", "/s/10446938/1/Growing-Up"], ["A Taste of Home", "/s/10113505/1/A-Taste-of-Home"], ["Christmas for the Headmaster", "/s/9953074/1/Christmas-for-the-Headmaster"], ["Sweet Dreams", "/s/9784569/1/Sweet-Dreams"], ["The Darkness Within", "/s/9655643/1/The-Darkness-Within"], ["Sleep", "/s/9443463/1/Sleep"], ["A Time of Shadow", "/s/9179678/1/A-Time-of-Shadow"], ["Final Prayer", "/s/9224006/1/Final-Prayer"]
    self.assertEqual(self.author.get_fanfics(), json.dumps(expected), "Fanfics are correct")
  
  def test_get_favorite_fanfics(self):  
    expected = ["The Devil's Chord", "/s/10839860/1/The-Devil-s-Chord"], ["Swan Song", "/s/11145277/1/Swan-Song"], ["The Two Year Emperor", "/s/9669819/1/The-Two-Year-Emperor"], ["Harry Potter and the Methods of Rationality", "/s/5782108/1/Harry-Potter-and-the-Methods-of-Rationality"], ["Harry Potter and the Natural 20", "/s/8096183/1/Harry-Potter-and-the-Natural-20"], ["The Customer Is (Not) Always Right", "/s/8937503/1/The-Customer-Is-Not-Always-Right"], ["Legend of Zelda: Interlinking", "/s/10203226/1/Legend-of-Zelda-Interlinking"], ["Rationalising Death", "/s/9380249/1/Rationalising-Death"], ["Prince of the Dark Kingdom", "/s/3766574/1/Prince-of-the-Dark-Kingdom"], ["Healing the Moon", "/s/10258745/1/Healing-the-Moon"], ["The Legend of Zelda: Sacred Reliquary", "/s/5444766/1/The-Legend-of-Zelda-Sacred-Reliquary"], ["Red Inheritance", "/s/7618232/1/Red-Inheritance"], ["Tainted Blood", "/s/7470279/1/Tainted-Blood"], ["Insomnia", "/s/4249013/1/Insomnia"], ["The Legacy Of Terabithia", "/s/4525156/1/The-Legacy-Of-Terabithia"]
    self.assertEqual(self.author.get_favorite_fanfics(), json.dumps(expected), "Favorite fanfics are correct")

  def test_get_favorite_authors(self):  
    expected = ["BTM707", "/u/1649925/BTM707"], ["EagleJarl", "/u/5111102/EagleJarl"], ["jdschmidtwriter", "/u/5142579/jdschmidtwriter"], ["LeighEm", "/u/1762588/LeighEm"], ["Less Wrong", "/u/2269863/Less-Wrong"], ["Mizuni-sama", "/u/1355498/Mizuni-sama"], ["Seldavia", "/u/28417/Seldavia"], ["Selphie Kinneas 175", "/u/645774/Selphie-Kinneas-175"], ["tikitikirevenge", "/u/474893/tikitikirevenge"] 
    self.assertEqual(self.author.get_favorite_authors(), json.dumps(expected), "Favorite authors are correct")

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

