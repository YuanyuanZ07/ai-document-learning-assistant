from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


def health_check(request):
    return JsonResponse({"status": "ok", "message": "Backend is running"})


@csrf_exempt
def upload_file(request):
    if request.method == "POST":
        file = request.FILES.get("file")

        if not file:
            return JsonResponse({"error": "No file uploaded"}, status=400)

        return JsonResponse({
            "message": "File uploaded successfully",
            "filename": file.name,
            "size": file.size
        })

    return JsonResponse({"error": "Invalid request method"}, status=405)


@csrf_exempt
def summary(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            text = data.get("text", "")

            if not text:
                return JsonResponse({"error": "No text provided"}, status=400)

            return JsonResponse({
                "summary": f"Preview: {text[:100]}..."
            })

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)