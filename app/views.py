from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)
from django.views import View
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.views.generic import FormView
from django.urls import reverse
import json 
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, FormView
from .decorators import only_authenticated_user, redirect_authenticated_user
from .models import (Docs)
import random 
import uuid
import io    
import json
from django.http import HttpResponse
import os 
import requests
from users.models import CustomUser
import re 
from django.http import FileResponse


class Setup(View):
    template = "setup.html"
    def get(self, request, *args, **kwargs):
        return render(self.request, self.template)
    

from django.contrib.staticfiles.views import serve as static_serve

def serve_build_files(request, path):
    file_path = os.path.join(settings.BASE_DIR, 'build', path)
    try:
        return static_serve(request, path, document_root=file_path)
    except FileNotFoundError:
        return HttpResponse('File not found', status=404)


class Dashboard(View):
    template = "dashboard.html"
    def get(self, request, *args, **kwargs):
        user = request.user
        docs = Docs.objects.filter(user=user)

        context = {
            "user": user, 
            "docs": docs,
            "error": True
        }
        return render(self.request, self.template, context)
    


class App(View):
    template = "app.html"
    def get(self, request, id, *args, **kwargs):
        user = request.user
        
        docs = Docs.objects.get(id=id)

        context = {
            "docs": docs,
            "smart_report": docs.short_summary,
            'id': id,
        }
        return render(self.request, self.template, context=context)
    

class UserProfile(View):
    template = "user_profile.html"
    def get(self, request, *args, **kwargs):
        context = {

        }
        return render(self.request, self.template)


def generate_gpt(text, history=[]):
        headers = {"Authorization": f"Bearer {settings.EDEN_AI_API_KEY}"}
        url ="https://api.edenai.run/v2/text/chat"
        payload = {
            "providers": "openai",
            "text": text,
            "chat_global_action": "Follow user instructions",
            "previous_history" : history,
            "temperature" : 0.0,
            "settings":{"openai":"gpt-3.5-turbo"},
            "max_tokens" : 1000
            }
        response = requests.post(url, json=payload, headers=headers)
        try:
            result = json.loads(response.text)
            msg = result['openai']['generated_text']
            # print(msg)
        except Exception as e:
            return 
        return msg
    


from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


# ============== CORE BACKEND ENGINE ====================
import PyPDF2
import ai21
import os
import textwrap


class Update_profile(View):
    def post(self, request):
        data = json.loads(request.body)
        user = request.user 
        user.first_name = data['first_']
        user.last_name = data['sec_']
        user.save()
        return JsonResponse({'msg': True})



def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        num_pages = len(reader.pages) 

        for page_num in range(num_pages):
            page = reader.pages[page_num] 
            text += page.extract_text()

    return text


def generate_summary(_path):
    txt = extract_text_from_pdf(_path)
    sums = []
    chunks = textwrap.wrap(txt, 10000)

    for i in chunks:
        response = ai21.Summarize.execute(
            source=i,
            sourceType='TEXT')
        sums.append(response['summary'])

    gen_data = " ".join(sums)
    return gen_data



SHORT_SUMMARY_PROMPT = '''
You are given a candidates resume raw text, write a 2-3 lines short description of it.  Your output should be in 2-3 long detailed lines, No replies/greetings-text or explanations required.
Here's the text 
'''


class UploadFiles(View):
    def post(self, request):
        from .pdf_generator import extract_text_from_pdf, generate_pdf, extract_text_from_docx, modify_docx
        from .chat_ml import build_embeddings
        file = request.FILES.get('files_txt')  
        user = request.user

        if file:
            # Get the original filename
            original_filename = file.name

            # Generate a random UUID filename
            filename = str(uuid.uuid4())

            # Get the file extension
            file_extension = os.path.splitext(original_filename)[1]
            original_name = os.path.splitext(original_filename)[0]

            # Append the file extension to the generated filename
            filename_with_extension = filename + file_extension

            filename_with_extension = 'files/' + filename_with_extension

            # Save the file to disk
            with open(filename_with_extension, 'wb') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)

            out_file = "files/" + str(uuid.uuid4()) 

            if file_extension == ".docx":
                txt = extract_text_from_docx(filename_with_extension)
            else:
                txt = extract_text_from_pdf(filename_with_extension)

            build_embeddings(filename_with_extension)
            generate_pdf(txt, filename_with_extension , out_file)

            summary = txt
            if len(txt) > 10000:
                summary = txt[:10000]

            short_summary = generate_gpt(SHORT_SUMMARY_PROMPT + summary, history=[])
            page_html = out_file + '.html'
            docs = Docs(user=user, name=original_name, original_file=filename_with_extension, file_id = out_file + '.pdf', page_html=page_html,  short_summary=short_summary)
            docs.save()

            return JsonResponse({'filename': filename_with_extension, 'result': 'success'})
        else:
            return JsonResponse({'error': 'No file provided'}, status=400)


import io
class DownloadPDF(View):
    def post(self, request):
        data = json.loads(request.body)
        user_board = Docs.objects.filter(id=data['board_id']).first()
        file_path = user_board.file_id
        with open(file_path, 'rb') as file:
            file_data = file.read()

        # Create an in-memory file-like object
        file_object = io.BytesIO(file_data)

        response = FileResponse(file_object, as_attachment=True, filename=file_path)
        return response
    

class DownloadDOCX(View):
    def post(self, request):
        from .pdf_generator import convert_pdf_to_docx
        data = json.loads(request.body)
        user_board = Docs.objects.filter(id=data['board_id']).first()
        file_path = user_board.file_id
        page_html = user_board.page_html

        # Now the logic to add the missing styles to the docx file
        convert_pdf_to_docx(file_path)
        
        with open('temp.docx', 'rb') as file:
            file_data = file.read()

        file_object = io.BytesIO(file_data)
        response = FileResponse(file_object, as_attachment=True, filename=file_path)
        return response


# Using openai
# async def generate_text(prompt):
#     url = 'https://api.openai.com/v1/engines/davinci-codex/completions'
#     headers = {
#         'Content-Type': 'application/json',
#         'Authorization': f'Bearer {os.environ.get("OPENAI_API")}'
#     }

#     # Define the prompt and parameters for the API request
#     data = {
#         'prompt': prompt,
#         'max_tokens': 64,
#         'temperature': 0.7
#     }

#     # Send the API request and get the response
#     response = requests.post(url, headers=headers, json=data)

#     # Extract the generated text from the response
#     text = response.json()['choices'][0]['text'].strip()
#     return text

