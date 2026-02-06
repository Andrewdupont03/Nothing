# 🔐 Bot Telegram – Chiffrement AES sécurisé avec paiement Moov/TMONEY

Bot Telegram qui permet de :

* Chiffrer et déchiffrer des messages via AES
* Essais gratuits limités
* Déblocage premium via paiement manuel Moov ou TMONEY
* Validation manuelle des paiements par l’admin

---

## 📂 Structure du projet

```
bot/
├── main.py           # logique principale du bot
├── crypto_utils.py   # fonctions de chiffrement/déchiffrement AES
├── trials.py         # gestion des essais gratuits et du premium
├── payments.py       # génération message paiement et envoi preuve
├── config.py         # configuration du bot (tokens, admin, paiement)
├── database.db       # base SQLite (utilisateurs, essais, premium)
└── requirements.txt  # dépendances Python
```

---

## ⚙️ Installation

1. Cloner le repo :

```bash
git clone https://github.com/TON_USERNAME/TON_BOT.git
cd TON_BOT
```

2. Installer les dépendances :

```bash
pip install -r requirements.txt
```

3. Remplir `config.py` :

```python
BOT_TOKEN = os.getenv("BOT_TOKEN")      # token du bot Telegram
ADMIN_ID = 123456789                     # ton ID Telegram
FREE_TRIALS = 10                         # essais gratuits

PAYMENT_METHOD = "MOOV"                  # "TMONEY" ou "MOOV"
PAYMENT_NUMBER = "96XXXXXX"              # ton numéro Moov / TMONEY
PAYMENT_PRICE = "1000 FCFA"              # prix premium
```

> 💡 Comme tu ne veux pas de `.env`, tu peux mettre `BOT_TOKEN` directement sur ton serveur via **Railway / Oracle Cloud variables d’environnement**.

---

## 💬 Commandes du bot

### Utilisateur

| Commande   | Fonction                                         |
| ---------- | ------------------------------------------------ |
| `/start`   | Message de bienvenue + instructions              |
| `/encrypt` | Chiffrer un message AES (demande mot de passe)   |
| `/decrypt` | Déchiffrer un message AES (demande mot de passe) |
| `/tries`   | Affiche le nombre d’essais gratuits restants     |
| `/premium` | Instructions pour payer via Moov/TMONEY          |
| `/paid`    | Envoyer la preuve de paiement (photo ou texte)   |

> Si essais gratuits = 0 et pas premium → `/encrypt` et `/decrypt` bloqués

---

### Admin

| Commande              | Fonction                                |
| --------------------- | --------------------------------------- |
| `/validate <user_id>` | Débloque le premium pour un utilisateur |

> L’admin reçoit toutes les preuves envoyées via `/paid`

---

## 🔐 Paiement Moov/TMONEY

1. L’utilisateur tape `/premium`
2. Le bot affiche :

   * Numéro Moov/TMONEY
   * Montant
   * Référence unique (ex: `TG-123456`)
3. L’utilisateur effectue le paiement
4. L’utilisateur envoie la preuve via `/paid`
5. L’admin valide avec `/validate <user_id>` → premium activé

> ⚠️ Le bot **ne manipule pas l’argent**. Tout est manuel et sécurisé.

---

## 💾 Base de données

* Fichier SQLite : `database.db`
* Table `users` :

| Colonne | Type    | Description                  |
| ------- | ------- | ---------------------------- |
| user_id | INTEGER | ID Telegram de l’utilisateur |
| trials  | INTEGER | Essais gratuits restants     |
| premium | INTEGER | 0 = non premium, 1 = premium |

---

## 🖥 Déploiement sur serveur gratuit (ex : Railway)

1. Créer un projet Railway
2. Déployer le repo GitHub
3. Ajouter les variables d’environnement :

   * `BOT_TOKEN`
   * `ADMIN_ID`
4. Le bot est prêt, aucun `.env` nécessaire

---

## ⚡ Exécution locale

```bash
python main.py
```

* Testez `/start`, `/encrypt`, `/decrypt`, `/tries`, `/premium`, `/paid`
* `/validate <user_id>` fonctionne uniquement si vous êtes admin

---

## 📌 Points importants

* Chiffrement AES sécurisé
* Essais gratuits limités
* Paiement manuel Moov/TMONEY
* Aucun mot de passe ou message stocké sur le serveur
* Validation premium 100% sous contrôle admin

---

## 🧰 Dépendances (`requirements.txt`)

```
python-telegram-bot==20.3
cryptography==41.0.3
```
