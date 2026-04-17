# 🤖 Telegram Auto-Verification Bot

This bot is designed to **automatically verify new users in a Telegram group**.
New members must click a verification button within a limited time, otherwise they will be **automatically kicked**.

---

## 📌 Features

* Detect new users joining the group
* Send verification button (inline button)
* Time-limited verification (default: 60 seconds)
* Delete messages from unverified users
* Automatically kick users who fail verification
* Simple console logging

---

## 🧠 How It Works

1. A user joins the group
2. Bot listens to `NEW_CHAT_MEMBERS` event
3. Bot:

   * Stores user in `pending_users`
   * Sends a **Verify** button
4. User clicks the button:

   * If within time → added to `verified_users`
   * If expired → ignored
5. While not verified:

   * All messages from the user are deleted
6. If time expires:

   * User is **banned + unbanned** (kick)

---

## ⚙️ Data Structure

```python
pending_users = {
  user_id: {
    "expiry": timestamp,
    "chat_id": chat_id
  }
}

verified_users = set()
```

---

## 🚀 Getting Started

### 1. Install Dependencies

```bash
pip install python-telegram-bot --upgrade
```

---

### 2. Set BOT TOKEN

Update this line:

```python
BOT_TOKEN = ""
```

With your token from BotFather:

```
BOT_TOKEN = "123456:ABC-XYZ..."
```

---

### 3. Run the Bot

```bash
python bot.py
```

---

### 4. Telegram Setup

To make the bot work properly:

* Add the bot to your group
* Promote it to **admin**
* Grant permissions:

  * Delete messages
  * Ban users

---

## 🔄 Event Flow

```
User joins
   ↓
Added to pending_users
   ↓
Bot sends verification button
   ↓
[User clicks]
   ├── Yes → verified_users
   └── No → timeout
                 ↓
               User kicked
```

---

## ⚠️ Important Notes

### 1. Hardcoded `message_thread_id`

```python
message_thread_id=23
```

* Only works for **forum/topic-based groups**
* Remove this parameter if not using topics

---

### 2. Username Can Be None

```python
@{user.username}
```

* Can break if user has no username
* Should fallback to `first_name`

---

### 3. No Data Persistence

* `pending_users` and `verified_users` are in-memory
* All data is lost when the bot restarts

---

### 4. Not Scalable Yet

* Not suitable for large-scale or multi-group usage
* No database integration

---

## ❌ Not Yet Implemented

### 🔴 Persistence (Database)

Missing:

* Redis / MongoDB / PostgreSQL
* Data recovery after restart

---

### 🔴 Advanced Anti-Spam

Currently only:

* Message deletion

Missing:

* Rate limiting
* CAPTCHA verification
* Link filtering

---

### 🔴 Multi-Group Support

* No separation per group
* `pending_users` is global

---

### 🔴 Proper Error Handling

Currently:

```python
print("ERROR:", e)
```

Missing:

* Structured logging
* Retry mechanisms

---

### 🔴 Configurable Settings

Hardcoded values:

```python
expiry = 60
interval = 10
```

Should be:

* Environment variables
* Config files

---

### 🔴 Security Improvements

Missing:

* Strong callback validation
* Protection against spoofed callbacks

---

### 🔴 UX Improvements

Missing:

* Auto-delete verification message after success
* Reminder before timeout
* Better user mention formatting

---

## 💡 Suggested Improvements

* Use Redis for `pending_users`
* Add CAPTCHA (simple math or challenge)
* Move config to environment variables
* Use Python `logging` module
* Support multi-group with:

  ```
  (chat_id, user_id)
  ```

---

## 🧪 Debugging

You can use this helper:

```python
async def debug_all(update, context):
```

It prints:

* Chat ID
* Thread ID
* Message text

---

## 🧩 Future Ideas

* Web dashboard for monitoring
* Verification statistics
* User whitelist
* Membership system integration

---

## 📄 License

Free to use and modify.

---
