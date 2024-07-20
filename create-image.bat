@echo off

chcp 65001 > nul

@echo "удаление образа..."

docker rmi studposts-back:1.0

@echo "создание образа..."

docker build . -t studposts-back:1.0

@echo "успешно"

pause