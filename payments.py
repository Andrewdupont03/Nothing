from telegram import LabeledPrice
from config import PROVIDER_TOKEN, PRICE_CENTS, CURRENCY

def invoice(chat_id):
    return {
        "chat_id": chat_id,
        "title": "Premium – Chiffrement AES",
        "description": "Accès illimité au chiffrement et déchiffrement sécurisé",
        "payload": "premium_upgrade",
        "provider_token": PROVIDER_TOKEN,
        "currency": CURRENCY,
        "prices": [LabeledPrice("Premium illimité (1 mois)", PRICE_CENTS)],
        "start_parameter": "premium",
    }
