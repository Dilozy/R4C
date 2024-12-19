from django.http import JsonResponse
from django.http import FileResponse

from .services import create_weekly_report


def download_excel_report(request):
    create_weekly_report()

    file_path = "robots/media/weekly_report.xlsx"

    if not file_path:
        return JsonResponse({"error": "File not found"})

    response = FileResponse(open(file_path, "rb"), as_attachment=True)
    return response
