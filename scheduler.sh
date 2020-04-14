#!/bin/bash

echo "started cronupdate"
crontab -l > cronupdate
echo "*/5 * * * * /home/ubuntu/anaconda3/envs/comp30830py37/bin/bikeScrape >> cronlog_bike"  >> cronupdate
echo "*/5 * * * * /home/ubuntu/anaconda3/envs/comp30830py37/bin/weatherScrape >> cronlog_weather" >> cronupdate
crontab cronupdate
rm cronupdate
echo "finished cronupdate"
