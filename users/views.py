from django.shortcuts import render

# Create your views here.
def user_view(request):
    return render(request, 'user_view.html')