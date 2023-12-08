import requests
import time
from datetime import datetime


class IG :
  def __init__(self, name, token, version='v18.0'):
    self.name = name
    self.token = token
    self.graph_url = 'https://graph.facebook.com/' + version + '/'
    self.fan_page_id = self.get_fan_page_id()
    self.user_id = self.get_instagram_business_account()
    self.video_url = self.get_video_url()
    self.start_date = datetime(2023, 12, 7)
    
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
      return {'error':'Fan page not found'}

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
      return {'error':'Instagram account not linked'}
  
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

    video_id = response['data'][0]['id']
    url = self.graph_url + video_id
    param['fields'] = 'media_url'
    response = requests.get(url =url,params = param)
    response = response.json()
    video_url = response['media_url']
    print(self.name + ' video url : ' + video_url)
    return video_url
  
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
    # print(self.name + ' video status : ' + response) 
    print(response)
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
        print('Retry too many times')
        break
      times += 1

    if times < 5:
      print(response)
      print('Done')

  def run(self):
    caption = self.get_file_name() + ' #' + self.name
    container = self.pub_reel(self.video_url , caption)
    self.pub_container(container)