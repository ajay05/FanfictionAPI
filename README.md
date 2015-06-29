# FanfictionAPI
An API for accessing fanfiction.net data

There are four user-accessible classes: Author, Fanfic, FanficListing, and BetaListing

Public methods for Author:
.get_fanfics()
.get_favorite_fanfics()
.get_favorite_authors()

The above three method return generators containing Fanfic or Author objects respectively

.is_beta_reader() returns true if the author is willing to beta
.get_id() returns the Author id
.get_country() should be obvious

.get_last_profile_update()
.get_join_date()

The above two methods will return Date objects in the next update

--------------------------

Public methods for Fanfic:
.get_title()
.get_url()
.get_author() #returns Author object
.get_author_url()
.get_summary()
.get_rating()
.get_language()
.get_genres()
.get_characters()
.get_pairings() #Each pairing is denoted by a string tuple
.get_chapters()
.get_word_count()
.get_reviews()
.get_favorites()
.get_follows()
.get_published_date()
.get_updated_date()
.get_id()
.get_reviews_url()

The above should all be obvious. One method remains

.get_reviews_dict() returns a dictionary. The key is a string representing the name of a reviewer.
The value is the number of reviews said author has left on the fic.

--------------------

The *Listing classes work a little differently. I'm bored, so I'll document them later.
