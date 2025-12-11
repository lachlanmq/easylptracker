# Easy LP Tracker by Xoffy

A very simple League of Legends Ranked LP tracker. Takes Riot account name and server then returns current rank, LP, win rate and games played within the CLI on a user-specified cooldown.

I couldn't find any extremely reliable local LP trackers so I made this in a day. Websites like U.GG, DPM.LOL and OP.GG are sometimes unreliable. This grabs your info from Riot's API directly.

I linked this to my own database so I could view and store further details of matches without cluttering the CLI.

You should use your own Riot API key and replace the one in the `RIOT_API_KEY` literal. You can get one [here](https://developer.riotgames.com/).

![Demo Photo](https://github.com/lachlanmq/easylptracker/blob/main/images/easy_lp_tracker1.png?raw=true)

# Dependencies

Requires Python and various packages to launch easy_lp_tracker.py within the terminal.

Packages required:
- Datetime
- Requests
- Supabase (optional if you use your own DB)

There is no pre-compiled version as of now.

Only been tested on Windows but should still work on Linux.

# Usage
Enter your full Riot account name and its region when prompted or you can also pass arguments.

### Examples:

`python ./easy_lp_tracker.py`

NOTE: Given arguments are case insensitive.

`python ./easy_lp_tracker.py Xoffy#kafka oc1`

`python ./easy_lp_tracker.py BALDREL#FRAUD EUW1`

The refresh cooldown can also be modified by changing the `REFRESH_COOLDOWN` literal to whatever time you want in seconds.

I set it to 120 seconds because I believe 2 minutes is a good balance.

### No generative AI was used in this project and I do not consent to it being used within any AI tool or assistant.
