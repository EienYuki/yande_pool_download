# -*- coding: utf-8 -*-
import os
import io
import time
from pyquery import PyQuery as pq
from urllib import urlretrieve

input_ID = ""
input_img_mode = ""
Folder_mame = ""

img_html_ulis = {}
Fail_ulis = {}
Fail_img_sava_paths = {}
Fail_img_ulis = {}

# 決定下載的圖片集合
print "https://yande.re/pool/show/XXXX"
print "ID = XXXX"
input_ID = str(raw_input("input ID:"))
html = pq(url="https://yande.re/pool/show/" + input_ID)
# 決定下載的圖片集合

# 列出全部圖片網頁網址
count = 0
data = html('span.plid')
for tp in data:
    img_html_ulis[count] = str(html(tp).text()).split(' ')[-1]
    count += 1
# 列出全部圖片網頁網址

# 第一階段 (下載)
if len(img_html_ulis) > 0:
    # 決定下載的圖片資料夾
    try:
        Folder_mame = html('title').text().split('|')[0][:-1]
        if not os.path.exists(Folder_mame):
            os.mkdir(Folder_mame)
    except:
        Folder_mame = "yande.re id= " + input_ID
        if not os.path.exists(Folder_mame):
            os.mkdir(Folder_mame)
    # 決定下載的圖片資料夾

    # 決定下載圖片的格式
    html = pq(url=img_html_ulis[0])
    tp = ""
    if len(str(html('a#highres').attr('href'))) >4:
        tp += "jpg"
    if len(str(html('a#png').attr('href'))) >4:
        if tp == "":
            tp += "png"
        else:
            tp += " or png"
    tp = "auto or " + tp
    input_img_mode = str(raw_input("input image format (" + tp +"):"))
    if input_img_mode == "jpg":
        input_img_mode = 'a#highres'
    if input_img_mode == "png":
        input_img_mode = 'a#png'
    if input_img_mode == "" or input_img_mode == "auto":
        if tp == "auto or png" or tp == "auto or jpg or png":
            input_img_mode = 'a#png'
        if tp == "auto or jpg":
            input_img_mode = 'a#highres'
    # 決定下載圖片的格式

    # 初始化
    count = 1
    count_max = str(len(img_html_ulis))
    # 初始化

    # 下載圖片----------------------------------------------
    for tp in img_html_ulis:

        # 取得相關 網頁、網址
        html = pq(url=img_html_ulis[count-1])
        img_uli = html(input_img_mode).attr('href')
        # 取得相關 網頁、網址

        if len(img_uli) >0:
            print "(" + str(count) + "/" + count_max +") Start:" + img_html_ulis[count-1]

            # 依據圖片儲存格式
            filename = str(count) + u'.' + str(img_uli).split('.')[-1]
            # 依據圖片儲存格式

            # 下載
            try:
                urlretrieve(img_uli, Folder_mame + u'/' + filename)
                print "Complete:"+ img_html_ulis[count-1]
            except:
                Fail_ulis[count] = img_html_ulis[count-1]
                Fail_img_sava_paths[count] = Folder_mame + u'/' + filename
                Fail_img_ulis[count] = img_uli
                print "Fail:"+ img_html_ulis[count-1]
            # 下載
        else:
            print "Error:"+img_uli
            break
        count += 1
        time.sleep(1)
    # 下載圖片----------------------------------------------
else:
    print "Error: Can not find"

# 第二階段 (有錯誤可以重新下載)
if(len(Fail_ulis) >0):
    # 列印 log
    print ""
    print "Fail Uli List:"
    for _log in Fail_ulis:
        print "Fail:" + Fail_ulis[_log]
    # 列印 log

    redl = "y"
    while redl == "y":
        # 刪除舊log
        if os.path.exists(Folder_mame + "/" +"Fail.log"):
            os.remove(Folder_mame + "/" +"Fail.log")
        # 刪除舊log

        # 寫入新log
        sw = open(Folder_mame + "/" +"Fail.log",'w')
        for tp in Fail_ulis:
            sw.write(Fail_ulis[tp]+"\n")
            sw.write(Fail_img_sava_paths[tp]+"\n")
            sw.write(str(Fail_img_ulis[tp])+"\n")
        sw.close()
        # 寫入新log

        # 詢問是否重新下載
        redl = str(raw_input("Re- download (y/n)"))
        if redl == "n":
            break
        # 詢問是否重新下載

        # 初始化
        temp_Fail_ulis = {}
        temp_Fail_img_sava_paths = {}
        temp_Fail_img_ulis = {}
        count = 1
        count_max = str(len(Fail_ulis))
        os.system('cls')
        # 初始化

        # 下載圖片----------------------------------------------
        for re_i in Fail_ulis:
            print "(" + str(count) + "/" + count_max +") Start:"+Fail_ulis[re_i]
            try:
                urlretrieve(Fail_img_ulis[re_i], Fail_img_sava_paths[re_i])
                print "Complete:"+Fail_ulis[re_i]
            except:
                temp_Fail_ulis[count] = Fail_ulis[re_i]
                temp_Fail_img_sava_paths[count] = Fail_img_sava_paths[re_i]
                temp_Fail_img_ulis[count] = Fail_img_ulis[re_i]
                print "Fail:"+Fail_ulis[re_i]
            count += 1
            time.sleep(1)
        # 下載圖片----------------------------------------------

        # 檢查----------------------------------------------
        if len(temp_Fail_ulis) == 0:
            print ""
            print "Download All completed"
            break
        else:
            Fail_ulis = temp_Fail_ulis
            Fail_img_sava_paths = temp_Fail_img_sava_paths
            Fail_img_ulis = temp_Fail_img_ulis
            print ""
            print "Fail Uli List:"
            for _log in Fail_ulis:
                print "Fail:" + Fail_ulis[_log]
            redl = "y"
        # 檢查----------------------------------------------
else:
    if(len(html) > 1):
        print ""
        print "Download All completed"
os.system('pause')
