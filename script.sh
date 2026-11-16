#! /bin/bash

source /path/venv/bin/activate

python3 /path/agent/test.py

text=$(cat /home/home-lab/test/agent/news.txt)
curl -X POST "https://api.telegram.org/botTOKEN"  -H "Content-Type: application/json"  -d "{\"chat_id\": YOUR_ID, \"text\": \"$text\"}"

deactivate
