from datetime import date
import enum

from pydantic import BaseModel, Field


class RuleID(str, enum.Enum):
    """
    Перечисление ID правил
    """
    GREETING = 'greeting'
    PARTING = 'parting'
    CAR_BODY = 'car_body'
    CAR_YEAR = 'car_year'
    CAR_MILEAGE = 'car_mileage'
    COMPREHENSIVE_DIAGNOSIS = 'comprehensive_diagnostics'
    PREVIOUS_WORKS = 'previous_works'


class AudioFile(BaseModel):
    """
    Аудиофайлы в Google Drive
    """
    id: str
    name: str
    mimeType: str


class ComplianceChecklist(BaseModel):
    """
    Правила для чек-листа
    """
    id: str
    rule: str


class CheckListItem(BaseModel):
    id: str
    check: bool


class Report(BaseModel):
    """
    Отчет от Gemini
    """
    result: list[CheckListItem] = Field(min_length=len(RuleID))
    appointment: str
    bad_moments: str
    overall: str
    date: date
