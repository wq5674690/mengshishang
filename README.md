### 项目说明

```
1、通过雨果静态文件生成器，进行生成静态文件；
2、通过git上传代码到github上，并创建二个分支，dev和master分支；分支版本要求，0.1.0开始，0.2.0结束；dev分支，每10分钟进行上传更新一次；main每1小时更新一次；
3、通过nginx进行分发，设置staging环境和dev环境；
4、通过ansible进行代码编译；
```

### 工具介绍

```
1、Hugo static site generator(静态页面生成器)
2、mac电脑
3、fortune(随机生产文章)
4、git(代码管理)、github
5、ansible(自动化维护工具)
6、nginx
```

### 要求

```
1、通过ansible playbook来配置服务器的基础环境
2、通过nginx设置二个环境，dev和staging
3、dev环境，代码通过git每10分钟更新一次，git分支为dev
4、staging环境，代码通过git每小时更新一次,git分支为main
5、编写相关脚本时，添加注释
```

### 基础环境安装

```shell
# 安装hugo
brew install hugo
cd ~
hugo new site mss
cd mss
git init
git submodule add https://github.com/budparr/gohugo-theme-ananke.git themes/ananke
echo theme = \"ananke\" >> config.toml
# 安装fortune
brew install fortune
# 安装nginx
brew install nginx
# 安装ansible
brew install ansible
touch /etc/ansible/ansible.cfg
touch /etc/ansible/hosts
mkdir -p /etc/ansible/roles
# 在ansbile主机列表中添加机器
echo '[staging]' >> /etc/ansible/hosts
echo '10.0.0.1 ansible_ssh_user=root ansible_ssh_port=22' >> /etc/ansible/hosts
echo '[defaults]' >> /etc/ansible/ansible.cfg
# SSH秘钥认证
ssh-keygen -t rsa
ssh-copy-id root@agent_host_ip
# 解决ansible执行过程中部分报错
echo 'interpreter_python = auto_legacy_silent' >> /etc/ansible/ansible.cfg
# 安装git
brew install git
# 本地hosts
sudo echo '127.0.0.1 mss6.cn' >> /etc/hosts
```

### hugo文章更新，模拟版本迭代

- 执行`sh $script_path/write_fortune.sh`
- 脚本存放到：`$hugo_home/script`
- 编译后的静态文件存放在：`$hugo_home/public`
- 脚本如下：

```shell
#!/bin/bash
# 进入脚本路径
cd $(dirname $0);
# 给路径变量赋值
script_path=`pwd`;
write_time=`date '+%Y-%m-%d_%T'`;
echo $write_time;
echo $script_path;
cd ..;
# 生成论坛文章页
hugo new posts/$write_time.md;
# 通过fortune生成文章内容并写入文件
echo `fortune` >> content/posts/$write_time.md;
# 启动预览hugo
# hugo server -D
# 编译生成public
hugo -D
```

### 手动上传代码脚本

- dev环境脚本$script_path/dev_git.sh
- 脚本存放到：$hugo_home/script

```shell
#!/bin/bash
# 进入脚本路径
cd $(dirname $0);
# 给路径变量赋值
script_path=`pwd`;
cd ..
git add .
# 每次版本号递增
git commit -m '0.1.1'；
git push -u origin dev；
# 或者
git tag -a V0.1.1 'release 0.1.1'；
git push origin --tags；
```

- staging环境脚本$script_path/staging_git.sh
- 脚本存放到：$hugo_home/script

```shell
#!/bin/bash
# 进入脚本路径
cd $(dirname $0);
# 给路径变量赋值
script_path=`pwd`;
cd ..
git add .
# 每次版本号递增
git commit -m '0.2.0'；
git push -u origin main；
# 或者
git tag -a V0.2.0 'release 0.2.0'；
git push origin --tags；
```

### git版本自动上传

- 更新的文件有：config.toml、public
- 注意生成dev环境的页面时，修改config.toml，域名指向：`baseURL = "http://dev.mss6.cn:8082/"`,生成staging环境页面时，域名指向：`baseURL = "http://mss6.cn:8081/"`
- 生成静态文件`hugo -D`

```shell
# 更新环境代码前，请确认是哪个环境的配置
# staging
sed -i 's/example.org/mss6.cn:8081/g' ~/mss/config.toml
# dev
sed -i 's/example.org/dev.mss6.cn:8082/g' ~/mss/config.toml
```

自动上传代码脚本（dev环境）如下：

```python
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

# dev环境版本每10分钟上传一次，并版本自增
sh_git = "git add ./"
# sh_push = "git push -u origin dev"
sh_push = "git push origin --tags"

for i in range(1,10):
    sh_version="v0.1." + str(i)
    fortune_time = time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime())
    # 上传代码格式化"git tag -a V0.1.0 -m 'release 0.2.0'" 
    # sh_commit = f"git commit -m 'release {sh_version.split('v')[1]}'"
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
```

staging环境的代码，只需修改以上脚本中，代码改为master，sleep时间修改为3600

### ansible bookplay更新项目

- Ansible-playbook文件 `$hugo_home/script/ansible_script/dev-update.yaml`
- Update dev

```yaml
- hosts : test  
  connection: local                                      
 # remote_user : root                           #通过root用户执行
  tasks :
  - name : pull                            
    shell : cd ~/mss; git clone -b dev https://github.com/wq5674690/mengshishang.git
  - name : copy hugo static dev
    copy: 
      src:  ~/mss/public
      dest:  /usr/local/var/www/dev
```

- Ansible-playbook文件 `$hugo_home/script/ansible_script/pro-update.yaml`
- update staging

```yaml
- hosts : test  
  connection: local                                      
 # remote_user : root                           #通过root用户执行
  tasks :
  - name : pull                            
    shell : cd ~/mss; git clone -b main https://github.com/wq5674690/mengshishang.git
  - name : copy hugo static staging
    copy: 
      src:  ~/mss/public
      dest:  /usr/local/var/www/staging
```



### nginx配置

- 本机hosts`127.0.0.1 mss6.cn`
- 以下配置保存到`/usr/local/etc/nginx/servers/hugo.conf`中，并`nginx -s reload`

```nginx
server {
    listen 8082;
    server_name dev.mss6.cn;

    location / {
        access_log  ~/Downloads/nginx/logs/hugo-dev.log;
        root /usr/local/var/www/dev/public;
        try_files $uri $uri/ /index.html last;
        index index.html;

        error_page 404 /404.html;
            location = /40x.html {
        }
 
        error_page 500 502 503 504 /50x.html;
            location = /50x.html {
        }
    }
}

server {
    listen 8081;
    server_name mss6.cn;

    location / {
        access_log  ~/Downloads/nginx/logs/hugo-staging.log;
        root /usr/local/var/www/staging/public;
        try_files $uri $uri/ /index.html last;
        index index.html;

        error_page 404 /404.html;
            location = /40x.html {
        }
 
        error_page 500 502 503 504 /50x.html;
            location = /50x.html {
        }

    }
}
```



