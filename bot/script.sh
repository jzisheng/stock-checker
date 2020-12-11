docker run --name cd -d -p 4444:4444 selenium/standalone-chrome
sleep 5
python3 bot.py
sleep 5
docker container kill cd
sleep 5
docker container prune --force
