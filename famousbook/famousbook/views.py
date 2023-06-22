from django.shortcuts import render

def redirect404(request, exception=None):
    """
    This function handles 404 errors by rendering a custom 404 page.
    @param request - the HTTP request object
    @param exception - the exception that caused the 404 error (optional)
    @return a rendered 404 page
    """
    print("in 404")
    return render(request, template_name="404.html", context={})