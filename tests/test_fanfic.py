__author__ = 'jwsm'

''' Tests for Fanfic class '''

from src import fanfic
from datetime import date

import unittest


class TestFanfic(unittest.TestCase):

    def setUp(self):
        self.fic_url = 'https://www.fanfiction.net/s/10262834/1/The-Consuming-Desert'
        self.mobile_fic_url = 'https://m.fanfiction.net/s/10262834/1/The-Consuming-Desert'
        self.crossover_url = 'https://www.fanfiction.net/s/11193694/1/The-Hidden-Side-Of-Me-You-Never-Knew'

        self.fic_file_name = 'fics/consuming_desert.html'
        self.fic_html = open(self.fic_file_name, 'r').read()
        self.fic = fanfic.Fanfic(self.fic_url, self.fic_html)

    def test_fanfic_constructor_returns_fanfic(self):
        fic = fanfic.Fanfic(self.fic_url)
        self.assertIsInstance(fic, fanfic.Fanfic, "constructor does not return a Fanfic")

    def test_fanfic_constructor_reads_txt_file(self):
        self.assertIsInstance(self.fic, fanfic.Fanfic, "constructor does not return a Fanfic")

    def test_fanfic_constructor_returns_fanfic_for_mobile_url(self):
        mobile_fic = fanfic.Fanfic(self.mobile_fic_url, self.fic_html)
        self.assertIsInstance(mobile_fic, fanfic.Fanfic, "constructor does not recognize mobile urls")

    def test_fanfic_constructor_works_with_crossover(self):
        fic = fanfic.Fanfic(self.crossover_url, self.fic_html)
        self.assertIsInstance(fic, fanfic.Fanfic, "constructor fails with crossover url")

    def test_construction_fails_with_non_url_argument(self):
        with self.assertRaises(ValueError):
            fanfic.Fanfic("foo")
        with self.assertRaises(ValueError):
            fanfic.Fanfic("")

    def test_fanfic_has_correct_title(self):
        self.assertEqual(self.fic.get_title(), "The Consuming Desert", "Title is not correct")

    def test_get_fanfic_author(self):
        self.assertEqual(self.fic.get_author(), "G01den Unicorn 11", "Author is not correct")

    def test_author_url(self):
        self.assertEqual(self.fic.get_author_url(), "http://www.fanfiction.net/u/4223235/G01den-Unicorn-11",
                         "Author url is not correct")

    def test_summary(self):
        self.assertTrue(self.fic.get_summary().startswith("Lorem"), 'Summary is not correct')
        self.assertTrue(self.fic.get_summary().endswith("elit."), 'Summary is not correct')

    def test_rating(self):
        # Note: Actual fic on site does not have rating of K+.
        # Modified for local file for more robust testing.
        self.assertEqual(self.fic.get_rating(), 'K+', 'Rating is not correct')

    def test_language(self):
        self.assertEqual(self.fic.get_language(), 'English')

    def test_genres(self):
        genres = self.fic.get_genres()
        self.assertEqual(len(genres), 2)
        # Actual fic does not have genre of Hurt/Comfort
        # Modified in local file for more robust testing
        self.assertEqual(genres[0], 'Adventure')
        self.assertEqual(genres[1], 'Hurt/Comfort')

    def test_characters(self):
        characters = self.fic.get_characters()
        for character in ['Link', 'Zelda', 'Nabooru']:
            self.assertIn(character, characters, "%s not in character list" % character)

    def test_characters_when_pairings_exist(self):
        fic = fanfic.Fanfic('https://www.fanfiction.net/s/11008652/1/Fantiality-Infinity',
                            open('fics/pairings1.html').read())

        characters = fic.get_characters()
        for character in ['Link', 'OC', 'Dark Link', 'Malon']:
            self.assertIn(character, characters, "%s not in character list" % character)

    def test_pairings(self):
        fic = fanfic.Fanfic('https://www.fanfiction.net/s/11008652/1/Fantiality-Infinity',
                            open('fics/pairings1.html').read())

        pairings = fic.get_pairings()
        self.assertIn('Link', pairings[0])
        self.assertIn('OC', pairings[0])
        self.assertIn('Dark Link', pairings[1])
        self.assertIn('Malon', pairings[1])

    def test_single_pairing(self):
        fic = fanfic.Fanfic('https://www.fanfiction.net/s/11008652/1/Fantiality-Infinity',
                            open('fics/single_pairing_test.html').read())

        pairings = fic.get_pairings()
        self.assertIn('Link', pairings[0])
        self.assertIn('OC', pairings[0])
        self.assertEqual(len(pairings), 1)

    def test_chapters(self):
        self.assertEqual(18, self.fic.get_chapters())

    def test_word_count(self):
        self.assertEqual(55797, self.fic.get_word_count())

    def test_reviews(self):
        self.assertEqual(73, self.fic.get_reviews())

    def test_favorites(self):
        self.assertEqual(23, self.fic.get_favorites())

    def test_follows(self):
        self.assertEqual(37, self.fic.get_follows())

    def test_id(self):
        self.assertEqual(10262834, self.fic.get_id())

    def test_get_updated(self):
        self.assertEqual(date.fromtimestamp(1427508274), self.fic.get_updated())
        not_updated_fic = fanfic.Fanfic('https://www.fanfiction.net/s/11008652/1/Fantiality-Infinity',
                                        open('fics/single_pairing_test.html').read())
        self.assertEqual(date.fromtimestamp(1422594060), not_updated_fic.get_updated())

    def test_published(self):
        self.assertEqual(date.fromtimestamp(1397299783), self.fic.get_published())
        not_updated_fic = fanfic.Fanfic('https://www.fanfiction.net/s/11008652/1/Fantiality-Infinity',
                                        open('fics/single_pairing_test.html').read())
        self.assertEqual(date.fromtimestamp(1422594060), not_updated_fic.get_published())

    def test_reviews_url(self):
        self.assertEqual('http://www.fanfiction.net/r/10262834/', self.fic.get_reviews_url())
        print(self.fic.get_reviews_dict())


if __name__ == '__main__':
    unittest.main()
