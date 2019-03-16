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

TODO: Put button here.
   
## Upgrade

Delete the App and redeploy. 