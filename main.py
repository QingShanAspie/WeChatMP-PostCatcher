# coding=utf-8
import json
import os
import random

from datetime import datetime, timedelta


# 保存文件
def SaveFile(fpath, fileContent):
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(fileContent)


# 读取文件
def ReadFile(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        all_the_text = f.read()
    return all_the_text


# 时间戳转日期
def Timestamp2Datetime(stampstr):
    dt = datetime.utcfromtimestamp(stampstr)
    dt = dt + timedelta(hours=8)
    newtimestr = dt.strftime("%Y-%m-%d-%Y%m%d")
    return newtimestr


# TAG随机
def TagRandom():
    TagLen = len(TAG) - 1
    res = ''
    item = random.randint(1, 5)
    if item == 1:
        res = TAG[random.randint(0, TagLen)]
    elif item == 2:
        for i in random.sample(range(0, TagLen), 2):
            res += TAG[i] + ", "
    elif item == 3:
        for i in random.sample(range(0, TagLen), 3):
            res += TAG[i] + ", "
    elif item == 4:
        for i in random.sample(range(0, TagLen), 4):
            res += TAG[i] + ", "
    elif item == 5:
        for i in random.sample(range(0, TagLen), 5):
            res += TAG[i] + ", "
    return str(res)[0: int(len(res) - 2)]


class Article:
    def __init__(self, url, pubdate, idx, title, digest):
        self.url = url
        self.pubdate = pubdate
        self.idx = idx
        self.title = title
        self.digest = digest


# 从fiddler保存的json文件中提取文章url等信息
def GetArticleList(jsondir):
    filelist = os.listdir(jsondir)
    ArtList = []
    for file in filelist:
        filepath = os.path.join(jsondir, file)
        filetxt = ReadFile(filepath)
        jsbody = json.loads(filetxt)
        general_msg_list = jsbody["general_msg_list"]
        jsbd2 = json.loads(general_msg_list)
        lists = jsbd2["list"]
        # 一个item里可能有多篇文章
        # 请注意这里的编号只是为了保存html方便，并不对应于真实的文章发文位置(比如头条、次条、3条)
        for item in lists:
            artidx = 1
            comm_msg_info = item["comm_msg_info"]
            pubstamp = comm_msg_info["datetime"]
            pubdate = Timestamp2Datetime(pubstamp)
            # 49为普通图文类型，还有其他类型，暂不考虑
            if comm_msg_info["type"] == 49:
                app_msg_ext_info = item["app_msg_ext_info"]
                url = app_msg_ext_info["content_url"]
                idx = artidx
                title = app_msg_ext_info["title"]
                digest = app_msg_ext_info["digest"]
                arts = Article(url, pubdate, idx, title, digest)
                ArtList.append(arts)
                # 一次发多篇
                if app_msg_ext_info["is_multi"] == 1:
                    artidx += 1
                    multi_app_msg_item_list = app_msg_ext_info["multi_app_msg_item_list"]
                    for subArt in multi_app_msg_item_list:
                        url = subArt["content_url"]
                        idx = artidx
                        title = subArt["title"]
                        digest = app_msg_ext_info["digest"]
                        arts = Article(url, pubdate, idx, title, digest)
                        ArtList.append(arts)
    return ArtList


if __name__ == "__main__":
    # 定义颜色
    COLOR = ["success", "warning", "info", "danger", "secondary"]

    # 定义TAG
    TAG = ["ASD", "Austim", "孤独症", "Aspie", "自闭症", "孤独症谱系", "AS", "介绍"]

    print(TagRandom())
    #
    # # 解析JSON
    # ret = GetArticleList('json')
    # ret.sort(key=lambda x: x.pubdate, reverse=True)
    #
    # # 判断文件夹，不存在便创建
    # if not os.path.exists('post'):
    #     os.makedirs('post')
    #     pass
    #
    # for art in ret:
    #     if art.title != "分享图片":
    #         if art.digest == "分享一篇文章。":
    #             art.digest = art.title
    #         Post1 = "---"
    #         Post2 = "\ntitle: " + art.title
    #         Post3 = "\ntags: "
    #         Post4 = "\ncolor: " + COLOR[random.randint(0, len(COLOR) - 1)]
    #         Post5 = "\ndescription: " + art.digest
    #         Post6 = "\nexternal_url: " + art.url
    #         Post7 = "\n---"
    #         mdfile = Post1 + Post2 + Post3 + Post4 + Post5 + Post6 + Post7
    #         SaveFile("post/" + art.pubdate + ".md", mdfile)
    #         print("Export: " + art.title + " Done!")
    #         pass
