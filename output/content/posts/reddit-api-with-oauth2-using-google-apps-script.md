---
title: "Reddit API with OAuth2 using Google Apps Script"
date: 2025-04-30
permalink: "/reddit-api-with-oauth2-using-google-apps-script/"
layout: "post"
excerpt: "Reddit offers several different options for integrating web apps, scripts, and installed apps. Just go to https://www.reddit.com/prefs/apps/ to create a new app and select the type.

In this guide, we’ll be taking a closer look at the script type of ..."
coverImage: "https://cdn.hashnode.com/res/hashnode/image/upload/v1745789526505/126d2634-be20-4bed-8ee9-5accb64109a6.png"
readTime: 5
tags: ["reddit", "REST API", "JavaScript", "google apps script", "OAuth2", "google sheets", "APIs", "social media", "social media marketing"]
series: "Google Apps Script"
---

Reddit offers several different options for integrating web apps, scripts, and installed apps. Just go to [https://www.reddit.com/prefs/apps/](https://www.reddit.com/prefs/apps/) to create a new app and select the type.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1745711363590/ab91b1c0-3435-404a-bab1-948da9ecf2da.png)

In this guide, we’ll be taking a closer look at the *script* type of Reddit app, made to run on a server, without user interaction in the browser. This could be used for scheduled posts from sheet data, automating a notification when a keyword is mentioned, or anything else for use on your own Reddit account.

**Note**: If you’re looking to build an app that *other Reddit users* can install, check out the *installed app* option. This guide is for script-type apps that only work on your account.

## Reddit Authorization Methods

Reddit does not support creating an API key or token from the Reddit website. Regardless of which app type you choose, that app will have to login with either a user name and password, or client\_id and secret.

You can create apps from the Reddit website (installed apps, web apps, or script), and then use the client ID to request an access token to begin using the API from your app.

### Reddit REST API with 2FA Enabled

If your Reddit account has two-factor authentication enabled, Reddit’s won’t allow logging into the API with a user name and password. This makes integrating with the API more complex, or forces you to turn off 2FA just to use the API. I didn’t want to sacrifice security to use the API, so I was looking for a method that would still work with 2FA enabled.

This guide will show you how to integrate with the Reddit API while keeping 2FA enabled. It uses a workaround that requires a one-time authorization in the browser to receive the verification code, after which the script can run completely server-side with no user interaction. This method works perfect for scripts that you want to run on a timer, or trigger with a webhook from another system.

**This guide will cover:**

* Creating an App in Reddit
    
* Requesting an authorization code
    
* Using the code in Apps Script to request an Access and Refresh Token
    
* Keeping the token refreshed
    
* Saving Reddit Data to Google Sheets on a Schedule

***Let’s get to it!***

## Creating an App in Reddit

Start out by creating a [new app](https://www.reddit.com/prefs/apps/) in your Reddit account and choose *Script* for the type. For the redirect URL, enter:

```plaintext
http://localhost
```

This tells Reddit where to send the verification code after you login and authorize your app in the browser.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1745755517378/bac8a432-265f-482e-8d15-4ec9f5babd2f.png)

Next, authorize the app by adding your `client_id` to this url and opening it in the browser:

```plaintext
https://www.reddit.com/api/v1/authorize?client_id=CLIENT_ID&response_type=code&state=random_string&redirect_uri=http://localhost&duration=permanent&scope=read
```

After clicking **Allow**, it should redirect you to your localhost, with the verification code in the URL parameter. The browser will show an error, unless you happen to have a web server running on your local host, but all you need is the code from the URL to use in the next step.

Copy everything between `code=` and `#_` .

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1745756045363/b521d152-3620-4f72-b525-29bf4f034d97.png)

## Requesting an Access Token and Refresh Token

The verification code can now be used to request an access token and refresh token from Apps Script. But we need somewhere to store the refresh token to avoid the browser login every time we run the script.

Create a new Google Spreadsheet with a *credentials* sheet, and columns for `access_token`, `refresh_token`, and `auth_code`.

Enter your auth\_code obtained from the URL in the last step.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1745757415997/6c00502f-1af4-4cdf-8f13-9dd9f7e990b3.png)

Then go to **Extensions** &gt; **Apps Script**, and paste in the following script:

```javascript
// === CONFIGURATION ===
const subredditName = 'GoogleAppsScript';
const userAgent = 'script:Get Subreddit:v1.1 (by /u/YOUR_USER_NAME)';
const credsSheetName = 'credentials';
const creds = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(credsSheetName);
const props = PropertiesService.getScriptProperties().getProperties();
const clientId = props.CLIENT_ID;
const clientSecret = props.SECRET;
const redirectUri = 'http://localhost'; // Ensure this matches your Reddit app config
let accessToken = creds.getRange('A2').getValue();
const refreshToken = creds.getRange('B2').getValue();
const authCode = creds.getRange('C2').getValue();

// Use AuthCode from URL after approving app
function exchangeAuthCodeForTokens() {
  const payload = {
    grant_type: 'authorization_code',
    code: authCode,
    redirect_uri: redirectUri
  };

  const options = {
    method: 'post',
    payload: payload,
    headers: {
      Authorization: 'Basic ' + Utilities.base64Encode(`${clientId}:${clientSecret}`),
    },
    muteHttpExceptions: true
  };

  Logger.log("Exchange Auth Code Request Options: " + JSON.stringify(options, null, 2));

  const response = UrlFetchApp.fetch('https://www.reddit.com/api/v1/access_token', options);
  Logger.log("Exchange Auth Code Response: " + response.getContentText());

  const tokens = JSON.parse(response.getContentText());

  if (tokens && tokens.access_token && tokens.refresh_token) {
    creds.getRange('A2').setValue(tokens.access_token);
    creds.getRange('B2').setValue(tokens.refresh_token);
    creds.getRange('C2').clearContent(); // Clear the used auth code
    return tokens.access_token;
  } else {
    Logger.log("Error exchanging auth code: " + response.getContentText());
    return null;
  }
}
```

Next, go to **Project Settings** and scroll down to **Script Properties**. Add properties for the `CLIENT_ID` and `SECRET` and add the values from your Reddit app.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1745786865872/bc595747-866a-4767-807f-f0c1d2e9bf3d.png)

Save the script and run it, and approve the permissions request on the first run. You should see the auth\_code in the sheet replaced with an access token and refresh token.

**Note**: *Auth codes only work once!* If you lose the valid refresh token in the sheet or want to retest this function, you’ll have to revisit the link to authorize the app again and get a new code. Also, these codes are short-lived. So the first one may have expired by the time you try testing this function. Just request a new code and update the sheet, then run the function again to get the tokens.

## Exchanging the Refresh Token for a new Access Token

Next we need a function to get a new access token in case the current one is expired.

```javascript
function refreshRedditToken() {
  const payload = {
    grant_type: 'refresh_token',
    refresh_token: refreshToken
  };

  const options = {
    method: 'post',
    payload: payload,
    headers: {
      Authorization: 'Basic ' + Utilities.base64Encode(`${clientId}:${clientSecret}`),
    },
    muteHttpExceptions: true
  };

  Logger.log("Refresh Token Request Options: " + JSON.stringify(options, null, 2));

  const response = UrlFetchApp.fetch('https://www.reddit.com/api/v1/access_token', options);
  Logger.log("Refresh Token Response: " + response.getContentText());

  const tokens = JSON.parse(response.getContentText());
  if (tokens && tokens.access_token) {
    creds.getRange('A2').setValue(tokens.access_token);
    return tokens.access_token;
  } else {
    Logger.log("Error refreshing token: " + response.getContentText());
    return null;
  }
}
```

Save and then run this function and you should see the access\_token updated in the sheet. Now this function can be called at any time to get an updated access\_token, and then call the Reddit API with authentication.

## Saving Reddit Data to Google Sheets

Lastly we’ll add a function to pull some metrics about a subreddit, and save it to a new sheet. Create a `metrics` sheet and add columns for `timestamp`, `subreddit`, `subscribers`, and `active_users`.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1745787381522/7a71dc8a-c348-4b23-bbd9-399b320ef1d7.png)

Then add a few lines to the config at the top:

```javascript
const metricsSheetName = 'metrics'; 
const metrics = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(metricsSheetName);
```

And a function to get the Subreddit metrics:

```javascript
// === REDDIT METRICS ===
function getSubreddit() {
  //First run, using auth code from URL after approving app
  if (!accessToken && authCode) {
    accessToken = exchangeAuthCodeForTokens();
    // If successful, accessToken and refreshToken should now be in the sheet
    accessToken = creds.getRange('A2').getValue(); // Get the newly stored access token
  } else if (!accessToken && refreshToken) {
    accessToken = refreshRedditToken();
  }

  if (accessToken) {
    const response = UrlFetchApp.fetch(`https://oauth.reddit.com/r/${subredditName}/about`, {
      method: 'get',
      headers: {
        Authorization: 'Bearer ' + accessToken,
        'User-Agent': userAgent
      }
    });

    const redditData = JSON.parse(response.getContentText()).data;
    metrics.appendRow([ 
      new Date().toDateString(),
      redditData.display_name,
      redditData.subscribers, 
      redditData.active_user_count, 
      ])
    Logger.log(redditData);

    return redditData;
  } else {
    Logger.log('No access token available. Ensure you have either an auth code or a refresh token.');
    return { reddit_subscribers: null }; 
  }
}
```

Save and run the function, and approve the new permissions if needed. You should now see a new row logged from the Reddit API.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1745787611050/f6fc6cc8-2afc-4f4c-9c50-6f3ad5b72611.png)

To access other data from the Reddit API, see the API docs [here](https://www.reddit.com/dev/api/).

## Conclusion

This is just one method of accessing the Reddit API. There are easier ways that avoid the one-time browser login, but that requires disabling two-factor authentication. If you’re looking for a secure way to use the Reddit API on a timer or triggered by a webhook, this is a decent solution for personal use.

### What’s Next?

From here, you could chart a subreddit’s growth, schedule posts using sheet data, or get notified when certain key words are mentioned. Although if it’s mentions you’re after, I highly recommend checking out [F5Bot](https://f5bot.com/). Their free service will email you any time a keyword is mentioned on Reddit or Hacker News. This can be used in combination with Apps Script and a mail filter that applies a certain label, simplifying the script and avoiding the Reddit auth.