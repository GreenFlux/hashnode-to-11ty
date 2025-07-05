---
title: "Why I Built A Code Editor Inside FileMaker Pro"
date: 2024-09-22
permalink: "/why-i-built-a-code-editor-inside-filemaker-pro/"
layout: "post"
excerpt: "Web Viewers in FileMaker Pro are like an escape hatch. When you hit the limits of the native FMP platform, you can always extend it with a web viewer to add new functionality. You can add some really cool features to FileMaker with a web viewer and a..."
coverImage: "https://cdn.hashnode.com/res/hashnode/image/upload/v1727007212211/765cd7de-93e5-45c0-8cab-ee23c220cef4.png"
readTime: 5
tags: ["filemaker", "codemirror", "JavaScript", "claris", "Low Code"]
series: "FileMaker Pro"
---

Web Viewers in FileMaker Pro are like an escape hatch. When you hit the limits of the native FMP platform, you can always extend it with a web viewer to add new functionality. You can add some really cool features to FileMaker with a web viewer and a few JavaScript libraries, like this [grid view](https://github.com/GreenFluxLLC/FileMaker-Experiments/tree/main/CSS%20Grid), and [drag-to-sort](https://github.com/GreenFluxLLC/FileMaker-Experiments/tree/main/SortableFMP) list.

I really enjoy pushing the limits of lowcode platforms, and FileMaker Pro was my first favorite lowcode tool. But let me tell you, working with web viewer code in FileMaker SUCKS! Imagine a CodePen style editor, but with the following restrictions:

* You can’t use double quotes anywhere without escaping them `”\””`
    
* No syntax highlighting
    
* No auto-indent / pretty-print
    
* No template literals. String concatenation using `code` & table::field & `code`
    
* Limited ability to pass data between FMP and web viewer

It’s not an IDE by any means, but then it wasn’t meant to be. However, that leaves you copy and pasting code between some other editor and viewer, testing changes in the other editor, pasting again and saving a layout in FileMaker… it shouldn’t be this hard. Web viewers have so much potential but they are a pain in the ass to use.

## There Has to Be A Better Way

Every time I try to build something in a web viewer, I keep thinking there has to be a better way to store, edit, and test the code. I’ve tried building a 3 pane editor with separate fields for HTML, CSS and JS, then merging them into a single doc with Substitute(). This helps a little, but there’s still no formatting, highlighting, etc. You still have to leave FMP to develop, then copy/paste into FileMaker. If only there were a way to write the code directly in FMP, with syntax highlighting, *and* test results instantly without switching between programs.

# Solution: A Web Viewer to Build Web Viewers

Building a basic code editor with syntax highlighting and multi-language support sounds complex, but it’s actually pretty easy with the CodeMirror library. Just import the library and select a textarea containing the code.

```xml
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CodeMirror Example with Syntax Highlighting</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.13/codemirror.min.css">
  </head>
  <body>
    <textarea id="editor"><h1>Header</h1>
<p>body text. </p>
</textarea>

    <!-- CodeMirror JS and Mode libraries from CDN -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.13/codemirror.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.13/mode/xml/xml.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.13/mode/htmlmixed/htmlmixed.min.js"></script>

    <script>
      // Initialize CodeMirror with default mode (HTML)
      let editor = CodeMirror.fromTextArea(document.getElementById('editor'), {
        lineNumbers: true,
        mode: 'htmlmixed',  // Start with HTML mode
        theme: 'default',
        tabSize: 2
      });
    </script>

  </body>
</html>
```

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1726964622333/3011f3c9-6b20-455c-ace2-f1fdb46c6221.png)

## Using CodeMirror in FileMaker

Dealing with quotes is a pain in FileMaker. You can’t use them directly in the Web Viewer’s input calculation field without escaping them. As a hack, you can store code that includes double quotes by pasting it in a text object on the layout, then using `GetLayoutObjectAttribute( objectName ; “content” )` to get the code without having to escape the quotes.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1727003798424/ffa0c0c0-6bf2-46be-a142-1108125dfe9b.png)

And in Browse Mode:

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1727003905355/08e1327e-4114-4103-abe1-38d0e1ce377c.png)

## Loading Code Stored In FileMaker

To preload the web viewer with code stored in a field in FileMaker, modify the `textarea` to leave a placeholder for inserting the editor’s code using Substitute(). Then, update the web viewer’s source to insert the code. In this case, I have a field named `doc` in a `CodeMirror` table, and the placeholder text in the textarea says EDITOR\_TEXT.

```xml
<textarea id="editor">EDITOR_TEXT</textarea>
```

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1727004103202/a64ddbb3-2e5b-4c9c-8b38-4bf3ba773745.png)

This will pre-load the code editor with code stored in the `CodeMirror::doc` field.

### Other Language Support

To extend your web viewer to support other languages like CSS and JavaScript, just import the libraries for each mode, and then provide a way for the user to switch.

```xml
<!-- CodeMirror mode for CSS -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.13/mode/css/css.min.js"></script>

<!-- CodeMirror mode for JavaScript -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.65.13/mode/javascript/javascript.min.js"></script>
```

You can then modify the `CodeMirror` initialization to allow switching between these languages dynamically. Here’s an updated version with a dropdown for language selection:

```xml
htmlCopy code<div id="toolbar">
  <select id="language-selector">
    <option value="htmlmixed">HTML</option>
    <option value="css">CSS</option>
    <option value="javascript">JavaScript</option>
  </select>
</div>
```

To handle the language switching, you can modify the CodeMirror editor mode when the user selects a language:

```javascript
const languageSelector = document.getElementById('language-selector');

languageSelector.addEventListener('change', function() {
  const selectedMode = this.value;
  editor.setOption('mode', selectedMode);
});
```

Now the syntax highlighting will change based on the selected language.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1727004669686/71061d79-7dfb-4ed8-8b65-a619f1214e85.gif)

### Saving the Data

To save the code written in the CodeMirror editor back into FileMaker, you can use the **FileMaker.PerformScript()** function to trigger a FileMaker script. This allows you to pass the content of the editor as a parameter to the script, then use the Set Field step to insert the code back into FileMaker.

Here’s an example with a "Save" button that will save the editor content:

```xml
htmlCopy code<button id="save-button">Save</button>

<script>
  document.getElementById('save-button').addEventListener('click', function() {
    const editorContent = editor.getValue();
    FileMaker.PerformScript('Save Editor Code', editorContent);
  });
</script>
```

In this case, you’ll need to create a FileMaker script named **"Save Editor Code"** that will handle the content passed from the web viewer and store it in a designated field.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1727004769421/d5a0fe4a-ea4d-4e6e-abd2-6331968693c9.png)

At this point, we have a decent code editor for writing and saving the code without leaving FileMaker.

### Displaying Code in a Second Web Viewer

Now, the code in the `CodeMirror::doc` field can be displayed in a second web viewer. This time no Substitute() is needed, because we want to display the final result from our first web viewer.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1727005069966/2106bd96-9c69-4450-a159-724014205fc3.gif)

### Final Results

And here it is in action. Now you can build and test FileMaker web viewer code directly in FileMaker, with syntax highlighting for any language! And you can view the results instantly by saving the editor code back to FileMaker.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1727006283945/e02bea33-112a-438d-b2cf-14a3565d85ee.gif)

Each record stores its own `doc` field, so you can build a library of web viewer code samples to use in other apps. This should make for a decent web viewer IDE, outputting all the code to a single field that can be used in the next solution.

### Conclusion

Building a new web viewer solution to extend FileMaker can be extremely fun and rewarding when you get it to work, but getting there can be a tedious and frustrating process. Hopefully this solution will help reduce some of that friction and let us focus more on the fun part!

## What’s Next?

CodeMirror has a ton of different options and plugins to extend the functionality. At first, I wasn’t able to ‘select-all’ with the keyboard on mac, but I was able to get it working by adjusting the config. Similarly, you could add keyboard shortcuts for auto-intent or other IDE functionality. Got an idea for another feature? Drop a comment below and I’ll see what I can do!