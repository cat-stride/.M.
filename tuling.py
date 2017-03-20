import requests
import json

class T_Robot(object):
	address = 'http://www.tuling123.com/openapi/api'
	APIkey = 'ba0ffa6414364c47a72952b2a3ca2dec'
	TALK = False

	def post_msg_to_tulingrobot(self, uid, msg):
		userid = uid.replace('@','')[:30]
		body = {'key':self.APIkey, 'info': msg}
		req = requests.post(self.address, data=body)
		rep = json.loads(req.text)
		if rep['code'] == 100000: # text
			rt = rep['text']
		elif rep['code'] == 200000: # link
			rt = rep['text'] + "\n" + rep['url']
		elif rep['code'] == 302000: # news
			rt = ''
		elif rep['code'] == 308000: # food
			rt = ''
		return rt


