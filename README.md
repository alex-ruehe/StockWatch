# StockWatch

Simple script that pulls stock information using [ystockquote](https://github.com/cgoldberg/ystockquote) and sends some information about your stocks via mail. Preferred
way to use the script is to run it on saturdays using cronjob or similar services to get an overview over the last 5 days via mail.
Mail is sent via sendmail, so make sure you have sendmail on your system

1. rename config.default.cfg to config.cfg and fill in your data (currently no database support - only file)
2. rename stocks.default.json to filename from config.cfg (default is stocks.json) 
3. add your stocks to the stocks file following the pattern in the file
4. run main.py to get mail with stock information