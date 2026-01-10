import os

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
    PreCheckoutQueryHandler,
)

from crypto_utils import encrypt_message, decrypt_message
from trials import (
    init_db,
    can_use,
    consume_trial,
    set_premium,
    get_user,
)
from payments import invoice

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
        "/upgrade – Passer Premium\n\n"
        "🛡️ Aucun message ni mot de passe n’est stocké."
    )

async def tries(update: Update, context: ContextTypes.DEFAULT_TYPE):
    trials, premium = get_user(update.effective_user.id)
    if premium:
        await update.message.reply_text("⭐ Premium actif – accès illimité")
    else:
        await update.message.reply_text(f"📊 Essais restants : {trials}")

async def encrypt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if not can_use(uid):
        await update.message.reply_text("❌ Essais épuisés. /upgrade")
        return
    states[uid] = {"mode": "encrypt", "step": "data"}
    await update.message.reply_text("✏️ Entrez le message à chiffrer")

async def decrypt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if not can_use(uid):
        await update.message.reply_text("❌ Essais épuisés. /upgrade")
        return
    states[uid] = {"mode": "decrypt", "step": "data"}
    await update.message.reply_text("🔐 Entrez le message chiffré")

# ─── MESSAGES TEXTE ────────────────────────────────────────────────────────────

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

# ─── PAIEMENT ──────────────────────────────────────────────────────────────────

async def upgrade(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_invoice(**invoice(update.effective_chat.id))

async def precheckout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.pre_checkout_query.answer(ok=True)

async def successful_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    set_premium(update.effective_user.id)
    await update.message.reply_text("✅ Premium activé. Merci 🔐")

# ─── MAIN ──────────────────────────────────────────────────────────────────────

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("encrypt", encrypt))
    app.add_handler(CommandHandler("decrypt", decrypt))
    app.add_handler(CommandHandler("tries", tries))
    app.add_handler(CommandHandler("upgrade", upgrade))

    app.add_handler(PreCheckoutQueryHandler(precheckout))
    app.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, successful_payment))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    app.run_polling()

if __name__ == "__main__":
    main()
