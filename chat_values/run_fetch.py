
import requests


TARGET_URL = "http://www.verke.org/nusuvefo-kalenteri"
session = requests.Session()
resp = session.get(TARGET_URL)
if resp.status_code != 200:
  raise FetchError("First fetch statuscod failed")


import pdb; pdb.set_trace();