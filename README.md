# StockTracker

## How To Use
Download these files in a folder and cd into that folder then 'python3 Bot3.py' to run. 
### The StockData.txt file is where the desired stocks, prices, and the time interval is set.
- words and numbers between '<>' are things that this script will see, the rest of the words
in the file get ignored. 
- You may add more rows to the company data and you can change the
time in between checking the prices (default <30> minutes), but do not change the <Interval> item and do not
change the order in which each '<>' appears. Also, do not set the timer to lower than about <5> minutes 
because the email you use to send messages may become suspicious and lock this script out. 
- You may add more companies in the form 
<newCompanyName><lowNumber:highNumber> and this app will add them to the tracking list.
- **you may add companies while the app is running**, it will still work because each time the
app checks for stocks it re reads the text file with updated information. This app is designed
to be a run it and forget it application that only texts you when something of interest happens.
### logging in
- This app requires use of an email account in order to text your phone via email and your service
provider. **DO NOT USE YOUR REGULAR EMAIL**, for Gmail this app requires that the less secure login
options be enabled and it is a bad idea to decrease the security of an email which has sensitive information
- create a new gmail account and disable [this](https://myaccount.google.com/u/0/lesssecureapps?pli=1&pageId=none) setting
so that the script can use this account to email you. if the account becomes locked you will need to log back in with
your browser and restart the app. Do not use a login with a username or password that you use anywhere else, there is no
reason to expose a password that has actual value to this script or to the less secure settings gmail.
- The script will ask for an email username "example@gmail.com", password, phone number ex:"1112223333" and a carrier.
The script needs to know the cell service provider in order to send a text via email by sending it to the carrier's email
first. 
- once logged in the app should run and output what it is doing in the command prompt or terminal and any time the 
requirements are met, it will output the line "text me". if you do not recieve a text within the next couple minutes, something has gone wrong
