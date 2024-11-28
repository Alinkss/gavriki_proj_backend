from django.shortcuts import render
from django.http import JsonResponse
from anti_plag.utils import similarity
import openai
from django.conf import settings
from anti_plag.forms import TextForm
import requests
from anti_plag.utils.similarity import generate_report
import json

openai.api_key = settings.OPENAI_API_KEY

def correct_text(text):
    response = openai.ChatCompletion.create(  
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a text correction assistant that suggests grammar, spelling, and stylistic improvements in the Ukrainian language."},
            {"role": "user", "content": f"Please correct the following Ukrainian text by fixing any grammar, spelling, or stylistic mistakes: {text}"}
        ],
        max_tokens=500
    )
    
    corrected_text = response['choices'][0]['message']['content'].strip()
    return corrected_text

def analysis_text(request):
    result = None
    sentences = []
    if request.method == 'POST':
        text_form = TextForm(request.POST)
        if text_form.is_valid():
            text = text_form.cleaned_data['text']
            
            changed_text = correct_text(text)
            
            result = {
                'original_text': text,
                'changed_text': changed_text
            }
            
            origin_sentences = text.split(". ")
            changed_sentences = changed_text.split(". ")
            
            for original, changed in zip(origin_sentences, changed_sentences):
                sentences.append(
                    {
                        'original_sentence': original.strip() + ".",
                        'corrected_sentence': changed.strip() + "."
                    }
                )
        return JsonResponse( {
            'success': True,
            'result': result,
            'sentences': sentences
        })
    else:
        text_form = TextForm()
            
    return JsonResponse({
        'success': False,
        'message': 'Invalid request method or form not valid.'
    })

# def analysis_text(request):
#     result = None
#     if request.method == 'POST':
#         text_form = TextForm(request.POST)
#         if text_form.is_valid():
#             text = text_form.cleaned_data['text']
            
#             result = correct_text(text)
#     else:
#         text_form = TextForm()
    
#     context = {
#         'text_form': text_form,
#         'result': result,
#     }
            
#     return render(request, 'anti_plag/text_analysis.html', context)


# def report_view(request):
#     if request.method == "POST":
#         text = request.POST.get('text', '')
#         language = request.POST.get('language', 'english') 

#         if not text:
#             if request.headers.get('Accept') == 'application/json':
#                 return JsonResponse({'error': 'No text provided.'}, status=400)
#             return render(request, 'anti_plag/report.html', {'error': 'Please provide text for analysis.'})

#         matches = generate_report(text, language)

#         form_json = [
#             {
#                 'url': url,
#                 'similarity': similarity,
#             } for url, similarity in matches.items()
#         ]


#         if request.headers.get('Accept') == 'application/json':
#             return JsonResponse({'matches': form_json})

#         context = {
#             'matches': form_json,
#         }
#         return render(request, 'anti_plag/report.html', context)

#     return render(request, 'anti_plag/report.html')

def report_view(request):
    if request.method == "POST":
        text = request.POST.get('text', '')
        language = request.POST.get('language', 'english') 

        if not text:
            return JsonResponse({'error': 'No text provided.'}, status=400)

        matches = generate_report(text, language)
        
        if len(matches) == 0:
            form_json = [
                {
                    'url': 'No matches found.',
                    'similarity': 0,
                }
            ]
        else:
            form_json = [
                {
                    'url': url,
                    'similarity': round(min(similarity * 100, 100), 2),
                } for url, similarity in matches.items()
            ]

        return JsonResponse({'matches': form_json})

    return JsonResponse({'error': 'Invalid request method.'}, status=405)