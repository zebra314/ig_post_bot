import requests
import time
from datetime import datetime


class IG :
  def __init__(self, name, token, video_url, version='v18.0'):
    self.name = name
    self.token = token
    self.video_url = video_url
    self.graph_url = 'https://graph.facebook.com/' + version + '/'
    self.fan_page_id = self.get_fan_page_id()
    self.user_id = self.get_instagram_business_account()
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
      # print('fan page id : ' + fan_page_id)
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
      # print('instagram account id : ' + instagram_account_id)
      return instagram_account_id
    except:
      return {'error':'Instagram account not linked'}
  
  def get_status_of_container(self, container):
    container_id = container['id']
    url = self.graph_url + container_id
    param = {}
    param['access_token'] = self.token
    param['fields'] = 'status_code'
    response = requests.get(url,params=param)
    response = response.json()
    return response
  
  def get_file_name(self):
    start_date = self.start_date
    current_date = datetime.now()
    delta = current_date - start_date
    days = delta.days
    name = 'Day ' + str(days)
    return name
  
  def get_post_data(self):
    url = self.graph_url + self.user_id
    param = dict()
    param['fields'] = 'caption,like_count,media_url,owner,permalink'
    param['access_token'] = self.token
    response = requests.get(url=url, params=param)
    response = response.json()
    return response
  
  def get_media_id(self):
    url = self.graph_url + self.user_id +'/media'
    param = dict()
    param['access_token'] = self.token
    response = requests.get(url =url,params = param)
    response = response.json()
    media = []
    for i in response['data']:
      media_data = self.get_post_data(media_id =i['id'],access_token=self.token)
      media.append(media_data)
    return media
  
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
    response = requests.post(url,params=param)
    response = response.json()
    # print(response)
    return response
  
  def run(self):
    caption = self.get_file_name() + ' #' + self.name
    container = self.pub_reel(self.video_url , caption)
    # print('\nUploading Video\n')
    time.sleep(20)
    # print('\nPublishing Container\n')
    self.pub_container(container)
    # print('\nDone\n')

