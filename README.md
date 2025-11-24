# RedDiscordBotPtero
This script allows you to run Reds-Discord bot on Pterodactyl instances without the need to change main startup flags or use bash/shell commands.

1. Download both .py files to the root directory of your instance.
2. Go to the startup tab of your panel, and make sure to set the language to python, and the startup file to install.py
3. Start the server. Follow the prompts to do the part 1 install. Note: When it asks for directory, copy the default directory given and paste into the console and hit enter, typing y to confirm and hit enter. This is because you can't confirm with just an enter command.
4. Once complete, go to the startup tab again and change the startup command to start.py
5. Make sure to edit the start.py file and change the CHANGEME text to the name of the bot you set in the steps above. It is CASE SENSITIVE.
6. Start the bot through the console/start button. It will ask you to input a discord bot token, hit enter when done.
7. Set a prefix as asked
8. Confirm any options it gives, and the bot will automatically start.

On subsequent starts, running the start.py script will start the bot by itself.