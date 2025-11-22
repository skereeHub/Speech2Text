import json

from google import genai
from google.genai.types import Schema, Type, GenerateContentConfig

from pydantic import BaseModel

from speech2text.src.config import GeminiConfig


class ComplianceChecklist(BaseModel):
    id: str
    rule: str


class GeminiClient:
    MODEL = 'gemini-2.5-flash'

    COMPLIANCE_CHECKLIST: list[ComplianceChecklist] = [
        ComplianceChecklist(id='greeting', rule='Менеджер розпочав розмову з чіткого привітання'),
        ComplianceChecklist(id='parting', rule='Розмова була завершена чітким прощанням'),
    ]

    JSON_OUTPUT_SHEMA = Schema(
        type=Type.OBJECT,
        properties={
            'result': Schema(
                type=Type.ARRAY,
                description='Результати перевірки кожного пункту чек-листу',
                items=Schema(
                    type=Type.OBJECT,
                    properties={
                        'id': Schema(type=Type.STRING, description='ID правила з чек-листа'),
                        'check': Schema(type=Type.BOOLEAN, description='Чи виконано правило'),
                    },
                    required=['id', 'check']
                )
            ),
            'overall': Schema(
                type=Type.STRING,
                description='Коротке резюме щодо цієї розмови'
            )
        },
        required=['result', 'overall']
    )

    def __init__(self):
        self.client = genai.Client(api_key=GeminiConfig().api_key)
        self.system_prompt = self._create_system_prompt()

    @staticmethod
    def _create_system_prompt():
        rules = '\n'.join(
            [
                f'- ID: {item.id} | Правило: {item.rule}'
                for item in GeminiClient.COMPLIANCE_CHECKLIST
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
