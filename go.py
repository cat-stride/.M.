import time
import oneshot
import itchat
from itchat.content import *
from tuling import T_Robot as TR

@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING])
def text_reply(msg):
    print(msg)
    print(itchat.search_friends(userName=msg['FromUserName']))
    user_message = msg['Content'].strip()  
    msgid = msg['NewMsgId']

    if oneshot.ping() != 200:
        itchat.send('宝宝休息时', msg['FromUserName'])
        return

    else:
        if user_message in ['get all','GET ALL']: # 取全部记录
            itchat.last_msg = 'get all'
            rt = oneshot.get_list()
            itchat.send(rt, msg['FromUserName'])

        elif user_message in ['get']: # 取今天记录
            itchat.last_msg = 'get'
            rt = '上线中'
            itchat.send(rt, msg['FromUserName'])

        elif user_message in ['today','delay','done','future','note','event']: # 取分类记录
            itchat.last_msg = 'type'
            rt = '上线中'
            itchat.send(rt, msg['FromUserName'])

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
    print('add_friend->NickName:',msg['RecommendInfo']['NickName'])
    print('add_friend->UserName:',msg['RecommendInfo']['UserName'])
    print('add_friend->Alias:',msg['RecommendInfo']['Alias'])
    print('FromUserName:',msg['FromUserName'])
    rt = oneshot.register(msg['RecommendInfo']['Alias']) # 
    print('rt:',rt)
    if rt == 404:
        return
    user_id = rt['id']
    
    itchat.add_friend(**msg['Text']) # 该操作会自动将新好友的消息录入，不需要重载通讯录
    itchat.send_msg('Nice to meet you!', msg['RecommendInfo']['UserName'])
    # itchat.set_alias(msg['FromUserName'], user_id)
    itchat.set_alias(msg['RecommendInfo']['UserName'], user_id)

@itchat.msg_register(TEXT, isGroupChat=True)
def text_reply(msg):
    # if msg['isAt']:
        # itchat.send(u'@%s\u2005I received: %s' % (msg['ActualNickName'], msg['Content']), msg['FromUserName'])

    print(msg['ActualUserName'])
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
itchat.auto_login(True, enableCmdQR=2)
itchat.run()

# 联系人 msg 消息体

# {
# 'Type': 'Text', 
# 'ImgHeight': 0, 
# 'FromUserName': '@4ec9c3bd199b22aa5bb745097e95198c', 
# 'StatusNotifyUserName': '', 
# 'FileName': '', 
# 'Text': '哈喽', 
# 'MediaId': '', 
# 'VoiceLength': 0, 
# 'OriContent': '', 
# 'FileSize': '', 
# 'ForwardFlag': 0, 
# 'CreateTime': 1490234824, 
# 'HasProductId': 0, 
# 'Content': '哈喽', 
# 'Url': '', 
# 'MsgId': '4066706357555293426', 
# 'MsgType': 1, 
# 'ToUserName': '@74e86974b831d7a222ea21c853f6614cea64d89ae7fbfca0b2d17c3c114e4138', 
# 'RecommendInfo': {'OpCode': 0, 'VerifyFlag': 0, 'Scene': 0, 'Sex': 0, 'NickName': '', 'Content': '', 'City': '', 'AttrStatus': 0, 'QQNum': 0, 'Province': '', 'Ticket': '', 'UserName': '', 'Alias': '', 'Signature': ''}, 
# 'PlayLength': 0, 
# 'NewMsgId': 4066706357555293426, 
# 'AppMsgType': 0, 
# 'Status': 3, 
# 'StatusNotifyCode': 0, 
# 'ImgStatus': 1, 
# 'Ticket': '', 
# 'AppInfo': {'Type': 0, 'AppID': ''}, 
# 'SubMsgType': 0, 
# 'ImgWidth': 0
# }



# 加好友 msg 消息体
# {
# 'Type': 'Friends', 
# 'ImgHeight': 0, 
# 'FromUserName': 'fmessage', 
# 'StatusNotifyUserName': '', 
# 'FileName': '', 
# 'Text': {'verifyContent': '', 'status': 3, 'userName': '@4ec9c3bd199b22aa5bb745097e95198c', 'autoUpdate': {'OpCode': 2, 'VerifyFlag': 0, 'Scene': 3, 'Sex': 1, 'NickName': '大猫黄', 'Content': "I'm 大猫黄", 'City': '广州', 'AttrStatus': 33786685, 'QQNum': 0, 'Province': '广东', 'Ticket': 'v2_2b0cf417273a3d226a8d98ad987dc569017b64252c57693782226caac711a21a79e4519bc26d619192a491276ca34fac00e63a7f2f7ae4111524dda17a51ebdf@stranger', 'UserName': '@4ec9c3bd199b22aa5bb745097e95198c', 'Alias': 'minixiaojeep', 'Signature': '念念不忘，必有回响'}}, 
# 'MediaId': '', 
# 'VoiceLength': 0, 
# 'OriContent': '', 
# 'FileSize': '', 
# 'ForwardFlag': 0, 
# 'CreateTime': 1490234352, 
# 'HasProductId': 0, 
# 'Content': '<msg fromusername="huang-o-wen" encryptusername="v1_dc935c48dc0cd03d0018ecadb493f8ac7b33c9d390d4c40d08d5f1c2f517b040@stranger" fromnickname="大猫黄" content="I&apos;m 大猫黄"  shortpy="DMH" imagestatus="3" scene="3" country="CN" province="Guangdong" city="Guangzhou" sign="念念不忘，必有回响" percard="1" sex="1" alias="minixiaojeep" weibo="" weibonickname="" albumflag="3" albumstyle="0" albumbgimgid="" snsflag="49" snsbgimgid="http://mmsns.qpic.cn/mmsns/4376ae1e0cf0ccced233def9ad1560d0dec29d64941ab85a30d36e9d20551e73d134f94732dc674092655741238a060bb20928f661ef59cc/0" snsbgobjectid="12164827643505160321" mhash="3bdf626c5b02658d3fa2f8b6f6a62d96" mfullhash="3bdf626c5b02658d3fa2f8b6f6a62d96" bigheadimgurl="http://wx.qlogo.cn/mmhead/ver_1/HY0b0Mkn1khUU9xhYvicloCArZsILGl79DViaO2FACEa2XKkGXYzmvmYzfQw7JKRoOtwjOH7xuebIXrtvZ9bgk3G6hm6RXpF9EOldibh7b5EOc/0" smallheadimgurl="http://wx.qlogo.cn/mmhead/ver_1/HY0b0Mkn1khUU9xhYvicloCArZsILGl79DViaO2FACEa2XKkGXYzmvmYzfQw7JKRoOtwjOH7xuebIXrtvZ9bgk3G6hm6RXpF9EOldibh7b5EOc/96" ticket="v2_2b0cf417273a3d226a8d98ad987dc569017b64252c57693782226caac711a21a79e4519bc26d619192a491276ca34fac00e63a7f2f7ae4111524dda17a51ebdf@stranger" opcode="2" googlecontact="" qrticket="" chatroomusername="" sourceusername="" sourcenickname=""><brandlist count="0" ver="642237482"></brandlist></msg>', 
# 'Url': '', 
# 'MsgId': '502740801512222302', 
# 'MsgType': 37, 
# 'ToUserName': '@74e86974b831d7a222ea21c853f6614cea64d89ae7fbfca0b2d17c3c114e4138', 
# 'RecommendInfo': {'OpCode': 2, 'VerifyFlag': 0, 'Scene': 3, 'Sex': 1, 'NickName': '大猫黄', 'Content': "I'm 大猫黄", 'City': '广州', 'AttrStatus': 33786685, 'QQNum': 0, 'Province': '广东', 'Ticket': 'v2_2b0cf417273a3d226a8d98ad987dc569017b64252c57693782226caac711a21a79e4519bc26d619192a491276ca34fac00e63a7f2f7ae4111524dda17a51ebdf@stranger', 'UserName': '@4ec9c3bd199b22aa5bb745097e95198c', 'Alias': 'minixiaojeep', 'Signature': '念念不忘，必有回响'}, 
# 'PlayLength': 0, 
# 'NewMsgId': 502740801512222302, 
# 'AppMsgType': 0, 
# 'Status': 3, 
# 'StatusNotifyCode': 0, 
# 'ImgStatus': 1, 
# 'Ticket': '', 
# 'AppInfo': {'Type': 0, 'AppID': ''}, 
# 'SubMsgType': 0, 
# 'ImgWidth': 0
# }