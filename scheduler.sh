#!/bin/bash

echo "started cronupdate"
crontab -l > cronupdate
echo "*/5 * * * * /home/ubuntu/miniconda3/envs/comp30830/bin/bikeScrape >> cronlog_bike"  >> cronupdate
echo "*/5 * * * * /home/ubuntu/miniconda3/envs/comp30830/bin/weatherScrape >> cronlog_weather" >> cronupdate
crontab cronupdate
rm cronupdate
echo "finished cronupdate"
