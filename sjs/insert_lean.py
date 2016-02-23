# -*- coding: utf-8 -*-
from leancloud import init, Object, Query
import re
from bs4 import BeautifulSoup
from qiniu import Auth, put_data, put_file, etag


__author__ = 'think'

access_key = '3xw5uASc565Mr44Vlt0iimqsZoBk3I0nM88YEjSP'
secret_key = 'ExEjTZG2QCVBktGMuM3YluorvQ28qQ5utK5mobRP'
bucket_name = 'cache'

q = Auth(access_key, secret_key)


# key = 'a\\b\\c"hello qiniu'
# data = 'hello cache'
# token = q.upload_token(bucket_name)
# ret, info = put_data(token, key, data)
# print ret
# print info
# assert ret['key'] == key

# 上传本地文件

localfile = 'thinking.png'
key = 'test_file4'
mime_type = 'text/plain'
params = {'x:a': 'a'}
token = q.upload_token(bucket_name)
ret, info = put_file(token, key, localfile, mime_type=mime_type, check_crc=True)
print info
assert ret['key'] == key
assert ret['hash'] == etag(localfile)
# 这个是div答案类型
# answer_li = """
# <li class="noborder"><font>答案</font><div id='test' class="editorBox"><div>试题解析</div><img width="15" height="15" id="_x000062f3815a-5989-4fbd-a16f-b9e097516179_i1179" src="/uploads/word_import/images/585/1389602487gh5ET6y5hUrvdsWmR08b.gif"></div></li>
# """
# soup = BeautifulSoup(answer_li, 'lxml')
# div = soup.find('div', class_='editorBox')
# div['id'] = 'changed'
# print div

# 这个是b标签答案类型
# answer_li = """
# <li class="noborder"><font>答案</font><div class="editorBox"><br>本题考查求函数值和函数最值、函数的对称性等基础知识，考查学生的转化能力、分析问题解决问题的能力和计算能力．第一问，直接代入<img width="13" height="15" id="_x000062f3815a-5989-4fbd-a16f-b9e097516179_i1264" src="www.yitiku.cn/uploads/word_import/images/666/1389602488tkBJ4C7hV6wBczrOfX8p.gif">求函数值，通过2组数的规律得到猜想，利用对称关系证明结论；第二问，先求出函数的定义域，利用单调性的定义判断函数的单调性，求最值，将原结论转化为求最值问题．<br>（1）∵<img width="147" height="25" id="_x000062f3815a-5989-4fbd-a16f-b9e097516179_i1265" src="/uploads/word_import/images/666/1389602488UHyOOg0d7lAbbpsWzboI.gif"><br>∴<img width="149" height="45" id="_x000062f3815a-5989-4fbd-a16f-b9e097516179_i1266" src="/uploads/word_import/images/666/1389602488KcJ36Yn5mdoxodWpCXSK.gif">；<img width="160" height="45" id="_x000062f3815a-5989-4fbd-a16f-b9e097516179_i1267" src="/uploads/word_import/images/666/1389602488YuYAgldEXPVCTPYmeC19.gif"><br>猜想：<img width="36" height="21" id="_x000062f3815a-5989-4fbd-a16f-b9e097516179_i1268" src="/uploads/word_import/images/666/1389602488iaHg818dIpifin7dNzgI.gif">的图象关于<img width="37" height="19" id="_x000062f3815a-5989-4fbd-a16f-b9e097516179_i1269" src="/uploads/word_import/images/666/1389602488fskujC9R2Icg7HOc7LXD.gif">对称，下面证明猜想的正确性；<br>∵<img width="392" height="27" id="_x000062f3815a-5989-4fbd-a16f-b9e097516179_i1270" src="/uploads/word_import/images/666/1389602488jkwU7HjAG7RSfMKxNlCd.gif"><br>∴<img width="36" height="21" id="_x000062f3815a-5989-4fbd-a16f-b9e097516179_i1271" src="/uploads/word_import/images/666/1389602488iaHg818dIpifin7dNzgI.gif">的图象关于<img width="37" height="19" id="_x000062f3815a-5989-4fbd-a16f-b9e097516179_i1272" src="/uploads/word_import/images/666/1389602488fskujC9R2Icg7HOc7LXD.gif">对称<br>（2）∵<img width="147" height="25" id="_x000062f3815a-5989-4fbd-a16f-b9e097516179_i1273" src="/uploads/word_import/images/666/1389602488UHyOOg0d7lAbbpsWzboI.gif">的定义域为<img width="32" height="21" id="_x000062f3815a-5989-4fbd-a16f-b9e097516179_i1274" src="/uploads/word_import/images/666/1389602488BG5HcgakNKL8U0PTZ7SS.gif">，由（1）知<img width="36" height="21" id="_x000062f3815a-5989-4fbd-a16f-b9e097516179_i1275" src="/uploads/word_import/images/666/1389602488iaHg818dIpifin7dNzgI.gif">的图象关于<img width="37" height="19" id="_x000062f3815a-5989-4fbd-a16f-b9e097516179_i1276" src="/uploads/word_import/images/666/1389602488fskujC9R2Icg7HOc7LXD.gif">对称<br>设<img width="92" height="24" id="_x000062f3815a-5989-4fbd-a16f-b9e097516179_i1277" src="/uploads/word_import/images/666/1389602488RIyJ68MESwo4EqAUdu2G.gif"><br>∴<img width="331" height="28" id="_x000062f3815a-5989-4fbd-a16f-b9e097516179_i1278" src="/uploads/word_import/images/666/1389602488hkQZXhBpt7Nq29ncGK0M.gif"><br><img width="247" height="48" id="_x000062f3815a-5989-4fbd-a16f-b9e097516179_i1279" src="/uploads/word_import/images/666/138960248803uCtfHF5mRALG2c8ZYc.gif"><br><img width="308" height="48" id="_x000062f3815a-5989-4fbd-a16f-b9e097516179_i1280" src="/uploads/word_import/images/666/1389602488m8GEgnFvSE6P78OIvoLF.gif"><br>∵<img width="45" height="24" id="_x000062f3815a-5989-4fbd-a16f-b9e097516179_i1281" src="/uploads/word_import/images/666/1389602488geW6kCYWsfHR1F1DCobr.gif"><sub>&nbsp;&nbsp; </sub>∴<img width="69" height="24" id="_x000062f3815a-5989-4fbd-a16f-b9e097516179_i1282" src="/uploads/word_import/images/666/1389602488h9DYFe7OnoRBWq3rOfRk.gif"><br>又<img width="257" height="48" id="_x000062f3815a-5989-4fbd-a16f-b9e097516179_i1283" src="/uploads/word_import/images/666/1389602488nWBTUeNCC6YhvJ8bRNnj.gif"><br>∴<img width="92" height="24" id="_x000062f3815a-5989-4fbd-a16f-b9e097516179_i1284" src="/uploads/word_import/images/666/1389602488EAX7EsJIzEs0rlDb3pds.gif">&nbsp;<br>∴<img width="36" height="21" id="_x000062f3815a-5989-4fbd-a16f-b9e097516179_i1285" src="/uploads/word_import/images/666/1389602488iaHg818dIpifin7dNzgI.gif">为<img width="33" height="21" id="_x000062f3815a-5989-4fbd-a16f-b9e097516179_i1286" src="/uploads/word_import/images/666/1389602488YlGRgy7lBoZsPVfVar6l.gif">上的增函数，由对称性知<img width="36" height="21" id="_x000062f3815a-5989-4fbd-a16f-b9e097516179_i1287" src="/uploads/word_import/images/666/1389602488iaHg818dIpifin7dNzgI.gif">在<img width="35" height="21" id="_x000062f3815a-5989-4fbd-a16f-b9e097516179_i1288" src="/uploads/word_import/images/666/1389602488T3ZrsFiBlhapBUuJpar2.gif">上为减函数，<br>∴<img width="105" height="21" id="_x000062f3815a-5989-4fbd-a16f-b9e097516179_i1289" src="/uploads/word_import/images/666/1389602488fTTM3pwVhxHamhYYogfM.gif"><br>∴<img width="61" height="21" id="_x000062f3815a-5989-4fbd-a16f-b9e097516179_i1290" src="/uploads/word_import/images/666/1389602488BnHJtzmCBOtWYkUqH8dO.gif">的图象除点<img width="37" height="21" id="_x000062f3815a-5989-4fbd-a16f-b9e097516179_i1291" src="/uploads/word_import/images/666/1389602488CG2UyZ7Qgu0ru4c85xal.gif">外均在直线<img width="39" height="21" id="_x000062f3815a-5989-4fbd-a16f-b9e097516179_i1292" src="/uploads/word_import/images/666/1389602488aN7UQtfaUmNJKhIKMIcK.gif">的下方．<br></div></li>
# """
#
# answer_soup = BeautifulSoup(answer_li, 'lxml')  # 从中选出font标签的后一个标签，
# answer_label = answer_soup.find('font').find_next_sibling()  # div或者b或者None
# print answer_label
#
# if answer_label is None:
#     answer_label_str = str(answer_label)
#     if answer_label_str[0:3] == '<b ':  # 说明为b标签
#         print 'b'
#         # answer = Selector(text=answer_label_str).xpath('//b/text()').extract()[0]
#         answer = answer_label.find('b').text
#     elif answer_label_str[0:3] == '<di':
#         # TODO:把里面的图片取出来
#         print 'div'
#         answer_img = []  # answer_img 初始为空，里面保存的是每个图片的字典
#         answer_img.append({'url': answer_label.find('img')['src']})
#         first_img = answer_label.find('img')['src'] = '0'
#         n = 1
#         for i in answer_label.img.find_next_siblings('img'):
#             img_dict_temp = {}
#             img_url = i['src']
#             if img_url[0:3] != 'www':
#                 img_url = 'www.yitiku.cn%s' % img_url
#             img_dict_temp['url'] = img_url
#             answer_img.append(img_dict_temp)
#
#             i['src'] = str(n)
#             n += 1
#             print i['src']
#     else:  # 另作处理
#         answer = '1'
# else:
#     answer = ''
# print answer_img
# print answer_label
