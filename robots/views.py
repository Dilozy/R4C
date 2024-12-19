import json

from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from .services import process_json_data, ValidationDataError
from .models import Robot


@method_decorator(csrf_exempt, name="dispatch")
class AddRobotAPI(View):
    """
    Класс, реализующий API endpoint для добавления нового робота
   
    В связи с тем, что при всех POST запросах Django требует csrf-токен, а в нашем случае запрос
    делается не через формы, то было решено отключить валидацию через csrf-токен
    В теории для валидации можно создать собственный токен для каждого пользователя и хранить его в кэше
    Тогда можно будет не опасаться csrf-атак даже без csrf-токена
    """
    
    def post(self, request, *args, **kwargs):
        """
        Метод для обработки данных, пришедеших через HTTP метод POST
        """
        data = json.loads(request.body)
        
        try:
            cleaned_data = process_json_data(data)
        except ValidationDataError as exc:
            return JsonResponse({"status": "error", "message": str(exc)})

        for json_obj in cleaned_data:
            Robot.objects.create(**json_obj)
        
        return JsonResponse({"status": "sucess", "message": "Новый робот(ы) был(и) успешно добавлен(ы)"})
