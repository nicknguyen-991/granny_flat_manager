from django.http import JsonResponse


def health(_request):
    """Lightweight smoke-test endpoint for deploy checks."""
    return JsonResponse({'status': 'ok'})
