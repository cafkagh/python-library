# -*- coding: utf-8 -*-
import time
from Pdo import Pdo as pdo
from datetime import datetime


class Wordpress:
    # 初始化
    def __init__(self, db_source='', host='127.0.0.1', port=3306, user='root', password='root', database='',
                 charset="utf8"):
        if db_source != '':
            self.pdo = db_source
        else:
            self.pdo = pdo(host=host, port=port, user=user, password=password, database=database, charset="utf8")
        self.now = datetime.now().__format__('%Y-%m-%d %H:%M:%S')
        self.gmt = datetime.utcnow().__format__('%Y-%m-%d %H:%M:%S')

    def new_posts(self, post_title='', post_content='', cat_id=0, post_author='', post_excerpt='',
                  post_status='publish', post_type='post', ping_status='open', comment_status='open', post_password='',
                  post_name='', to_ping='', pinged='', post_content_filtered='', post_parent=0, guid='', menu_order=0,
                  post_mime_type=''):
        post = dict()
        relation = dict()

        post["post_title"] = post_title  # 标题
        post["post_content"] = post_content  # 正文
        post["post_author"] = post_author  # 对应作者ID
        post["post_excerpt"] = post_excerpt  # 摘录
        post["post_status"] = post_status  # 文章状态（publish/auto-draft/inherit等）
        post["post_type"] = post_type  # 文章类型（post/page等）

        post["post_date"] = self.now  # 发布时间
        post["post_modified"] = self.now  # 修改时间
        post["post_date_gmt"] = self.gmt  # 发布时间（GMT+0时间）
        post["post_modified_gmt"] = self.gmt  # 修改时间（GMT+0时间）

        post["ping_status"] = ping_status  # PING状态（open/closed）
        post["comment_status"] = comment_status  # 评论状态（open/closed）
        post["post_password"] = post_password  # 文章密码
        post["post_name"] = post_name  # 文章缩略名
        post["to_ping"] = to_ping  # 所有需要Ping的网址
        post["pinged"] = pinged  # 已经PING过的链接
        post["post_content_filtered"] = post_content_filtered  # 文章内容过滤
        post["post_parent"] = post_parent  # 父文章，主要用于PAGE
        post["guid"] = guid  # 每篇文章的一个地址
        post["menu_order"] = menu_order  # 排序ID
        post["post_mime_type"] = post_mime_type  # MIME类型
        post["comment_count"] = "0"  # 评论总数

        last_id = self.pdo.insert_db("wp_posts", [post])
        # print last_id
        if post_name == '':
            self.pdo.save("wp_posts", "id = " + str(last_id), {'post_name': last_id})

        if cat_id != 0:
            relation["term_taxonomy_id"] = cat_id  # 分类目录id
            relation["term_order"] = "0"  # 排序
            relation["object_id"] = str(last_id)  # 对应文章ID/链接ID
            self.pdo.insert_db("wp_term_relationships", [relation])
        return last_id

    def post_meta(self, post_id='', meta_key='', meta_value=''):
        last_id = self.pdo.insert_db("wp_postmeta", [{"post_id": post_id, "meta_key": meta_key, "meta_value": meta_value}])
        return last_id

    def attachment(self, filename='', post_author='', post_mime_type='', guid=''):
        post_id = self.new_posts(post_title=filename, post_name=filename, post_author=post_author,
                                 post_status='inherit', ping_status='closed', guid=guid, post_type='attachment',
                                 post_mime_type=post_mime_type)
        return post_id


if __name__ == "__main__":
    wp = Wordpress(host='127.0.0.1', user='root', password='root', database='keye')
    print(wp.now)
    print(wp.gmt)
