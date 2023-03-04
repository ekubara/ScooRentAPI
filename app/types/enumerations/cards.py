from enum import Enum


class Banks(str, Enum):
    POCHTABANK = "Почтабанк"
    SBERBANK = "Сбербанк"
    SOVKOMBANK = "Совкомбанк"
    TINKOFF = "Тинькофф"
    VTB = "ВТБ"
