const TelegramBot = require('node-telegram-bot-api');
require('dotenv').config();

// ✅ NEW Telegram bot token from BotFather
const TELEGRAM_TOKEN = "8042508263:AAG1iFBEzqOh-fKz93sVxb8J0LDaQC-5cIk";
const CHAT_ID = process.env.CHAT_ID;

const bot = new TelegramBot(TELEGRAM_TOKEN);

(async () => {
  try {
    console.log("🚀 Bot started");
    console.log("📨 CHAT_ID =", CHAT_ID);

    await bot.sendMessage(CHAT_ID, "✅ Telegram test successful! Racing bot is connected.");
    console.log("✅ Message sent!");
  } catch (error) {
    console.error("❌ Bot error:", error.message);
  }
})();
