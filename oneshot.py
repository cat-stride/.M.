import requests
import urllib.request
import json
import time

WEB_REST_API = 'http://127.0.0.1:5000/wechat/api/bullets'
PING = 'http://127.0.0.1:5000'
# PING = 'http://112.74.191.114'

def post_oneshot(data):
	r = requests.post(WEB_REST_API, data=data)
	if r.status_code == 200:
		return 200
	return 'Post failed'

def get_oneshot(user_id):
	url = WEB_REST_API + '/?user_id=' + user_id
	r = requests.get(url)
	if r.status_code == 200:
		return r.json()
	return 'Not found'

def help():
	info = """
	One Shot 有以下类型
	1.今日待办(today)
	2.延期待办(delay)
	3.预订待办(future)
	4.待办完成(done)
	5.一般笔记(note)
	6.事件(event)
	发送一条消息给机器人，机器人提示是否保存
	发送'help'或'?'获取帮助信息
	发送'get'获取本人今天的记录
	发送'get all'获取本人所有记录
	发送类型英文代码，获取本人该类型记录，如发送'delay'，获取延期待办记录
	机器人每天早上8:00会推送今日待办提醒
	"""
	return info

def ping():
	try:
		p = urllib.request.urlopen(PING)
		if p.getcode() == 200:
			return 200
		else:
			return 404
	except URLError:
		return 404

def get_list(user_id):
	oneshots = get_oneshot(user_id)
	rt = ''
	for shot in oneshots:
		rt += '子弹id :' + str(shot['id']) + '\n' + \
		"符号名：" + shot['type']  + '\n' + "内容：" + \
		shot['content']  + '\n' +  "记录日期：" + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(shot['timestamp'])) + '\n'
	if len(oneshots) == 0:
		rt = '没有记录'
	return rt

def select_oneshot():
	radio = """
	是否保存上述内容？回复以下其中一个数字：
	1.今日待办(today)
	2.延期待办(delay)
	3.预订待办(future)
	4.待办完成(done)
	5.一般笔记(note)
	6.事件(event)
	7.唠嗑(LK)
	不回复或回复7都将不保存
	需要帮助请回复help
	"""
	return radio

def save_oneshot(user_id, type, content):
	data = {}
	if int(type) == 1:
		data['type'] = 'today'
		data['content'] = content
		data['user_id'] = user_id
		post_data = json.dumps(data)
		rt = post_oneshot(post_data)
		if rt != 200:
			return 'Today post failed'
	elif int(type) == 2:
		data['type'] = 'delay'
		data['content'] = content
		data['user_id'] = user_id
		post_data = json.dumps(data)
		rt = post_oneshot(post_data)
		if rt != 200:
			return 'Delay post failed'
	elif int(type) == 3:
		data['type'] = 'future'
		data['content'] = content
		data['user_id'] = user_id
		post_data = json.dumps(data)
		rt = post_oneshot(post_data)
		if rt != 200:
			return 'Future post failed'
	elif int(type) == 4:
		data['type'] = 'done'
		data['content'] = content
		data['user_id'] = user_id
		post_data = json.dumps(data)
		rt = post_oneshot(post_data)
		if rt != 200:
			return 'Done post failed'
	elif int(type) == 5:
		data['type'] = 'note'
		data['content'] = content
		data['user_id'] = user_id
		post_data = json.dumps(data)
		rt = post_oneshot(post_data)
		if rt != 200:
			return 'Note post failed'
	elif int(type) == 6:
		data['type'] = 'event'
		data['content'] = content
		data['user_id'] = user_id
		post_data = json.dumps(data)
		rt = post_oneshot(post_data)
		if rt != 200:
			return 'Event post failed'
	elif int(type) == 7:
		return '那继续唠吧'
	return 'Saved'

def select_bullets_by_type(user_id, btype):
	# 1.今日待办(today)
	# 2.延期待办(delay)
	# 3.预订待办(future)
	# 4.待办完成(done)
	# 5.一般笔记(note)
	# 6.事件(event)
	url = WEB_REST_API + '/type/?user_id=' + user_id + '&type=' + btype
	r = requests.get(url)
	# print(r.text)
	if r.status_code == 200:
		oneshots = r.json()
		rt = ''
		for shot in oneshots:
			rt += '子弹id :' + str(shot['id']) + '\n' + \
			"符号名：" + shot['type']  + '\n' + "内容：" + \
			shot['content']  + '\n' +  "记录日期：" + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(shot['timestamp'])) + '\n'
		if len(oneshots) == 0:
			rt = '没有记录'
		return rt
	return 404

def get_date_bullets(user_id):
	timestamp = int(time.time())
	# date = time.strftime('%Y-%m-%d',time.localtime(timestamp))
	url = WEB_REST_API + '/date/?user_id=' + user_id + '&timestamp=' + str(timestamp)
	r = requests.get(url)
	# print(r.text)
	if r.status_code == 200:
		oneshots = r.json()
		rt = ''
		for shot in oneshots:
			rt += '子弹id :' + str(shot['id']) + '\n' + \
			"符号名：" + shot['type']  + '\n' + "内容：" + \
			shot['content']  + '\n' +  "日期：" + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(shot['timestamp'])) + '\n'
		if len(oneshots) == 0:
			rt = '没有记录'
		return rt
	return 404

def register(wechat_id):
	url = WEB_REST_API + "/register"
	data = {}
	data['wechat_id'] = wechat_id
	post_data = json.dumps(data)
	# print(url,post_data)
	r = requests.post(url, data=post_data)
	# print('r:',r)
	if r.status_code == 200:
		return r.json()
	return 404

def auto_pull_bullets(user_id, btype):
	url = WEB_REST_API + '/type/?user_id=' + user_id + '&type=' + btype
	r = requests.get(url)
	# print(r.text)
	if r.status_code == 200:
		oneshots = r.json()
		rt = ''
		for shot in oneshots:
			rt += '子弹id :' + str(shot['id']) + '\n' + \
			"符号名：" + shot['type']  + '\n' + "内容：" + \
			shot['content']  + '\n' +  "记录日期：" + time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(shot['timestamp'])) + '\n'
		if len(oneshots) == 0:
			rt = '没有记录'
		return rt
	return 404
