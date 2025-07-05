---
title: "SQL to JSON in FileMaker using Papa Parse"
date: 2024-12-14
permalink: "/sql-to-json-in-filemaker-using-papa-parse/"
layout: "post"
excerpt: "Recently I needed to upload some data from a local FileMaker database to a REST API as part of a migration. FileMaker’s Insert from Url script step uses curl requests for sending data to another API, and anyone who’s used it knows the struggle of esc..."
coverImage: "https://cdn.hashnode.com/res/hashnode/image/upload/v1734114855939/a74b4709-7620-4c9a-beba-20283491e12e.png"
readTime: 5
tags: ["filemaker", "claris", "papa-parse", "JavaScript", "SQL"]
series: "FileMaker Pro"
---

Recently I needed to upload some data from a local FileMaker database to a REST API as part of a migration. FileMaker’s Insert from Url script step uses curl requests for sending data to another API, and anyone who’s used it knows the struggle of escaping quotes and concatenating field names to build the JSON, one string at a time. FileMaker just wasn’t built with JSON in mind.

But in version 16 they added several functions that made parsing and editing JSON much easier. However, this still requires building the JSON one field at a time, using `JSONSetElement()` for each field. It’s a step up from the old approach, but its still too verbose.

Another approach is to use the FileMaker Data API, also added in version 16. This is a much better method for fetching data in JSON format, but it requires that the file be hosted with FileMaker Server. And my use case was working with a local file.

***So now what?***

Back to looping over the data with a script, or `while()` function? Setting each field, one step at a time to build the JSON?

It probably would have worked fine, but it just felt so clunky. What if you need to do this for 20 different tables?! This could be just a few lines of code in JavaScript, but the JSON functions in FileMaker would require separate scripts or nested loops with complex logic to iterate over the column names of each field. And that doesn’t sound fun at all.

I try to approach every programming problem from a re-usability standpoint, and use variables where possible to enable future application of the code for other use cases. I’d much rather spend a few hours building a dynamic tool, than hard-code something for my one-time use case, even if it takes longer to build. So that’s what I did.

## Enter the Web Viewer

This is a simple problem for JavaScript. Just import a CSV parsing library and feed it some data. All of the looping, header names, escaping quotes, and other nonsense is handled for you with a few config options. Here’s some data, give it back to me in JSON. It’s that simple. Well, except for that whole Web Viewer part.

The trick is getting your data from FileMaker as comma separated values and passing that into the Web Viewer, and then getting the JSON back out. I knew I could do the conversion part with the Papa Parse JavaScript library, and that `FileMaker.PerformScript()` could be used to send data as a parameter to a FileMaker script. So I started with figuring out how to pass in the data.

First I set up a basic Web Viewer using Papa Parse, with hard coded data. This is based on the example from the [Papa Parse docs](https://www.papaparse.com/docs).

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <title>CSV to JSON Converter</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/PapaParse/5.3.0/papaparse.min.js"></script>
  </head>
  <body>
    <button onclick="exportJson()">Export JSON</button>
    <pre><div id="results"></div></pre>
    <script>
      const csvData = `field1,field2,field3
a,b,c
d,e,f`;

      function convertCSVToJSON(csvData) {
        const jsonData = Papa.parse(csvData, {
          header: true,
          skipEmptyLines: true
        }).data;
        return JSON.stringify(jsonData, undefined, 2);
      }

      function exportJson() {
        const jsonData = convertCSVToJSON(csvData);
        document.getElementById('results').textContent = jsonData;
        FileMaker.PerformScript("Process_JSON_from_Webviewer", jsonData); 
      }

      window.onload = exportJson;
    </script>
  </body>
</html>
```

I saved this value into a new field, `tasks::Webviewer` , and then set the Web Viewer’s source to this field.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1734184200793/c6c0304f-58cc-416b-aba4-48cca85dd03f.png)

This imports the Papa Parse library, and passes it a string that is a valid CSV body:

```bash
field1,field2,field3
a,b,c
d,e,f
```

This worked and displayed the resulting JSON. The next step was to get the records I wanted to upload as a CSV string… which isn’t much different than the result from the FileMaker `ExecuteSQL()` return value, if you use the right field and row separators!

## Inserting the CSV Data to the Web Viewer

I started by adding a placeholder `CSV_DATA` to my WebViewerSource HTML, instead of the hard coded data. Then, instead of displaying the HTML doc from the WebViewerSource field directly, I used `SUBSTITUTE()` to swap in the real CSV data, generated using ExecuteSQL.

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <title>CSV to JSON Converter</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/PapaParse/5.3.0/papaparse.min.js"></script>
  </head>
  <body>
    <button onclick="exportJson()">Export JSON</button>
    <pre><div id="results"></div></pre>
    <script>
      const csvData = `CSV_DATA`;

      function convertCSVToJSON(csvData) {
        const jsonData = Papa.parse(csvData, {
          header: true,
          skipEmptyLines: true
        }).data;
        return JSON.stringify(jsonData, undefined, 2);
      }

      function exportJson() {
        const jsonData = convertCSVToJSON(csvData);
        document.getElementById('results').textContent = jsonData;
        FileMaker.PerformScript("Process_JSON_from_Webviewer", jsonData); 
      }

      window.onload = exportJson;
    </script>
  </body>
</html>
```

Web Viewer source:

```plaintext
Let([

    ~headers = "title,status,start,end,progress";     
    ~sqlQuery = "SELECT title, status, start, \"end\", progress FROM tasks";    
    ~rowData  = ExecuteSQL(~sqlQuery; ","; "¶");    
    ~csvData  = ~headers & "¶" & ~rowData;    
    ~htmlDoc  = tasks::Webviewer;    
    ~result   = Substitute ( ~htmlDoc; "CSV_DATA"; ~csvData )
    
    ];
    
    ~result
    
    )
```

In this case, I had to use escape quotes on the field name `end` because it’s an [SQL Reserved Word](https://community.appsmith.com/content/blog/sql-reserved-words).

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1734185020917/229dbc45-6a6b-45ad-aaa1-d9126111e80a.png)

## Extracting the JSON

Lastly, I added a script to be called from the Web Viewer, and receive the JSON as a parameter.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1734184590248/48e842c9-7799-41a5-a5c7-759bcb6bcf69.png)

The Web Viewer HTML calls this script and passes the JSON using the `exportJson` function:

```javascript
      function exportJson() {
        const jsonData = convertCSVToJSON(csvData);
        document.getElementById('results').textContent = jsonData;
        FileMaker.PerformScript("Process_JSON_from_Webviewer", jsonData); 
      }
```

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1734184686277/fed26bf7-abd2-4877-9c0d-0e1730f7e6e4.png)

From here, I was able to use the JSON in the body of a curl request and upload it directly to the API, without having to host the database on FileMaker Server, or build the JSON one field at a time. I’m still hard coding the header names instead of extracting them programmatically, but this allows for manually selecting which fields to send to the API.

### Other Thoughts

If you want, you can also copy the Papa Parse library into a text layout object, then extract it using `getLayoutObjectAttribute()`. Then merge in the script with `SUBSTITUTE()`, enabling it to run completely offline. In my case, I had internet access, but the file wasn’t on a server to allow using the Data API, so this approach worked perfectly.

## Conclusion

The trusty old Web Viewer came through once again. Whenever you hit the limits of the native FileMaker platform, chances are, you just need a web viewer, the right JS library, and a few lines of code. Now if they would only add [syntax highlighting and formatting](https://blog.greenflux.us/why-i-built-a-code-editor-inside-filemaker-pro) to the web viewer source field.