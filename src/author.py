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
    self._html = Fanfic(self._url, html)._get_html()


  def get_fanfics(self):  
    '''
    Returns:
      Authors fanfics
    '''
    if self._fanfics is None:
      title = self._html.select("#st .mystories .stitle")
      self._fanfics = self._get_title_and_links(title)
      return self._fanfics

  def get_favorite_fanfics(self):  
    '''
    Returns:
      Authors favorite fanfics
    '''
    if self._favorite_fanfics is None:
      title = self._html.select("#fs .favstories .stitle")
      self._favorite_fanfics = self._get_title_and_links(title)
      return self._favorite_fanfics

  def get_favorite_authors(self):  
    '''
    Returns:
      Authors favorite authors 
    '''
    if self._favorite_authors is None:
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
    if self._beta_reader is None:
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
    if self._join_date is None:
      table = self._html.select('#bio')[0].find_previous_sibling("table")
      self._join_date = table.select('tr:nth-of-type(3) td span')[0].get_text()
      return self._join_date

  def get_last_profile_update(self):  
    '''
    Returns:
      Last profile update date 
    '''
    if self._profile_update_date is None:
      table = self._html.select('#bio')[0].find_previous_sibling("table")
      self._profile_update_date = table.select('tr:nth-of-type(3) td span:nth-of-type(2)')[0].get_text()
      return self._profile_update_date

  def get_id(self):  
    '''
    Returns:
      Author id 
    '''
    if self._author_id is None:
      table = self._html.select('#bio')[0].find_previous_sibling("table")
      data = table.select('tr:nth-of-type(3) td')[0].get_text()
      result = data.split(",") 
      if 'id' in result[1]:
        self._author_id = result[1].split(":")[1].strip()
      else:
        self._author_id = -1  
      return self._author_id 

  def get_country(self):  
    '''
    Returns:
      Author's country 
    '''
    if self._author_country is None:
      table = self._html.select('#bio')[0].find_previous_sibling("table")
      self._author_country = table.select('tr:nth-of-type(3) td img')[0].attrs['title']
      return self._author_country

