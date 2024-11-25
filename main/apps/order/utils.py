from telegram import Bot
from django.conf import settings



async def send_order_to_telegram(username, order_items_data, total_price):
    bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
    chat_id = settings.TELEGRAM_CHAT_ID

    message = f"Order for {username}\n"
    for item in order_items_data:
        message += f"- {item['menu_item_name']} x {item['quantity']}\n"
    message += f"\nTotal Price: {total_price:.2f} sum"

    await bot.send_message(chat_id=chat_id, text=message)
    return "Order sent to telegram bot successfully!"






