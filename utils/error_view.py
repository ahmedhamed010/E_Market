from django.http import JsonResponse

        # لو خطا من المستخدم 
def handler404(request , exception):
    message = ('Path Not Found')
    response = JsonResponse(data={'error':message})
    response.status_code = 404
    return response


        # لو خطا من السيرفير 
def handler500(request):
    message = ('Internal Server Error')
    response = JsonResponse(data={'error':message})
    response.status_code = 500
    return response