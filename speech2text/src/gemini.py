import json

from google import genai
from google.genai.types import Schema, Type, GenerateContentConfig

from speech2text.src.config import GeminiConfig
from speech2text.src.models import RuleID, ComplianceChecklist


class GeminiClient:
    """
    Клиент для работы с Gemini API для анализа текста
    """
    MODEL = 'gemini-2.5-flash'

    # Чек-лист правил для проверки
    COMPLIANCE_CHECKLIST: list[ComplianceChecklist] = [
        ComplianceChecklist(id=RuleID.GREETING, rule='Менеджер розпочав розмову з чіткого привітання.'),
        ComplianceChecklist(id=RuleID.PARTING, rule='Розмова була завершена чітким прощанням.'),
        ComplianceChecklist(id=RuleID.CAR_BODY, rule='Менеджер дізнався кузов автомобіля.'),
        ComplianceChecklist(id=RuleID.CAR_YEAR, rule='Менеджер дізнався рік автомобіля.'),
        ComplianceChecklist(id=RuleID.CAR_MILEAGE, rule='Менеджер дізнався пробіг автомобіля.'),
        ComplianceChecklist(id=RuleID.COMPREHENSIVE_DIAGNOSIS, rule='Менеджер зробив пропозицію комплексної діагностики автомобіля.'),
        ComplianceChecklist(id=RuleID.PREVIOUS_WORKS, rule='Менеджер дізнався, які роботи з автомобілем проводились раніше.'),
    ]

    # Выходная схема JSON формата, которую мы получаем в ответе от Gemini
    JSON_OUTPUT_SHEMA = Schema(
        type=Type.OBJECT,
        properties={
            'result': Schema(
                type=Type.ARRAY,
                description='Результати перевірки кожного пункту чек-листу.',
                items=Schema(
                    type=Type.OBJECT,
                    properties={
                        'id': Schema(type=Type.STRING, description='ID правила з чек-листа.'),
                        'check': Schema(type=Type.BOOLEAN, description='Чи виконано правило.'),
                    },
                    required=['id', 'check']
                )
            ),
            'appointment': Schema(
                type=Type.STRING,
                description='Дата та час запису, якщо менеджер домовився. Якщо запису немає, залишити порожній рядок.'
            ),
            'bad_moments': Schema(
                type=Type.STRING,
                description='Виділити дуже критичні моменти діалогу з клієнтом (наприклад: грубість, неточність, довгі паузи), пропускаючи мілкі недоліки'
            ),
            'overall': Schema(
                type=Type.STRING,
                description='Коротке резюме щодо цієї розмови та загальний висновок щодо якості.'
            )
        },
        required=['result', 'appointment', 'bad_moments', 'overall']
    )

    def __init__(self):
        self.client = genai.Client(api_key=GeminiConfig().api_key)
        self.system_prompt = self._create_system_prompt()

    @staticmethod
    def _create_system_prompt():
        rules = '\n'.join(
            [
                f'- ID: {check.id} | Правило: {check.rule}'
                for check in GeminiClient.COMPLIANCE_CHECKLIST
            ]
        )

        return (
            'Ви - HR-аудитор. Ваше завдання - оцінити розмову менеджера з продажу/підтримки з клієнтом відповідно до внутрішнього чек-листа.'
            'Ви повинні проаналізувати наданий текст і повернути результат у форматі JSON, який ТОЧНО відповідає наданій схемі.'
            '--- ЧЕК-ЛИСТ ---'
            f'{rules}'
        )

    def analyze_dialogue(self, content: str) -> dict:
        config = GenerateContentConfig(
            system_instruction=self.system_prompt,
            response_mime_type='application/json',
            response_schema=GeminiClient.JSON_OUTPUT_SHEMA,
            temperature=0.0
        )
        prompt = (
            'Проаналізуй наступну розмову менеджера та клієнта, застосовуючи наданий чек-лист.'
            f'\n\n{content}'
        )

        response = self.client.models.generate_content(
            model=GeminiClient.MODEL,
            contents=prompt,
            config=config
        )

        return json.loads(response.text)
