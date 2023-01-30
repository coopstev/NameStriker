Welcome to the Name Striker!

Name Striker is a Discord bot that Kicks, Bans, and DMs guild members if their display name is not of the form of a real name
(first and last names required, middle names optional). The logic is as follows:

If a user's display name (server nickname if they have one, username otherwise) is not of the required form:

	If they have no previous strikes, they are Kicked from the server and sent a direct message.
	The direct message tells them that they have received their one and only strike (citing the naming policy as the reason) and can rejoin the server.
	The strike info is stored both locally in striked.txt and sent into a text channel called #strikes.

	If they already have one strike, they are Banned from the server and sent a direct message.
	The direct message tells them that they have recevied their second strike (citing the naming policy as the reason) and have been Banned.
	The strike info and Banned status is sent into a text channel called #strikes.
	Locally, the user's info is removed from striked.txt and moved into banned.txt.

If a user receives a strike or is Banned for some other reason besides the naming policy,
you can add this info to striked.txt or banned.txt, respectively, manually by adding their UserID to the list.

To run the Name Striker, clone this repository, open the cloned folder NameStriker in command line, and run the command python Striker.py
Once "Done processing strikes." is printed, press Ctrl + C to close the bot.
To add the bot to your server, follow the step-by-step tutorial here: https://www.youtube.com/watch?v=fU-kWx-OYvE

Copyright 2023 Cooper Stevens