# IRCCloud SASL Username is not Nickname Workaround

This is an easy to deploy Heroku App that helps users who have to authenticate to servers where the SASL username and
password is used for authentication and there is no server password option. *However, the user's nickname does not
match their SASL username.* There is a workaround, but it is manual:

* Use the SASL username in the Nickname field
* Change the nickname after successful authentication.

However, there's a big drawback. If the connection is dropped for whatever reason, it will not reconnect correctly, as
the nickname is updated to the user's desired nickname and not the SASL username. To reconnect, the user must set the
nickname back to the SASL username, reconnect, and change the nickname.

This east to deploy Heroku app automates that and solve the hosting conundrum.
 
## Usage and Deployment

1. Have ready:    
    * IRCCloud Email
    * IRCCloud Pass
    * Name you've given of the IRC Network in IRCCloud. Eg. FreeNet, Secret Server, OFTC, etc.
    * SASL Username for Server Authentication.
    * Desired Nickname
2. Be sure the network has the correct "NickServ password". This is the password for SASL.
3. Deploy to Heroku
    * Press this button to deploy this application to Heroku. You will need to create an account if you haven't.
    The way this tool is deployed fits in well under the free quotas on the free plan. 
        * [![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)
    * Set the corresponding variable names in the deploy and *Deploy*.
4. After the deployment is done, press the *Manage* button at the bottom.
5. Click on "Heroku Scheduler" in the "Installed add-ons" portion on the Overview Page. 
6. Add a job to Heroku Scheduler to run `python run.py` every hour.
 
***Confused**? Please make a GitHub issue and let us work out
what's deficient in the documentation.*
   
## Upgrade

Delete the App and redo the above. 