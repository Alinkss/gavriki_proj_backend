from django.shortcuts import render
from django.http import JsonResponse
from anti_plag.utils import similarity

def report_view(request):
    if request.method == "POST":
        text = request.POST.get('text', '')

        if not text:
            return JsonResponse({'error': 'No text provided.'}, status=400)
        matches = similarity.report(text)
        
        form_json = [
            {
                'url': url, 'similarity': similarity
            } for url, similarity in matches.items()
        ]
        
        context = {
            'matches': form_json
        }

        return JsonResponse(
                {
                    'matches': form_json
                }
            )

    return JsonResponse({'error': 'Invalid request method.'}, status=405)



# def report_view(request):
#     if request.method == "POST":
#         text = request.POST.get('text', '')

#         if not text:
#             return JsonResponse({'error': 'No text provided.'}, status=400)
#         matches = similarity.report(text)

#         return render(request, 'anti_plag/report.html', {'matches': matches})

#     return render(request, 'anti_plag/report.html', {})
