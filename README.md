# tweet-generator

This app builds a simple language model from public tweets and generates new tweets based on that.
Donald Trump's tweets are already contained in the repo, other users' data can be added and used from the command line interface.

## How to use

In order to use the CLI, run the main.py-file.
Then, the following command can be used:

- "t": generates a new tweet based on the current language model. The default model is Donald Trump.
- "refresh data [<api_key> <api_secret> <access_token> <access_token_secret>]": pulls the newest tweets corresponding to the current model from twitter and updates the language model. The optional arguments are required for authentication whenever no credentials-file is being used (see below for details).
- "switch <Twitter-handle>": Switches to a new Twitter-account as the basis for the language model and pulls its tweets. This command requires the use of credentials-file (see below). The Twitter-handle has to be entered without the leading @-character.
- "q": Quits the application.
  
## How to authenticate / credentials
  
In order to pull data from the Twitter-api and to update the language model, you need authentication-tokens form Twitter.
You can get them here: https://developer.twitter.com/en/apply-for-access

There are two ways to enter your credentials: Use a credentials-file or enter the tokens manually into the CLI.

The credentials-file has to be a json-file with the name "credentials.json" that is located at the root of the "tweet-generator"-folder and has to contain the fields "api_key", "api_secret", "access_token" and "access_token_secret". The app can then get the tokens from that file, so there is no need to re-enter them at every refresh of the tweet-data.
