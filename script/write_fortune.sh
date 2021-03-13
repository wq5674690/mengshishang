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