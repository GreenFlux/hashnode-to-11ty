---
title: "So you want to integrate with the SEC API"
date: 2025-06-23
permalink: "/so-you-want-to-integrate-with-the-sec-api/"
layout: "post"
excerpt: "Hello, yes I’d like to speak to the (developer experience) manager! 🤬


☝️That was me a few weeks ago when I first tried using the SEC API.
I’ve integrated with a lot of APIs over the years, but none have thrown me quite as many curve balls as this ..."
coverImage: "https://cdn.hashnode.com/res/hashnode/image/upload/v1750518143975/04356db1-9dcd-46f5-9ae2-5b30a17d4220.png"
readTime: 5
tags: ["finance", "fintech", "stockmarket", "stocks", "JavaScript", "json", "xml", "CORS"]
---

{% raw %}
> Hello, yes I’d like to speak to the (developer experience) manager! *🤬*

![](https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExc20zcjhwbTk1c3JkdnN2bTVuODJkdXlzZGh1a2kxc2prMnF5YWRiMSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/wIU9MjBVKF4Qw/giphy.gif)

☝️**That was me a few weeks ago when I first tried using the** [**SEC API**](https://www.sec.gov/search-filings/edgar-application-programming-interfaces)**.**

I’ve integrated with a lot of APIs over the years, but none have thrown me quite as many curve balls as this ancient beast and its mysterious endpoints. But I’m over my rage phase now. I’m not here to throw shade. Actually, I’ve come to understand and appreciate the oddities of the SEC endpoints. Although difficult to work with at first, it turns out there are very valid reasons for the design choices that seem hell-bent on ruining your weekend project.

In this post, I’ll break down the various hurdles when integrating with the SEC API, and provide some boilerplate JavaScript functions that can be used as a starting point for your project. There are some more advanced libraries and tools that can abstract away these complexities, but this post is for developers who would like to understand the data formats involved, and how to transform them for displaying in the UI without using other libraries. Let’s do it the hard way and learn something!

## Problem #0 : No API Key Required?

This one isn’t really an issue, just an oddity, and one of the first things I noticed. The SEC API doesn’t require an API key. They don’t even offer an option to create one!? But they do require a `User-Agent` header, to identify the app and provide contact info for the developer. It should be in the format `app_name email@example.com`, and is sort of like an API key *that you define*.

This makes sense though, because the API is read-only. So the only purpose of the user-agent is to limit usage and prevent abuse.

## Problem #1: CORS? More Like NO-RS!

If you’re trying to fetch SEC data from the browser, especially from environments like CodePen or a local dev server, you’re gonna have a bad time. The SEC API does **not** include CORS headers, so you can’t access it directly from the frontend due to browser security restrictions.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1750508668610/d6bb531b-a50b-41a1-b033-489a8e2a9942.png)

So how do you get around the CORS errors? You have a few options:

**Option A: Use a proxy to fetch from browser/client-side (not for production)**

```javascript
const proxy = 'https://corsproxy.io/?';
const url = proxy + encodeURIComponent('https://www.sec.gov/files/company_tickers.json');

const res = await fetch(url);
const data = await res.json();

/* or as a one-liner
fetch('https://corsproxy.io/?'+encodeURIComponent('https://www.sec.gov/files/company_tickers.json'))
  .then(r => r.json())
  .then(console.log);
*/
```

**Option B: Fetch server-side**

```javascript
// Node.js or serverless function with a backend fetch
const data = await fetch('https://www.sec.gov/files/company_tickers.json', {
  headers: { 'User-Agent': 'my-sec-app myemail@example.com' }
}).then(r => r.json());
```

**Option C: Download and host the file**

```bash
curl https://www.sec.gov/files/company_tickers.json -o tickers.json
```

Alright, that’s easy enough to work around. But why are client-side requests blocked?

CORS restrictions are not common on REST APIs that have API Keys, but this one only has a User-Agent header. The CORS restrictions help prevent abuse and heavy traffic from anonymous users.

For this guide, I’ll be using Appsmith to run the APIs server-side, so CORS won’t be an issue.

---

### Problem #2: Ticker Lookup Format is Not an Array

Ok, you made it past the CORS issues, and now you want to list out companies and their tickers. Sounds easy?

You’d expect the API to return *an array* of company *objects*. Instead, you get an *object* with numeric-strings as keys:

```javascript
{
  "0": { "cik_str": 789019, "ticker": "MSFT", "title": "MICROSOFT CORP" },
  "1": { "cik_str": 320193, "ticker": "AAPL", "title": "Apple Inc." },
...
// 
}
```

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1750462348470/bfa5881a-d9ba-4135-95ce-da52c5b4c6cf.png)

Yes, that’s a single object with **10034** properties, using sequential integers-as-strings for the keys. 🤮

Luckily this can easily be converted into an array of objects:

```javascript
	tickerTable(){
		return Object.values(GetTickers.data)
	}
```

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1750462515436/c885863a-4f36-4df6-ad0e-b956e596e6e9.png)

Ok, easy fix. ***BUT WHY!?!?*** Most UI tools expect an array of objects for the input data.

Well, this format dates back to the 1990s for IDX/TSV files which were commonly used then for bulk downloads. Single objects are also faster for adding/updating a company’s properties vs an array format.

### Problem #3: Columnar Instead of Row-Based Data

The `filings.recent` section returns each field as a separate array—one array for dates, another for form types, etc.

```javascript
{
  "filingDate": ["2024-06-18", "2024-06-17"],
  "form": ["8-K", "10-Q"],
  "accessionNumber": ["0000320193-24-000058", "0000320193-24-000054"]
}
```

Instead of an array of objects, it’s an object of arrays. Fun! 🫠

![](https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExdmtmZ3EzbmdvdGowYWYzbGpjMTM5MmRteTFramVobzNsM3YwamczeiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/ukGm72ZLZvYfS/giphy.gif)

#### 💡 Solution

Map over the list of headers and build an array of objects. This requires an outer loop for the list of fields, and an inner loop to reduce each row to an object.

```javascript
	fields: [
		'accessionNumber','filingDate','reportDate',
		'form','fileNumber','primaryDocument'
	],

	/** Convert SEC "columns‑as‑arrays" structure → rows of objects */
buildSubmissions() {
  const src = GetSubmissions.data.filings.recent; // SEC payload
  const n = Math.max(...this.fields.map(f => src[f] ?. length || 0));
  return Array.from({
    length: n
  }, (_, i) => this.fields.reduce((row, key) => {
    row[key] = src[key] ?. [i] ?? null; // keep order + fill blanks
    return row;
  }, {}));
}
```

Now `buildSubmissions()` returns an array of rows ready for UI rendering.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1750510121800/6ee00f22-4ff3-4253-95c2-ee5f96e965ec.png)

Not nearly as easy as the last fix, but still manageable. But WHY?! What’s with all these weird formats?

The "columns-as-arrays" structure found in `filings.recent` mirrors the bulk dataset format used in downloadable EDGAR index files going back decades (e.g., .tsv and .idx files). This format is efficient for batch processing and CSV-style exports.

---

### Problem #4: CIK and Accession Numbers Require Manual Cleanup

Most people only know companies by their name, and maybe their stock ticker, but not their CIK number. Unfortunately, it’s the CIK number you need in the URL to lookup company info. So first you have to lookup the CIK with a different endpoint, then use that to search for more info on the company.

That’s not an uncommon pattern with REST APIs, but it is complicated by the leading zeros that must be added in the URLs. CIK numbers should be padded with zeros to ensure the string is 10 characters. But that’s not how the `/company_tickers.json` endpoint returns them.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1750510870992/2a5e1395-cf3c-4b14-86ac-7000147c56c5.png)

So once you lookup the CIK number and want to use it in the next API, you have to add the extra zeros to make it 10 digits.

```bash
https://data.sec.gov/api/xbrl/companyfacts/CIK{{String(Table1.selectedRow.cik_str).padStart(10, '0')}}.json
```

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1750511010430/190eb07f-6d87-402a-be0d-938363f71db2.png)

Also, the accession number includes dashes (`"0000320193-24-000058"`), but the URLs to filings on sec.gov require you to strip them out.

```javascript
const accPlain = accessionNumber.replace(/-/g, '');
const url = `https://www.sec.gov/Archives/edgar/data/${cik}/${accPlain}/${primaryDocument}`;
```

So what’s the deal with this one? Your guess is as good as mine. It’s probably a limitation or requirement of the website’s archiving structure.

### Problem #5: Some Endpoints Return XML

You finally lookup the CIK number, add the zeros, and use it get a company filing, and—surprise—it’s XML, not JSON.

#### 💡 Solution

Use [`fast-xml-parser`](https://github.com/NaturalIntelligence/fast-xml-parser):

```python
import { XMLParser } from 'fast-xml-parser';

const parser = new XMLParser();
const parsed = parser.parse(xmlString);
```

Again, this one just comes down to the SEC API being old and slow to evolve to modern standards.

---

### So what’s the deal? Why so many hurdles with this API?

It’s tempting to chalk this up to outdated tech, and you wouldn’t be wrong. EDGAR was built in **1993** to support compliance and disclosure, not RESTful UIs. But there’s more to it than that.

The “API” you see now is a modernized wrapper around legacy systems and bulk download indexes that haven’t changed in decades. The data structures returned by the API resemble CSVs and fixed-width formats because that’s what the wrapper is built around.

Additionally, the SEC’s priority is public access, not developer convenience. Think “download 10 years of filings” more than “live queries from a React app.”

In other words, the SEC API lacks a modern REST API experience because it’s not meant to be the backend for your project. It’s a public archive, and and the fact that it has an API at all is a bonus.

---

### Conclusion

The SEC API is not broken—it’s just built for a different audience, from a different era. But once you understand the quirks, it’s completely usable and incredibly powerful.

Hopefully, this post helped you skip the rage phase and jump straight to working with the data. If you're building with Appsmith or another frontend framework, you can use the patterns and snippets here to normalize and present filings, company info, and primary documents in a user-friendly UI.
{% endraw %}