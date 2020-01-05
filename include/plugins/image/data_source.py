import json
import requests
from lxml import etree
import sys, threading


class KThread(threading.Thread):
  """A subclass of threading.Thread, with a kill() method.
  Come from:
  Kill a thread in Python:
  http://mail.python.org/pipermail/python-list/2004-May/260937.html
  """
  def __init__(self, *args, **kwargs):
    threading.Thread.__init__(self, *args, **kwargs)
    self.killed = False
  def start(self):
    """Start the thread."""
    self.__run_backup = self.run
    self.run = self.__run  # Force the Thread to install our trace.
    threading.Thread.start(self)
  def __run(self):
    """Hacked run function, which installs the trace."""
    sys.settrace(self.globaltrace)
    self.__run_backup()
    self.run = self.__run_backup
  def globaltrace(self, frame, why, arg):
    if why == 'call':
      return self.localtrace
    else:
      return None
  def localtrace(self, frame, why, arg):
    if self.killed:
      if why == 'line':
        raise SystemExit()
    return self.localtrace
  def kill(self):
    self.killed = True

class TimeoutException(Exception):
  """function run timeout"""

def timeout(seconds):
  def timeout_decorator(func):
    def _new_func(oldfunc, result, oldfunc_args, oldfunc_kwargs):
      result.append(oldfunc(*oldfunc_args, **oldfunc_kwargs))
    def _(*args, **kwargs):
      result = []
      new_kwargs = {  # create new args for _new_func, because we want to get the func return val to result list
        'oldfunc': func,
        'result': result,
        'oldfunc_args': args,
        'oldfunc_kwargs': kwargs
      }
      thd = KThread(target=_new_func, args=(), kwargs=new_kwargs)
      thd.start()
      thd.join(seconds)
      alive = thd.isAlive()
      thd.kill()  # kill the child thread
      if alive:
        # raise Timeout(u'function run too long, timeout %d seconds.' % seconds)
        try:
          raise TimeoutException(u'function run too long, timeout %d seconds.' % seconds)
        finally:
          return None
      else:
        return result[0]
    _.__name__ = func.__name__
    _.__doc__ = func.__doc__
    return _
  return timeout_decorator

class SauceNAO:

  def __init__(self, api_key, output_type=2, testmode=0, dbmask=None, dbmaski=None, db=999, numres=3, shortlimit=20, longlimit=300):
    params = dict()
    params['api_key'] = api_key
    params['output_type'] = output_type
    params['testmode'] = testmode
    params['dbmask'] = dbmask
    params['dbmaski'] = dbmaski
    params['db'] = db
    params['numres'] = numres
    self.params = params
    self.header = "————>saucenao<————"


  def get_sauce(self, url):
    self.params['url'] = url
    response = requests.get('https://saucenao.com/search.php', params=self.params)
    data = response.json()
    
    return data

  def get_view(self, sauce) -> str:
    sauces = self.get_sauce(sauce)

    repass = ""
    try:
      for sauce in sauces['results']:
        url = sauce['data']['ext_urls'][0].replace("\\","").strip()
        similarity = sauce['header']['similarity']
        putline = "[{}] 相似度:{}%".format(url, similarity)
        if repass:
          repass = "\n".join([repass, putline])
        else:
          repass = putline
    except Exception as e:
      pass

    return repass


class ascii2d:

  def __init__(self, num=2):
    self.num = num
    self.header = "————>ascii2d<————"

  def get_search_data(self, url: str, data=None):
    if data is not None:
      html = data
    else:
      # print("get_search_url: ", url)
      html_data = requests.get(url)
      html = etree.HTML(html_data.text)

    all_data = html.xpath('//div[@class="detail-box gray-link"]/h6')
    # print("all_data: ", all_data)
    info = []
    for data in all_data[:self.num]:
      info_url = data.xpath(".//a/@href")[0].strip()
      tag = (data.xpath("./small/text()") or data.xpath(".//a/text()"))[0].strip()
      info.append([info_url, tag])

    return info

  def add_repass(self, tag: str, data):
    po = "——{}——".format(tag)
    for line in data:
      putline = "[{}][{}]".format(line[1], line[0])
      po = "\n".join([po, putline])

    return po

  def get_view(self, ascii2d) -> str:
    url_index = "https://ascii2d.net/search/url/{}".format(ascii2d)
    # print("url_index: ", url_index)
    html_index_data = requests.get(url_index)
    print("[info]index html data OK.")
    html_index = etree.HTML(html_index_data.text)

    a_url_foot = html_index.xpath('//div[@class="detail-link pull-xs-right hidden-sm-down gray-link"]')[0].xpath('./span/a/@href')
    url2 = "https://ascii2d.net{}".format(a_url_foot[1])

    color = self.get_search_data('', data=html_index)
    bovw = self.get_search_data(url2)

    repass = ''
    if color and bovw:
      putline1 = self.add_repass("色调检索", color)
      putline2 = self.add_repass("特征检索", bovw)
    repass = "\n".join([putline1, putline2])

    return repass


@timeout(7)
async def get_view(sc, image_url: str) -> str:
  header = sc.header
  print("[info]Now starting get the {}".format(header))
  view = ''
  putline = ''

  try:
    view = sc.get_view(image_url)
  except TimeoutException as e:
    print("[warning]Time out of the {}".format(header))

  if view:
    putline = "\n\n".join([header, view])
    print("[info]Loading {} page succeeded".format(header))

  return putline

async def get_image_data(image_url: str, api_key: str):
  if type(image_url) == list:
    image_url = image_url[0]

  print("[info]Loading Image Search Container……")
  NAO = SauceNAO(api_key)
  ii2d = ascii2d()

  print("[info]Loading all view……")
  repass = ''
  for sc in [NAO, ii2d]:
    putline = await get_view(sc, image_url)
    if putline:
      if repass:
        repass = "\n\n".join([repass, putline])
      else:
        repass = putline
  
  return repass
