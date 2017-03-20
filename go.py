import time
import oneshot
import itchat
from itchat.content import *
from tuling import T_Robot as TR

@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING])
def text_reply(msg):
    print(msg)
    user_message = msg['Content'].strip()
        
    msgid = msg['NewMsgId']

    if oneshot.ping() != 200:
        itchat.send('服务没有启动，请耐心等待。', msg['FromUserName'])
        return

    else:
        if user_message in ['get all','GET ALL']: # 取全部记录
            itchat.last_msg = 'get all'
            rt = oneshot.get_list()
            itchat.send(rt, msg['FromUserName'])

        elif user_message in ['get']: # 取今天记录
            itchat.last_msg = 'get'
            pass

        elif user_message in ['today','delay','done','future','note','event']: # 取分类记录
            itchat.last_msg = 'type'
            pass

        elif user_message in ['1','2','3','4','5','6','7']:
            print(itchat.temp_record,itchat.last_msg)
            if len(itchat.temp_record) == 0 or itchat.last_msg in ['get','get all','help','number','type']:
                itchat.send('想唠嗑？请继续。。。', msg['FromUserName'])
                return
            rt = oneshot.save_oneshot(user_message, itchat.temp_record)
            itchat.send(rt, msg['FromUserName'])
            itchat.last_msg = 'number'

        elif user_message in ['help','HELP','帮助','?','？']:
            itchat.last_msg = 'help'
            rt = oneshot.help()
            itchat.send(rt, msg['FromUserName'])

        else:
            itchat.last_msg = 'other'
            itchat.temp_record = user_message
            rt = oneshot.select_oneshot() 
            itchat.send(rt, msg['FromUserName'])



@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO])
def download_files(msg):
    msg['Text'](msg['FileName'])
    return '@%s@%s' % ({'Picture': 'img', 'Video': 'vid'}.get(msg['Type'], 'fil'), msg['FileName'])

@itchat.msg_register(FRIENDS)
def add_friend(msg):
    itchat.add_friend(**msg['Text']) # 该操作会自动将新好友的消息录入，不需要重载通讯录
    itchat.send_msg('Nice to meet you!', msg['RecommendInfo']['UserName'])

@itchat.msg_register(TEXT, isGroupChat=True)
def text_reply(msg):
    # if msg['isAt']:
        # itchat.send(u'@%s\u2005I received: %s' % (msg['ActualNickName'], msg['Content']), msg['FromUserName'])


    uid = msg['FromUserName']
    msgcontent = msg['Content'].strip()

    if msgcontent in ['stop','STOP']:
        tr.Talk = False
        rt = '轻轻地我走了，正如我轻轻地来，挥一挥衣袖，不带走一片云彩'
        itchat.send(rt, msg['FromUserName'])

    if msgcontent in ['start','START']:
        tr.Talk = True

    if tr.Talk:
        rt = tr.post_msg_to_tulingrobot(uid,msgcontent)
        if len(rt) > 0:
            itchat.send(rt, msg['FromUserName'])



tr = TR()
tr.Talk = True
itchat.auto_login(True,enableCmdQR=2)
itchat.run()