const puppeteer = require('puppeteer');
const TelegramBot = require('node-telegram-bot-api');
require('dotenv').config();

const TELEGRAM_TOKEN = "8042508263:AAG1iFBEzqOh-fKz93sVxb8J0LDaQC-5cIk";
const CHAT_ID = process.env.CHAT_ID;

const bot = new TelegramBot(TELEGRAM_TOKEN);

async function scrapeTips() {
  const browser = await puppeteer.launch({
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox'],
  });

  const page = await browser.newPage();
  console.log("🔍 Navigating to AtTheRaces...");
  await page.goto('https://www.attheraces.com/tips', { waitUntil: 'domcontentloaded' });

  console.log("🧪 Scraping tips...");
  const tips = await page.evaluate(() => {
    const tipsList = [];
    document.querySelectorAll('.tips-list .grid-item').forEach((item) => {
      const race = item.querySelector('.meeting-time')?.innerText?.trim();
      const horse = item.querySelector('.runner-name')?.innerText?.trim();
      if (race && horse) {
        tipsList.push(`${race} – ${horse}`);
      }
    });
    return tipsList;
  });

  console.log("✅ Tips scraped:", tips);
  await browser.close();
  return tips;
}

(async () => {
  try {
    const tips = await scrapeTips();

    if (!tips || tips.length === 0) {
      console.log("⚠️ No tips found, sending warning to Telegram...");
      await bot.sendMessage(CHAT_ID, '⚠️ No tips found on At The Races today.');
    } else {
      const message = `🐎 *Today's Racing Tips*\n\n${tips.join('\n')}`;
      console.log("📤 Sending tips to Telegram...");
      await bot.sendMessage(CHAT_ID, message, { parse_mode: 'Markdown' });
    }
  } catch (error) {
    console.error("❌ Bot error:", error.message);
    await bot.sendMessage(CHAT_ID, `❌ Bot error: ${error.message}`);
  }
})();
