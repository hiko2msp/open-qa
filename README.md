# open-qa

A simple question answering system using slack bot

## Usage

1. Fork it!
1. Get API Token from slack developers page.
1. Get service account credentials from google developers page.
1. Create Google Spread Sheet with name "BotCommunicationPatterns".
1. Deploy it with Heroku using [Github Integration](https://devcenter.heroku.com/articles/github-integration)

  + Set Config Vars
    + API\_TOKEN: Your Slack API Token
    + SERVICE\_ACCOUNT: Your Service Account for Google Spread Sheet as JSON Text
    + SHEET\_KEY: Your key of Google Spread Sheet (Please copy it from sheet URL)
1. Launch Apps
