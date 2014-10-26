
import requests



uid = "10152869560301062"
url = "http://graph.facebook.com/%s/picture?type=large" % uid
pic = requests.get(url)
print pic.url
