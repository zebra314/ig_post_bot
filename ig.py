import requests
import time
from datetime import datetime
import logging
import logging.handlers


class IG :
  def __init__(self, name, token, version='v18.0'):
    self.logger = self.init_logger()
    self.name = name
    self.token = token
    self.graph_url = 'https://graph.facebook.com/' + version + '/'
    self.fan_page_id = self.get_fan_page_id()
    self.user_id = self.get_instagram_business_account()
    self.video_url = self.get_video_url()
    self.start_date = datetime(2023, 12, 7)

  def init_logger(self):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger_file_handler = logging.handlers.RotatingFileHandler(
      "status.log",
      maxBytes=1024 * 1024,
      backupCount=1,
      encoding="utf8",
    )
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    logger_file_handler.setFormatter(formatter)
    logger.addHandler(logger_file_handler)
    return logger
    
  def get_fan_page_id(self):
    '''
    Get fan page id from token
    '''
    url = self.graph_url + 'me/accounts/'
    param = dict()
    param['access_token'] = self.token
    response = requests.get(url=url, params=param)
    response = response.json()

    try:
      fan_page_id = str(response['data'][0]['id'])
      print(self.name + ' fan page id : ' + fan_page_id)
      return fan_page_id
    except:
      self.logger.error(self.name + " cannot get fan page id.")
      raise

  def get_instagram_business_account(self):
    '''
    Get instagram business account id from fan page
    '''
    url = self.graph_url + self.fan_page_id
    param = dict()
    param['fields'] = 'instagram_business_account'
    param['access_token'] = self.token
    response = requests.get(url = url,params=param)
    response = response.json()

    try:
      instagram_account_id = response['instagram_business_account']['id']
      print(self.name + ' ig id : ' + instagram_account_id)
      return instagram_account_id
    except:
      self.logger.error(self.name + " cannot get instagram business account id.")
      raise
  
  def get_file_name(self):
    start_date = self.start_date
    current_date = datetime.now()
    delta = current_date - start_date
    days = delta.days
    name = 'Day ' + str(days)
    return name
  
  def get_video_url(self):
    url = self.graph_url + self.user_id +'/media'
    param = dict()
    param['access_token'] = self.token
    response = requests.get(url =url,params = param)
    response = response.json()

    try:
      video_id = response['data'][0]['id']
    except:
      self.logger.error(self.name + " cannot get video id.")
      raise
  
    url = self.graph_url + video_id
    param['fields'] = 'media_url'
    response = requests.get(url =url,params = param)
    response = response.json()

    try:
      video_url = response['media_url']
      return video_url
    except:
      self.logger.error(self.name + " cannot get video url.")
      raise
  
  def pub_reel(self, video_url, caption=''):
    url = self.graph_url + self.user_id + '/media'
    param = dict()
    param['access_token'] = self.token
    param['caption'] = caption
    param['video_url'] = video_url
    param['media_type'] = 'REELS'
    param['thumb_offset'] = '500'
    param['share_to_feed'] = True
    param['is_comment_enabled'] = True
    response = requests.post(url, params=param)
    response = response.json()
    # print(response)
    return response
  
  def pub_container(self, container):
    url = self.graph_url + self.user_id + '/media_publish'
    param = dict()
    param['access_token'] = self.token
    param['creation_id'] = container['id']
    times = 0
    
    response = requests.post(url,params=param)
    response = response.json()

    while 'error' in response:
      print(self.name + ' container status : ' + response['error']['error_user_msg'])
      time.sleep(15)
      response = requests.post(url,params=param)
      response = response.json()
      if times >= 5:
        print(self.name + 'retry pubbing container too many times, thus quit.')
        self.logger.error(self.name + 'retry pubbing container too many times')
        self.logger.error('cause : ' + response['error']['error_user_msg'])
        break
      times += 1

    if times < 5:
      # print(response)
      print(self.name + ' done pub container.')

  def run(self):
    self.logger.info(self.name + ' start running.')
    caption = self.get_file_name() + ' #' + self.name
    container = self.pub_reel(self.video_url , caption)
    self.pub_container(container)
    self.logger.info(self.name + ' finish running.')