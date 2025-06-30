from django.shortcuts import render

#Test Chat Features
def test(request):
    return render(request, 'chat/chattest.html')
