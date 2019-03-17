# IRCCloud SASL Username is not Nickname Workaround

https://twitter.com/IRCCloud/status/1103641420647272448

This is an easy to deploy Heroku App that helps IRCCloud users who have to authenticate to servers where the SASL 
username and password is used for authentication and there is no server password alternative. Unfortunately, IRCCloud
assumes that SASL == Nickname as SASL in their view is used as an alternative to NickServ authentication.
This is not always true. There is a workaround, but it is manual:

* Use the SASL username in the Nickname field
* Change the nickname after successful authentication and connection.

It's not a complete workaround though. If the connection is dropped for whatever reason, it will not reconnect 
correctly, as the nickname is updated to the user's desired nickname and not the SASL username. To reconnect, the 
user must set the nickname back to the SASL username, reconnect, and change the nickname. This is terribly manual.

**Pain in the ass!! And you lose chat during this downtime which is not cool in a bouncer.**

This easy to deploy Heroku app automates this check and dance and is free to host and run. It's not perfect, but it's 
better than nothing.
 
## Usage and Deployment

1. Have ready:    
    * IRCCloud Email
    * IRCCloud Pass
    * Name you've given of the IRC Network in IRCCloud. Eg. FreeNet, Secret Server, OFTC, etc.
    * SASL Username for Server Authentication.
    * Desired Nickname to switch to after SASL authentication
    * A Heroku Account
2. Be sure the network has the correct "NickServ password". This is the password for SASL.
3. Deploy to Heroku
    * Press this button to deploy this application to Heroku. 
    The way this tool is deployed and run fits in well under the free quotas on the free plan. 
        * [![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)
    * Set the corresponding variable names in the deploy and *Deploy* away.
4. After the deployment is done, press the *Manage* button at the bottom to manage the app.
5. Click on "Heroku Scheduler" in the "Installed add-ons" portion on the *Overview* Page. 
6. Add a job to Heroku Scheduler to run `python run.py` every hour.
 
***Confused**? Please make a GitHub issue and let us work out what's deficient in the documentation.*
   
## Upgrade

Delete the App and redo the above. 