# payments.py

from telegram import Update
from telegram.ext import ContextTypes
from config import ADMIN_ID, TMONEY_NUMBER, TMONEY_PRICE


def get_tmoney_message(user_id: int) -> str:
    """
    Message affiché à l'utilisateur pour payer via TMONEY / MOOV
    """
    reference = f"TG-{user_id}"

    return (
        "💳 *Paiement Premium via MOOV TMONEY*\n\n"
        f"📱 *Numéro TMONEY* : `{TMONEY_NUMBER}`\n"
        f"💰 *Montant* : `{TMONEY_PRICE}`\n"
        f"📝 *Référence obligatoire* : `{reference}`\n\n"
        "📌 *Procédure*\n"
        "1️⃣ Effectuez le paiement TMONEY\n"
        "2️⃣ Envoyez la *capture d'écran* ou l'*ID de transaction*\n"
        "3️⃣ Tapez la commande `/paid`\n\n"
        "⏳ *Validation manuelle par l’admin*"
    )


async def send_payment_proof(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    L'utilisateur envoie une preuve de paiement (texte ou image)
    """
    user = update.effective_user

    caption = (
        "💳 *Preuve de paiement TMONEY*\n\n"
        f"👤 *User ID* : `{user.id}`\n"
        f"👤 *Username* : @{user.username if user.username else '—'}"
    )

    if update.message.photo:
        photo = update.message.photo[-1]
        await context.bot.send_photo(
            chat_id=ADMIN_ID,
            photo=photo.file_id,
            caption=caption,
            parse_mode="Markdown"
        )
    else:
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=(
                caption +
                f"\n\n📝 *Message* :\n{update.message.text}"
            ),
            parse_mode="Markdown"
        )

    await update.message.reply_text(
        "✅ *Preuve envoyée avec succès.*\n"
        "⏳ En attente de validation par l’admin.",
        parse_mode="Markdown"
    )
