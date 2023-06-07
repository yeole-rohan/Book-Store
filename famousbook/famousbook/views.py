from django.shortcuts import render

def redirect404(request, exception=None):
    print("in 404")
    return render(request, template_name="404.html", context={})