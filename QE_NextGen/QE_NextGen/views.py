from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django import forms



def home(request):
    try:
        print("Request method:", request.method) 
        code_or_url = "URL"  # This should be set based on some logic or input
        
        if code_or_url == "URL":
            print("url")
            # Perform URL-specific logic here
            return JsonResponse({'message': 'URL processing completed successfully'})
        
        elif code_or_url == "DOM structure":
            print("Dom")
            # Perform DOM-specific logic here
            return JsonResponse({'message': 'DOM structure processing completed successfully'})
        
        else:
            # Handle unexpected values
            return JsonResponse({'error': 'Invalid value for code_or_url'}, status=400)
    
    except Exception as e:
        # Handle any exceptions that occur
        print("An error occurred:", str(e))
        return JsonResponse({'error': 'An error occurred: ' + str(e)}, status=500)

        
   