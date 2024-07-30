# LoginTracker
A work-in-progress Python/Google Sheets sign-in/sign-out system

Keep in mind: this is VERY work-in-progress. Expect stuff to be broken.

For a quick (but relatively controversial) way of installing everything but the service_account.json file, use `curl -sSL https://github.com/TaigaM123/LoginTracker/install.sh | bash` on a Debian/Ubuntu-based system.

---
Hardware:
* Raspberry Pi (can theoretically be done on any Debian/Ubuntu computer, I think? Only tested on a Raspberry Pi though)
* SD Card running Raspberry Pi OS (64-bit)
* USB Camera (tested with a Microsoft Lifecam HD-3000)
* USB flash drive named "LoginLogger" (no quotes, you can change the name it's looking for in main.py)
* Internet connection

To set up a service_account.json, see [here](https://docs.gspread.org/en/latest/oauth2.html#for-bots-using-service-account). Note the `service_account.json` should be moved to the LoginTracker folder, not `~/.config/gspread/service_account.json`.

A template for the Google Sheet is [here](https://docs.google.com/spreadsheets/d/1hAG3BInsXe4kDI7Lr8NNKz52V_XTZJkCf4aOdqBTRyw/edit?gid=1135907022#gid=1135907022). 

---
Thanks @cj-plusplus!
Small portions of the Python were done by ChatGPT. I'm not sure how much time or effort it saved me though.
