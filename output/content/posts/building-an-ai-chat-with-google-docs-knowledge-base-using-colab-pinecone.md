---
title: "Building an AI Chat with Google Docs Knowledge Base Using Colab + Pinecone"
date: 2024-11-17
permalink: "/building-an-ai-chat-with-google-docs-knowledge-base-using-colab-pinecone/"
layout: "post"
excerpt: "LLMs can be a huge productivity boost for work, but the output is only as good as the input. To get the best results, you often have to provide extra reference data to go with the query. This is know as RAG (Retrieval Augmented Generation), and can b..."
coverImage: "https://cdn.hashnode.com/res/hashnode/image/upload/v1731882286675/30df4356-95c9-4fba-adf4-4102104bf6ae.png"
readTime: 5
---

LLMs can be a huge productivity boost for work, but the output is only as good as the input. To get the best results, you often have to provide extra reference data to go with the query. This is know as RAG (Retrieval Augmented Generation), and can be in the form of documents, images, web searches, or function calling that returns API or SQL query responses.

In this guide, I’ll be building a Chat Assistant with RAG using files from Google Docs as a knowledge base. We’ll set up a source folder with multiple docs to use as a reference, upload them to a Pinecone Assistant, and then chat with the docs using Python.

Pinecone is a fully managed vector database that makes it easy to add vector search to production applications. They offer state-of-the-art vector search libraries, advanced features such as filtering, and distributed infrastructure to provide high performance and reliability at any scale.

## Setup

For this example, I’ve created a new Google Drive folder and included two Google Docs containing previous blog posts \[[post 1](https://blog.greenflux.us/image-to-text-extraction-with-llama32-vision-and-python)\], \[[post2](https://blog.greenflux.us/building-a-data-driven-organizational-chart-in-apps-script)\]. I’ll be asking the assistant specific questions from these blog posts. You can use whatever docs you want, but be sure to start out with only a few files until you have the script tested and working.

Once you have the folder set up with a few docs, sign up for a free [Pinecone](https://app.pinecone.io/) account and go to you dashboard. Select **API Keys** on the left side bar, and copy your key or create a new one.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1731874861694/3c987041-c9fb-40ee-bdc0-f0bb78c4971c.png)

Then open up a new [Google Colab](https://colab.new) project and save the key in the Secrets manager. Name the variable `PINECONE_API_KEY`, paste in the value, and then turn on the *Notebook access* setting to enable it.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1731875020165/9fe2316c-0b08-4bf0-8a39-59b991c47474.png)

Next, add a new code block to install the required libraries, and run it.

```python
!pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib pinecone pinecone-plugin-assistant
```

Then add another code block to import the required libraries, and run it.

```python
import io
import time
from typing import Dict, Any
import requests
from google.colab import auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload
from pinecone import Pinecone
from pinecone_plugins.assistant.models.chat import Message
from google.colab import userdata

api_key = userdata.get('PINECONE_API_KEY')
assistant_name = 'gdocs-chat'
folder_id = 'YOUR_FOLDER_ID'
```

## Connecting to Google Drive and Pinecone

Now that everything is installed and imported, we can set up a new assistant, and a connection to Google Drive. This function will look for an existing Assistant by name, and create it if it doesn’t exist. This way you can choose an existing assistant or create a new one, and not need two different functions.

```python
def initialize_services(api_key: str, assistant_name: str):
   """Initialize Google Drive and Pinecone services."""
   # Initialize Google Drive service
   auth.authenticate_user()
   drive_service = build('drive', 'v3')
   
   # Initialize Pinecone
   pc = Pinecone(api_key=api_key)
   
   try:
       assistant = pc.assistant.Assistant(assistant_name)
   except Exception:
       # Create new assistant if it doesn't exist
       assistant = pc.assistant.create_assistant(
           assistant_name=assistant_name,
           instructions="Answer directly and succinctly. Do not provide any additional information.",
           timeout=60
       )
   
   return drive_service, assistant

# Initialize services and store the results
try:
   drive_service, assistant = initialize_services(api_key, assistant_name)
   print("Services initialized successfully")
except Exception as e:
   print(f"Error during initialization: {str(e)}")
```

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1731875350430/43217513-5238-4c6f-a028-09a82c9ad6db.png)

You should see the Services initialized successfully message. You can now connect to Google Drive and Pinecone.

Head back to Pinecone and refresh the page. You should see the new Assistant in your account.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1731876948524/e20f25b3-ffb6-43b6-bc45-cea9924a2824.png)

## Looping Over Google Docs

Next, we need a function to list all the documents in a given folder ID, and store them as PDFs.

```python
def list_docs_in_folder_as_pdfs(drive_service, folder_id: str) -> list:
    """Retrieve and export all documents from a Google Drive folder to PDFs."""
    try:
        results = drive_service.files().list(
            q=f"'{folder_id}' in parents and mimeType='application/vnd.google-apps.document'",
            spaces='drive',
            fields='nextPageToken, files(id, name, mimeType)'
        ).execute()
        
        pdf_documents = []
        for item in results.get('files', []):
            request = drive_service.files().export_media(
                fileId=item['id'],
                mimeType='application/pdf'
            )
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)
            
            done = False
            while not done:
                status, done = downloader.next_chunk()
                
            pdf_documents.append({
                'id': item['id'],
                'name': item['name'],
                'pdf_content': fh.getvalue()
            })
        
        return pdf_documents
        
    except HttpError as error:
        print(f'An error occurred: {error}')
        return []
```

Lastly, we’ll need a function to upload an individual file to a Pinecone Assistant. Pinecone’s Getting Started docs have a great [example](https://docs.pinecone.io/guides/get-started/assistant-quickstart#4-upload-a-file-to-the-assistant) on uploading a *local file* with Python, but in this case we need a way to upload a file from a variable— after retrieving it from Google Drive. This can be done using the [upload\_file](https://docs.pinecone.io/reference/api/assistant/create_file) method.

```python
def upload_pdf_to_pinecone(
    api_key: str,
    assistant_name: str,
    pdf_document: Dict[str, Any],
    base_url: str = "https://prod-1-data.ke.pinecone.io"
) -> dict:
    """Upload a PDF file to Pinecone from a Google Drive document export."""
    url = f"{base_url}/assistant/files/{assistant_name}"
    headers = {"Api-Key": api_key}
    
    file_obj = io.BytesIO(pdf_document['pdf_content'])
    filename = f"{pdf_document['name']}.pdf"
    
    try:
        response = requests.post(
            url,
            headers=headers,
            files={'file': (filename, file_obj, 'application/pdf')}
        )
        response.raise_for_status()
        return response.json()
        
    except requests.RequestException as e:
        print(f"Failed to upload PDF '{filename}': {str(e)}")
        return None
        
    finally:
        file_obj.close()
```

With each of the utility functions created, we can now loop over the files in a given folder, and upload them all to the Pinecone Assistant.

```python
def upload_all_files():    
    # Initialize services
    drive_service, assistant = initialize_services(api_key, assistant_name)
    
    # Get all PDFs from the folder
    pdf_documents = list_docs_in_folder_as_pdfs(drive_service, folder_id)
    
    if not pdf_documents:
        print("No documents found in the specified folder.")
        return
    
    # Upload all PDFs to Pinecone
    for pdf_doc in pdf_documents:
        print(f"Uploading {pdf_doc['name']}...")
        result = upload_pdf_to_pinecone(
            api_key=api_key,
            assistant_name=assistant_name,
            pdf_document=pdf_doc
        )
        if result:
            print(f"Successfully uploaded {pdf_doc['name']}")
        time.sleep(1)  # Add a small delay between uploads
    
```

## Chatting with the Assistant

Once the files are uploaded, we’ll need one more function to chat with the Assistant.

```python
def chat_with_docs(message: str):
    """Chat with the documents using the Pinecone assistant."""
    pc = Pinecone(api_key=api_key)
    assistant = pc.assistant.Assistant(assistant_name)
    
    msg = Message(content=message)
    resp = assistant.chat(messages=[msg])
    print("\nResponse:", resp.message.content)
```

Ok, with all of the pieces ready, we can now upload all the files from a folder and begin chatting!

```python
upload_all_files()  
chat_with_docs("what other type of work has greenflux done?")
```

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1731883325869/0f6a50a3-8564-4929-b4a4-3e9fca10ba94.png)

Look at that! The assistant answered with specific information from our Google Docs! Now you can chat with your own data using Google Docs as a knowledge base.

![](https://cdn.hashnode.com/res/hashnode/image/upload/v1731877894189/529c957d-b24b-4117-8605-20d362bc8a89.png)

## Conclusion

Pinecone’s Assistants make it easy to upload files for retrieval augmented generation, enabling chat apps with access to your data, and providing more accurate results that are specific to your use case. With just a few Python functions you can build a complete RAG chat app that’s grounded on your own Google Docs data.