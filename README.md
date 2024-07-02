![float, the dice, laying on a desk with battlemaps and folder](./.github/banner.png)

# float

a simple dice roller bot made for me and my friends. hosted under MIT license.

mostly on maintenance because there's not much stuff you can put in a diceroller bot.

## how do i host this

you are able to use a systemd service such as
```
[Unit]
Description=a dicerolling discord bot
After=network.target

[Service]
ExecStart=/PATH/TO/float/venv/bin/python3 main.py
WorkingDirectory=/PATH/TO/float/
StandardOutput=inherit
StandardError=inherit
Restart=always
User=BOT_RUNNER_USER_REPLACE_ME

[Install]
WantedBy=multi-user.target
```

after setting up git and venv.
