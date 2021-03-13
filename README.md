## 项目说明

```
1、通过雨果静态文件生成器，进行生成静态文件；
2、通过git上传代码到github上，并创建二个分支，dev和master分支；分支版本要求，0.1.0开始，0.2.0结束；dev分支，每5分钟进行上传更新一次，master上传一次最终版本；
3、通过nginx进行分发，设置staging环境和dev环境；
4、通过ansible进行代码编译；
```

### 开发要求

```
1、你的网站的基本模板，以显示在页脚的版本，并在登陆页上的帖子列表
2、将显示单个页面内容的帖子模板
```

### 工具介绍

```
1、Hugo static site generator(静态页面生成器)
2、Terraform( IT 基础架构自动化编排工具)
3、fortune(随机生产文章)
4、git(代码管理)、github
5、ansible(自动化维护工具)
6、nginx
```

### 要求

```
1、通过ansible playbook来配置服务器的基础环境
2、通过nginx设置二个环境，dev和staging
3、dev环境，代码通过git每10分钟更新一次
4、staging环境，代码通过git每小时更新一次
5、编写相关脚本时，添加注释
```

### 基础环境安装

```shell
# 安装hugo
brew install hugo
hugo new site quickstart
cd quickstart
git init
git submodule add https://github.com/budparr/gohugo-theme-ananke.git themes/ananke
echo theme = \"ananke\" >> config.toml
# 启动hugo
hugo server -D
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
```

### hugo文章更新，模拟版本迭代

- 执行`sh $script_path/write_fortune.sh`
- 脚本存放到：$hugo_home/script
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
```

### 上传代码脚本

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
git commit -m '0.1.1'
git push -u origin dev
# 或者
git tag -a V0.1.1 'release 0.1.1'
git push origin --tags
```

- staging环境脚本$script_path/staging_git.sh
- 脚本存放到：$hugo_home/script

```python
for i in range(0.1.0,0.2.0,0.0.1):
    print(i)
    
```



```shell
#!/bin/bash
# 进入脚本路径
cd $(dirname $0);
# 给路径变量赋值
script_path=`pwd`;
cd ..
git add .
# 每次版本号递增
git commit -m '0.2.0'
git push -u origin staging
# 或者
git tag -a V0.2.0 'release 0.2.0'
git push origin --tags
```

任务计划

```shell
crontab -e
# 设定dev环境更新时间
10 * * * * sh $script_path/write_fortune.sh
# 设定staging环境更新时间
* 1 * * * sh $script_path/write_fortune.sh

```



