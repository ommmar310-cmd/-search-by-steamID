SteamID-search 
-----------------------
this project created to make search games in multiple steam accounts easier 

You can search games in an account (must be public) by the steamID or profile name

-----------------------
1-you need to put data etiher profile name ( Lable) or steamID(steam_identifier) in ACCOUNTS_DB inside update.py (you dont need to put passwords or manual games its just for you to make it easier) 

2-get an steam api key using https://steamcommunity.com/dev/apikey and put it in API_KEY

3-run it to fetch the data

----------------------

now you can use search.py to search a game inside the accounts just run it then and enter the game name

----------------------
dependices
----------------------
requests 
---bash
pip install requests
---
Arch
---bash
sudo pacman -S python-requests
---
------------------------
