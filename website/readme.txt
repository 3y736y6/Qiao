gitee ，github，gitlab创建远程仓库
对应编程语言对应.gitignore
上传人信息
git config --global user.name "xx"
git config --global user.email "xxxx"

进入项目目录，把该项目初始化作为本地仓库 
git init

把远程仓库地址对应"origin"：
git remote add origin https://远程仓库地址


上述初始化完成后进行日常提交
git add .
git commit -m "xxx"
git push origin master
弹窗填写远程仓库gitee密码

远程下载全部代码：
创建一个文件夹，并进入
git clone https://远程仓库地址

远程更新代码：
git pull origin master


在www文件夹中找到py的env
安装flask
.../python3.11 -m pip install flask
查看端口指令
netstat -ano

pip list --format=freeze > requirements.txt
导出当前环境依赖

