const puppeteer = require('puppeteer');
const TelegramBot = require('node-telegram-bot-api');

// ✅ YOUR TELEGRAM DETAILS
const TELEGRAM_TOKEN = '6500228396:AAHP-Y-8CIItGiW6w6pK8jl3oJJ0td7mWl8';
const CHAT_ID = '-1002833778838'; // HorsesSignal group

const bot = new TelegramBot(TELEGRAM_TOKEN);

async function scrapeTips() {
    const browser = await puppeteer.launch({ headless: 'new' });
    const page = await browser.newPage();
    await page.goto('https://www.attheraces.com/tips', { waitUntil: 'domcontentloaded' });

    const tips = await page.evaluate(() => {
        const tipsList = [];
        document.querySelectorAll('.tips-list .grid-item').forEach(item => {
            const race = item.querySelector('.meeting-time')?.innerText?.trim();
            const horse = item.querySelector('.runner-name')?.innerText?.trim();
            if (race && horse) {
                tipsList.push(`${race} – ${horse}`);
            }
        });
        return tipsList;
    });

    await browser.close();
    return tips;
}

(async () => {
    try {
        const tips = await scrapeTips();
        if (tips.length === 0) {
            await bot.sendMessage(CHAT_ID, "⚠️ No tips found today.");
        } else {
            const message = `🐎 *Today's Racing Tips*\n\n${tips.join('\n')}`;
            await bot.sendMessage(CHAT_ID, message, { parse_mode: 'Markdown' });
        }
    } catch (err) {
        console.error(err);
        await bot.sendMessage(CHAT_ID, `❌ Error scraping tips: ${err.message}`);
    }
})();
