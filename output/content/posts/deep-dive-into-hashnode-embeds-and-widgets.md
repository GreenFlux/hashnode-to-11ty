---
title: "Deep Dive Into Hashnode Embeds and Widgets"
date: 2025-05-30
permalink: "/deep-dive-into-hashnode-embeds-and-widgets/"
layout: "post"
excerpt: "I’ve been using Hashnode for my blog for about 5 years now. I originally chose it because it was the only option that supported connecting a custom domain for free, and 5 years later I have no regrets. Actually, I’m doubling down.
While I’m quite hap..."
coverImage: "https://cdn.hashnode.com/res/hashnode/image/upload/v1748645473466/6f8834ad-1c5b-480e-a0df-8dfa586c78da.png"
readTime: 5
tags: ["Hashnode", "iframe", "widgets", "knowledge graph", "HTML"]
---

I’ve been using Hashnode for my blog for about 5 years now. I originally chose it because it was the only option that supported connecting a custom domain for free, and 5 years later I have no regrets. Actually, I’m doubling down.

While I’m quite happy with the features of Hashnode that I *do* use, I recently realized that there’s another set of features that I haven’t explored at all: **embeds** and **widgets**. So I decided to do a deep-dive into the various embed options and see what else Hashnode has to offer. I’ll be testing out several of these options in this post, and providing real use cases and examples that I’ll be adding to the rest of my blogs.

## Built-in Support

Hashnode has built-in support for embedding content from several different services, using only the URL. You can access the embed menu by typing:

`/embeds`

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1742435568114/576bceb8-777d-4fa2-8dae-ad31dfeebd54.png)

This allows you to embed live, interactive content from other platforms. You can embed an external link, YouTube Video, Tweet, CodePen, or several other options, just by adding a link.

**Here are a few examples:**

You can embed a Tweet, but you have to replace *x.com* with ***twitter.com***.

%[https://twitter.com/greenflux_dev/status/1858286704618250321] 

Or a YouTube video

%[https://youtu.be/xOfJukfKM3U] 

Or even a playlist:

%[https://www.youtube.com/playlist?list=PLE_KXGiWfqwhADyWxNZJhwn7HF89KxiKB] 

You can also embed live, interactive code using CodePen!

%[https://codepen.io/GreenFlux/pen/yLdwgxN] 

All of these options work using only the URL itself, without needing to copy the iframe embed code from the source site. Just paste in the direct URL, video or CodePen link and it will display the embedded content.

Here’s the full list of supported sites:  
[https://docs.hashnode.com/help-center/hashnode-editor/which-embeds-are-supported-by-hashnode](https://docs.hashnode.com/help-center/hashnode-editor/which-embeds-are-supported-by-hashnode)

These work great for content you want to embed just once, in a single article. But what if you want to add the same embed to every page, or make it reusable on select pages?

## Hashnode Widgets

Another option is to create a [widget](https://docs.hashnode.com/blogs/blog-dashboard/widgets). This allows you to reuse the embed in any post. You can reference it with `%%WIDGET_NAME`, anywhere in your markdown, and the widget will get inserted. Or use `/widget` to display a list of available widget to insert.

To create a widget, you need the full embed code from YouTube, CodePen, or whatever site you want to use, not just the URL.

Here’s a widget using the profile card embed code from Daily.dev.

%%[dailydev] 

And here’s the code used for the widget:

```xml
<a href="https://app.daily.dev/greenflux"><img src="https://api.daily.dev/devcards/v2/ZPb9mU4UbNJoR54JkhxoC.png?type=default&r=bw8" width="356" alt="Joseph Petty's Dev Card"/></a>
```

### Pinned embeds

Want to show the same embed on every page? Crate a custom embed and pin it. You can pin up to two widgets.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1748645857357/d3f420ba-e7a5-4ec1-b347-56041c04ccb4.png)

## Interactive Widgets

You can even embed interactive content using other websites, or a no-code/low-code app builder. Here’s a custom widget I made in Appsmith to display an interactive knowledge graph of all of my blog posts. Try zooming on the middle and selecting a node.

%%[blog-graph] 

View the app in full screen here:

[https://app.appsmith.com/app/hashnode/graph-67ff01cb70e14943222474a8](https://app.appsmith.com/app/hashnode/graph-67ff01cb70e14943222474a8)

## Conclusion

It turns out there’s quite a bit you can do with Hashnode embeds and widgets. I’ll be using these more in my blog now, and creating more interactive content. The CodePen and Appsmith embeds in particular seem to have quite a bit of potential for interactive tutorial content. Drop a comment below if you have a specific topic you’d like me to cover!