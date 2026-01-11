import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from crypto_utils import encrypt_message, decrypt_message
from trials import init_db, can_use, consume_trial, set_premium, get_user
from payments import get_tmoney_message, send_payment_proof
from config import ADMIN_ID

# ─── SÉCURITÉ : TOKENS OBLIGATOIRES ─────────────────────────────────────────────
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN manquant (variable d’environnement)")

# ─── INIT ──────────────────────────────────────────────────────────────────────
init_db()
states = {}

# ─── COMMANDES ─────────────────────────────────────────────────────────────────

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔐 Bot de chiffrement AES sécurisé\n\n"
        "Commandes :\n"
        "/encrypt – Chiffrer un message\n"
        "/decrypt – Déchiffrer un message\n"
        "/tries – Essais restants\n"
        "/premium – Accéder au Premium\n\n"
        "🛡️ Aucun message ni mot de passe n’est stocké."
    )

async def tries(update: Update, context: ContextTypes.DEFAULT_TYPE):
    trials, premium = get_user(update.effective_user.id)
    if premium:
        await update.message.reply_text("⭐ Premium actif – accès illimité")
    else:
        await update.message.reply_text(f"📊 Essais restants : {trials}")

# ─── ENCRYPT / DECRYPT ─────────────────────────────────────────────────────────

async def encrypt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    trials, premium = get_user(uid)
    if trials <= 0 and not premium:
        await update.message.reply_text("❌ Essais épuisés. Tapez /premium pour débloquer")
        return
    states[uid] = {"mode": "encrypt", "step": "data"}
    await update.message.reply_text("✏️ Entrez le message à chiffrer")

async def decrypt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    trials, premium = get_user(uid)
    if trials <= 0 and not premium:
        await update.message.reply_text("❌ Essais épuisés. Tapez /premium pour débloquer")
        return
    states[uid] = {"mode": "decrypt", "step": "data"}
    await update.message.reply_text("🔐 Entrez le message chiffré")

# ─── GESTION MESSAGES TEXTE ────────────────────────────────────────────────────

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if uid not in states:
        return

    state = states[uid]

    if state["step"] == "data":
        state["data"] = update.message.text
        state["step"] = "password"
        await update.message.reply_text("🔑 Entrez le mot de passe")
        return

    try:
        if state["mode"] == "encrypt":
            result = encrypt_message(state["data"], update.message.text)
        else:
            result = decrypt_message(state["data"], update.message.text)

        consume_trial(uid)
        await update.message.reply_text(f"✅ Résultat :\n{result}")

    except Exception:
        await update.message.reply_text("❌ Mot de passe incorrect ou message invalide")

    finally:
        del states[uid]

# ─── PAIEMENT PREMIUM TMONEY / MOOV ────────────────────────────────────────────

async def premium(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Affiche les instructions de paiement à l'utilisateur
    """
    uid = update.effective_user.id
    await update.message.reply_text(get_tmoney_message(uid), parse_mode="Markdown")

async def paid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    L'utilisateur envoie la preuve de paiement (texte ou image)
    """
    await send_payment_proof(update, context)

async def validate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Commande admin : /validate <user_id> pour activer premium
    """
    user_id_str = context.args[0] if context.args else None
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ Commande réservée à l'admin")
        return
    if not user_id_str or not user_id_str.isdigit():
        await update.message.reply_text("❌ Usage : /validate <user_id>")
        return

    user_id = int(user_id_str)
    set_premium(user_id)
    await update.message.reply_text(f"✅ Premium activé pour l'utilisateur {user_id}")

# ─── MAIN ──────────────────────────────────────────────────────────────────────

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # commandes utilisateurs
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("encrypt", encrypt))
    app.add_handler(CommandHandler("decrypt", decrypt))
    app.add_handler(CommandHandler("tries", tries))
    app.add_handler(CommandHandler("premium", premium))
    app.add_handler(CommandHandler("paid", paid))

    # commande admin
    app.add_handler(CommandHandler("validate", validate))

    # messages texte (AES)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    app.run_polling()


if __name__ == "__main__":
    main()
