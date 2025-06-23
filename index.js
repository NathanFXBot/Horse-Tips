const TelegramBot = require('node-telegram-bot-api');
require('dotenv').config();

// ✅ Hardcoded token to bypass newline issues
const TELEGRAM_TOKEN =
  "6500228396:" +
  "AAHP-Y-8CIItGiW6w6pK8jl3o" +
  "JJ0td7mWl8";

const CHAT_ID = process.env.CHAT_ID;

const bot = new TelegramBot(TELEGRAM_TOKEN);

(async () => {
  try {
    console.log("📤 Sending test message...");
    await bot.sendMessage(CHAT_ID, "✅ Telegram test successful! Racing bot is connected.");
    console.log("✅ Message sent!");
  } catch (error) {
    console.error("❌ Bot error:", error.message);
  }
})();
