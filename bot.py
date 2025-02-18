import asyncio
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import telegram
from telegram.ext import Application, CommandHandler, ContextTypes

# Telegram Bot Token (Replace with your bot token)
BOT_TOKEN = "7425768644:AAFXsJpW7rhF5ax9-QDVs0hFV_HLFWdhB9k"
CHAT_ID = "6483303120"

async def send_telegram_message(message):
    try:
        bot = telegram.Bot(token=BOT_TOKEN)
        await bot.send_message(chat_id=CHAT_ID, text=message)
        print(f"Message sent: {message}")  # Debug message
    except Exception as e:
        print(f"Error sending message: {e}")  # Debug error

async def check_al_ahly_tickets(context: ContextTypes.DEFAULT_TYPE):
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    
    try:
        while True:
            driver.get("https://www.tazkarti.com/#/matches")
            time.sleep(5)  # Wait for the page to load
            
            # Debug: Print current URL
            print(f"Current URL: {driver.current_url}")
            
            matches = driver.find_elements(By.CSS_SELECTOR, "div")  # Adjust selector if needed
            print(f"Found {len(matches)} matches.")  # Debug: Print number of matches found
            
            for match in matches:
                print(f"Checking match: {match.text}")  # Debug: Print match details
                
                if "Al Ahly FC" in match.text:
                    print("Match found! Sending message...")  # Debug: Match found
                    await send_telegram_message("🎟️ Al Ahly tickets are available! Check Tazkarti now: https://www.tazkarti.com/#/matches")
                    driver.quit()
                    return
            else:
                print("No match found. Will check again later...")  # Debug: No match found
                await asyncio.sleep(200)  # Wait for 5 minutes before checking again
                driver.refresh()
    
    finally:
        driver.quit()

async def start(update, context):
    print("Received /start command")  # Debug: Received /start command
    await update.message.reply_text("Bot started! Checking for Al Ahly tickets...")
    print("Bot started. Checking for Al Ahly tickets...")  # Debug message
    await check_al_ahly_tickets(context)

def main():
    application = Application.builder().token(BOT_TOKEN).build()

    # Add a command handler
    application.add_handler(CommandHandler("start", start))

    # Run the bot
    print("Bot is running...")  # Debug: Bot is running
    application.run_polling()

if __name__ == "__main__":
    main()
