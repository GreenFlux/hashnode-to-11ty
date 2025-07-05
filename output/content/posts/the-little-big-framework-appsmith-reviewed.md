---
title: "The Little Big Framework: Appsmith Reviewed"
date: 2021-09-22
permalink: "/the-little-big-framework-appsmith-reviewed/"
layout: "post"
excerpt: "Intro
Hi, I'm Joseph Petty from GreenFlux, LLC - I'm a full-time freelancer/developer- focused on mobile/web apps, databases, and no/low-code platforms and integrations. I've been using Appsmith for a while now and have written a few  other posts  on..."
coverImage: "https://cdn.hashnode.com/res/hashnode/image/upload/v1632313770813/yF8kaRjTc.png"
readTime: 5
tags: ["Developer Tools", "app development", "Devops", "Databases", "APIs"]
series: "Appsmith"
---

# Intro
Hi, I'm Joseph Petty from @[GreenFlux, LLC](@greenflux) - I'm a full-time freelancer/developer- focused on mobile/web apps, databases, and no/low-code platforms and integrations. I've been using Appsmith for a while now and have written a few  [other posts](https://blog.greenflux.us/)  on it already, so I figured it was time to do a full review of the platform. 

### So what is Appsmith? 

Well, for one thing- it's SUPER new, like just over a year old. But you'd have no idea just from using it. Their dev team is blazing fast 🔥 and has been churning out awesome new features almost every week since I started using it. 

That being said, it *is* still a very young platform, so it's expected that some major features are still in development. I think they're off to an amazing start and I just wanted to mention how new the platform is before talking about any missing features. 

Before I get into the details, here's a quick overview of what **can** be built with Appsmith- *and what can't* (yet 😉).

- ✅ - Web apps, admin panels, dashboards, reporting tools, etc
- ✅ - Full page or iframe browser-based apps
- ✅ - White-labeled apps (remove all Appsmith branding)
- ✅ - Datasource connections (APIs, *-SQL, GraphQL, Google Sheets)
- ✅ - Custom Javascript to transform data or add logic/UI features

- ❌ - Native/hybrid mobile app
- ❌ - Cron Jobs (coming soon)
- ❌ - Custom Themes (coming soon)
- ❌ - App versioning/History (coming soon)
- ❌ - Audit Logs (coming soon)
- ❌ - Granular permissions/ User groups (Enterprise Plan?)

So at a high-level, Appsmith is a powerful developer tool for quickly building UIs and connecting to a wide range of datasources. It's no-code in the sense that UI is drag and drop with an open grid-style canvas. When it comes to adding logic, transforming data and defining workflows, Appsmith lets you insert plain Javascript right inside any widget, query, or almost any other setting. 

I love this approach because there's no made-up abstraction layer or terminology to learn on the code side. Yes, you need to understand some basic Javascript, but that's a very useful, transferable skill. Working in Appsmith has pushed me to learn more Javascript and made me a better developer. 

Ok, enough rambling; on to the details:

# Open Source
Appsmith is an open-source project, so the code is entirely free to use. You can even host your own server with unlimited users, create custom widgets, and submit your own features/bug fixes through GitHub. The dev team is very welcoming to community contributions, and I've already seen a few features added by members from the Discord. 

They've also been fast to approve new feature requests and add them to GitHub when new ideas come up in Discord. I've seen them take a suggestion and create a new issue in GitHub within minutes, and on several occasions.  

# Pricing
So the code is free to use, but it has to be hosted somewhere. Now, if setting up a server isn't for you, don't worry! Appsmith also offers FREE HOSTING with unlimited users, datasources, and apps! 

![Screen Shot 2021-09-18 at 11.33.19 AM.png](https://cdn.hashnode.com/res/hashnode/image/upload/v1631979505204/9HPTn4X5u.png)

There is also an Enterprise Plan in the works, but pricing details are yet to be released.  

# Widgets
Widgets are the basic UI building blocks in Appsmith. Interface components like buttons, tables, file pickers, etc, are displayed on a left sidebar. Just drag and drop widgets anywhere on the canvas grid and adjust the settings to change the appearance or connect a datasource. 

![Screen Shot 2021-09-18 at 11.49.06 AM.png](https://cdn.hashnode.com/res/hashnode/image/upload/v1631980153157/Hs0ZEhrmd.png)

# Data Sources
There are no-code builders that use Google Sheets as a backend, others that can connect to SQL data sources, and a few with decent API connectors... 

**And then there's APPSMITH! ** 🤯

![Screen Shot 2021-09-18 at 11.50.17 AM.png](https://cdn.hashnode.com/res/hashnode/image/upload/v1631980225834/j4TnFJ0MY.png)

**And on top of the wide range of source-specific connectors, the Datasources tab has some *really cool* extras:** 😎

**Sample Datasets:**
Jump straight to building without setting up a database by using the mock datasets! 

**Authenticated API:**
Save API credentials once, and then add any new request under that source. No need to authenticate each new endpoint or method when you add a new one. 

**Import from CURL:** 
Paste in a CURL request from another source, and Appsmith will parse out the headers, endpoint, body, etc and add a new API automatically! 

**Generate Page from Datasource:**
Just pick a datasource and a searchable column, and BOOM! 🪄💥 **NEW APP!**
https://github.com/appsmithorg/appsmith/pull/5513

# Deploy and Share
Changes are saved automatically and reflected in real-time in the Appsmith editor, but you have to click **Deploy** to push those updates to the live version of the app. So you can make multiple edits/saves and see the results in the editor, but App Users won't see them until those changes are deployed. 

Appsmith groups app by Organization, and uses these groups to share apps with other users. When you share an app with someone, you're actually sharing all apps in that organization- so be sure to organize your apps into Organizations that match the user-groups you intend to share with. 

# Hosting
Appsmith offers free hosting on their Appsmith Cloud instance, as well as an Enterprise plan that is still being developed. Users may also host their own version for free. 

Here's a detailed guide on how to deploy your own Appsmith server on Docker:
https://docs.appsmith.com/setup/docker

# Javascript
Transform data, and add logic/formatting to UI components with plain Javascript. 
Appsmith is no-code when it comes to dragging Widgets into the canvas. When it's time to add more advanced features, many platforms have created their own internal language or abstraction layer, which can be hard to learn and limited in functionality. But Appsmith lets you insert raw Javascript right inside any widget, API or query template, or other setting. 

![Screen Shot 2021-09-18 at 6.07.19 PM.png](https://cdn.hashnode.com/res/hashnode/image/upload/v1632002931170/C0e6vGB_M.png)

The beauty of Appsmith is in the ability to insert Javascript just about anywhere in the app. The APIs/DB Queries you create can be triggered by, or used to control, widget appearance, visibility, behavior, etc. 

![Screen Shot 2021-09-19 at 8.11.19 PM.png](https://cdn.hashnode.com/res/hashnode/image/upload/v1632096819688/7dQMq7u6b.png)

![Screen Shot 2021-09-19 at 8.17.52 PM.png](https://cdn.hashnode.com/res/hashnode/image/upload/v1632097079612/mvI9ofSSH.png)

Every Widget is a JSON object and can be referenced by the name you give it in the properties pane. The editor auto-completes and suggests available Widgets and Queries as you type. 

![2021-09-19 20.25.05.gif](https://cdn.hashnode.com/res/hashnode/image/upload/v1632097537029/fuz7m_dvi.gif)

# Integrations
Integrating with APIs in Appsmith is straightforward and direct. The UI is very similar to Postman- and gives you direct access to view responses and errors right in the editor. 

![Screen Shot 2021-09-18 at 4.53.41 PM.png](https://cdn.hashnode.com/res/hashnode/image/upload/v1631998445362/NWj28duJh.png)

When connecting an API to a widget, the widget's property pane displays the data from the last response right in the editor. So you can connect directly to an external API as a datasource, and see the results as you're building the app! 

![Screen Shot 2021-09-18 at 5.13.46 PM.png](https://cdn.hashnode.com/res/hashnode/image/upload/v1631999633712/xQIAJkyQZ.png)

# Workflows 
There aren't really any specific features dedicated to creating workflows or automating processes, but that's not to say it can't be done. You can easily chain together multiple APIs or DB queries using Javascript.

Also worth noting, there's no way to trigger Javascript without user interaction, however, there's a feature in testing to run a function on page load. 

Another option for automations is to integrate with n8n.io or other automation platforms using webhooks. Here's a great tutorial from one of the community calls a few months ago. 

https://www.youtube.com/watch?v=mWZGn8kuIBo&t=1s

# Security
When sharing an app with a new user, you can assign them one of 3 Roles:

**Administrator: **  
- Create/Edit App
- View App
- Make App Public
- Invite Users
- Manage Users  

**Developer:**  
- Create/Edit App
- View App
- Invite Users  

**App Viewer:**  
- View App
- Invite Users as App Viewers only

New users can sign up with Google, GitHub, or just an email and password. There is no Multi-factor Authentication. SAML/SSO and granular access controls are in the Enterprise Plan only. 

When you create an app and save API or database credentials, those values are never sent to the browser for **App Users**. The Appsmith servers (or your own hosted server) act as a proxy layer to append the request with credentials before forwarding it to the endpoint or database. The  response goes directly to the client's browser. The Appsmith servers do not store any of the query responses. 

[DOCS: does-appsmith-store-my-data](https://docs.appsmith.com/security#does-appsmith-store-my-data)

# Architecture
So how does Appsmith `*smith* apps? 

Well, the app definition is stored in plain JSON on the Appsmith server. That JSON gets sent to each client, where the page is built client-side using Javascript and DSL. 

So there's no HTML page being stored or generated on a server and sent to the client. The app definition is sent from the server to the client's browser (minus the credentials- for App Users), along with some Javascript needed to dynamically build the page and form requests to the Appsmith server. 

# App Versioning /Exporting
Apps can be exported as plain JSON and imported back into any server. You can build your app on the free Appsmith cloud and later export to run on your own server or vice-versa. So it's easy to manually save your own backup copies at any time and recover if needed. 

There's also a GitSync feature in beta right now that should be released soon to allow syncing backup copies to GitHub. However, at the moment, there is no way to save multiple app versions or recover old versions aside from manually exporting and importing. 

# Community
The Appsmith team provide excellent support via several channels:
- Discord: https://discord.com/invite/rBTTVJp
- Community Forum: https://community.appsmith.com/
- Intercom: Chat popup in Editor and Docs

The Discord is pretty active but the forum was launched a few months ago, so it's just starting to pick up. 

Appsmith has also been very active in reaching out to the community for feedback. And they host a live community call every Thursday at 1 PM Eastern to demo new/upcoming features and answer questions from the community. 

# Roadmap
- Custom Themes
- Reusable Javascript functions and larger JS editor
- GitSync for App Versioning
- Custom JS objects and functions, reusable across apps 😻

# Summary
With a no-code UI builder, TONS of data source connectors, custom Javascript, an open-source license and thriving community, Appsmith is uniquely positioned in the no-code builder market space. There's still some work to be done regarding Enterprise features, and the lack of a mobile client limits use-cases. But given Appsmith's current feature set at this early stage and the speed of the developer team, the incredible power of this platform will only continue to grow.