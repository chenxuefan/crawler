git init
git remote rm origin
git remote add origin https://github.com/chenxuefan/crawler.git
git add .
git commit -m "update"
git pull origin master
git push -u origin +master