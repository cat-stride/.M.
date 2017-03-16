import requests

POST_API = 'http://182.254.229.127:5000/api/bullets'
GET_API = 'http://182.254.229.127:5000/api/bullets'

def post_oneshot(data):
	print('传入远端data:',data)

	r = requests.post(POST_API, data=data)
	print(type(r),r)
	if r.status_code == 200:
		return 200
	return 'Post failed'


def get_oneshot():
	r = requests.get(GET_API)

	if r.status_code == 200:
		return r.json()
	return 'Not found'