import os

# ─── TELEGRAM ───────────────────────────────────────────────────────────────
BOT_TOKEN = os.getenv("BOT_TOKEN")  # token du bot Telegram
ADMIN_ID = 123456789                 # <-- Remplace par ton ID Telegram

# ─── ESSAIS GRATUITS / PREMIUM ──────────────────────────────────────────────
FREE_TRIALS = 10                     # essais gratuits pour chaque nouvel utilisateur

# ─── PAIEMENT TMONEY / MOOV ────────────────────────────────────────────────
PAYMENT_METHOD = "MOOV"              # "TMONEY" ou "MOOV"
PAYMENT_NUMBER = "96XXXXXX"          # ton numéro Moov ou TMONEY
PAYMENT_PRICE = "1000 FCFA"          # montant à payer pour premium
