from datetime import datetime

from django.utils import timezone


class ValidationDataError(Exception):
    """
    Кастомное исключение для обработки ошибок валилации запроса в формате JSON
    """
    pass


def validate_alphanumeric_field(field_value, field_name):
    """
    Проверяет, что поле состоит из 2 символов, допустимы только буквы и цифры.
    """
    if field_value and len(field_value) == 2 and field_value.isalnum():
        return field_value.upper()
    raise ValidationDataError(f"{field_name} должна состоять из 2 символов, допустимы только цифры и буквы.")


def validate_datetime_field(field_value, field_name):
    """
    Проверяет, что поле состоит передается в формате YYYY-MM-DD HH:MM:SS
    """
    try:
        # Преобразуем строку в naive datetime
        naive_datetime = datetime.strptime(field_value, "%Y-%m-%d %H:%M:%S")
        
        # Если время naive, делаем его aware, используя текущую временную зону
        aware_datetime = timezone.make_aware(naive_datetime, timezone.get_current_timezone())
        return aware_datetime
        
    except ValueError as exc:
        raise ValidationDataError(f"{field_name} должна быть в формате 'YYYY-MM-DD HH:MM:SS'.") from exc


def process_json_data(data):
    """
    Обработчик данных в формате JSON
    """

    cleaned_data = []
 
    for json_obj in data:
        if len(json_obj) != 3 or not {"model", "version", "created"}.issubset(json_obj.keys()):
            raise ValidationDataError("Неверный формат введенных данных." \
                                      "Ожидаются ключи: 'model', 'version', 'created'.")
    
        cleaned_obj = {
            "model": validate_alphanumeric_field(json_obj.get("model"), "Модель"),
            "version": validate_alphanumeric_field(json_obj.get("version"), "Версия"),
            "created": validate_datetime_field(json_obj.get("created"), "Дата создания")
        }
        
        cleaned_obj["serial"] = f"{cleaned_obj.get('model')}-{cleaned_obj.get('version')}"

        cleaned_data.append(cleaned_obj)
    
    return cleaned_data
