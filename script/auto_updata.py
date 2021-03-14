#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import sys,os
import time
import logging

logging.basicConfig(level=logging.DEBUG,
                    filename='logs/py-error.log',
                    datefmt='%Y/%m/%d %H:%M:%S',
                    format='%(asctime)s - %(name)s - %(levelname)s - %(lineno)d - %(module)s - %(message)s')
logger = logging.getLogger(__name__)

# 脚本路径
srcipt_path=sys.path[0]
hugo_path=os.getcwd()
print(srcipt_path)
print(hugo_path)
# 测试
# sh_1 = 'touch ' + srcipt_path + '/test.py'
# os.system(sh_1)

# dev环境版本每10分钟上传一次，并版本自增

sh_git = "git add ./"
sh_push = "git push origin --tags"

for i in range(1,10):
    sh_version="v0.1." + str(i)
    fortune_time = time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime())
    # 上传代码格式化"git tag -a V0.1.0 -m 'release 0.2.0'" 
    sh_commit = f"git tag -a {sh_version} -m 'release {sh_version.split('v')[1]}'"
    # print(sh_commit)
    # print(fortune_time)
    sh_create_md = f"hugo new posts/{fortune_time}.md"
    sh_fortune = f"echo `fortune` >> {hugo_path}/content/posts/{fortune_time}.md"
    os.system(sh_create_md)
    os.system(sh_fortune)
    # 等待1秒
    time.sleep(1)
    os.chdir(hugo_path)
    os.system("pwd")
    os.system(sh_git)
    os.system(sh_commit)
    try:
        os.system(sh_push)
    except Exception as e:
        logger.error('可能是连不上github,请查看一下联通github的网络')
        logger.error(e)        
    time.sleep(360)
print('自动上传代码任务已执行完毕！')