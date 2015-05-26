__author__ = 'akotian'

'''
Autor class
'''
import requests
from bs4 import BeautifulSoup, SoupStrainer
import json
import urls
import re
from fanfic import Fanfic

class Author(object):

  def __init__(self, url=None, html=None):
    """
    Constructor
    """
    self._fanfics = None
    self._favorite_fanfics = None
    self._favorite_authors = None
    self._beta_reader = None
    self._join_date = None
    self._profile_update_date = None
    self._author_id = None
    self._author_country = None
    if url != None:
      self._url = urls.normalize_url(url)
      self._html = Fanfic(url=self._url)._get_html()
    else:
      self._html = Fanfic(html=html)


  def get_fanfics(self):  
    '''
    Returns:
      Authors fanfics
    '''
    title = self._html.select("#st .mystories .stitle")
    self._fanfics = self._get_title_and_links(title)
    return self._fanfics

  def get_favorite_fanfics(self):  
    '''
    Returns:
      Authors favorite fanfics
    '''
    title = self._html.select("#fs .favstories .stitle")
    self._favorite_fanfics = self._get_title_and_links(title)
    return self._favorite_fanfics

  def get_favorite_authors(self):  
    '''
    Returns:
      Authors favorite authors 
    '''
    title = self._html.select("#fa dl a")
    self._author = self._get_title_and_links(title)
    return self._author

  def _get_title_and_links(self, title):
    '''
      Process titles and links
    '''
    data = []
    for i in title:
        data.append([i.get_text(), i.attrs['href']])
    return json.dumps(data)

  def is_beta_reader(self):  
    '''
    Returns:
      Is Beta reader
    '''
    table = self._html.select('#bio')[0].find_previous_sibling("table")
    profile_type = table.select('tr:nth-of-type(2) td a')[0].get_text()
    if (profile_type == 'Beta Profile'):
      self._beta_reader = 1
    else:
      self._beta_reader = 0
    return self._beta_reader  

  def get_join_date(self):  
    '''
    Returns:
      Author join date 
    '''
    table = self._html.select('#bio')[0].find_previous_sibling("table")
    self._join_date = table.select('tr:nth-of-type(3) td span')[0].get_text()
    return self._join_date

  def get_last_profile_update(self):  
    '''
    Returns:
      Last profile update date 
    '''
    table = self._html.select('#bio')[0].find_previous_sibling("table")
    self._profile_update_date = table.select('tr:nth-of-type(3) td span:nth-of-type(2)')[0].get_text()
    return self._profile_update_date

  def get_id(self):  
    '''
    Returns:
      Author id 
    '''
    table = self._html.select('#bio')[0].find_previous_sibling("table")
    data = table.select('tr:nth-of-type(3) td')[0].get_text()
    result = data.split(",") 
    if 'id' in result[1]:
      self._id = result[1].split(":")[1]
    else:
      self._id = -1  
    return self._id 

  def get_country(self):  
    '''
    Returns:
      Author's country 
    '''
    table = self._html.select('#bio')[0].find_previous_sibling("table")
    self._country = table.select('tr:nth-of-type(3) td img')[0].attrs['title']
    return self._country
