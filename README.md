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



