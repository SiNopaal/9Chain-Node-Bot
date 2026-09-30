const puppeteer = require('puppeteer');
const wallets = require('../wallets_600.json');

const sleep = ms => new Promise(r => setTimeout(r, ms));

(async () => {
  console.log('🚀 Launch browser...');
  const browser = await puppeteer.launch({
    headless: true,
    args: [
      '--no-sandbox',
      '--disable-setuid-sandbox',
      '--disable-dev-shm-usage',
      '--disable-gpu',
      '--disable-web-security',
      '--window-size=1920,1080',
      '--single-process'
    ],
    ignoreHTTPSErrors: true
  });
  const page = await browser.newPage();
  await page.setViewport({ width: 1920, height: 1080 });
  await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36');

  console.log('🌐 Navigating to flipt.fun...');
  await page.goto('https://testnet.flipt.fun', { waitUntil: 'networkidle2', timeout: 60000 });

  await sleep(3000);

  for (let i = 0; i < Math.min(wallets.length, 5); i++) { // Test dengan 5 wallet dulu
    const w = wallets[i];
    try {
      console.log(`[${w.index}] Processing ${w.address.slice(0,10)}...`);

      await page.goto('https://testnet.flipt.fun', { waitUntil: 'networkidle2', timeout: 30000 });
      await sleep(2000);

      // Click connect wallet
      const connectBtn = await page.$('button:has-text("Connect")');
      if (connectBtn) await connectBtn.click();
      await sleep(3000);

      // Inject private key
      const pkInput = await page.$('textarea, input[type="password"]');
      if (pkInput) await pkInput.type(w.privateKey);
      await sleep(1000);

      const importBtn = await page.$('button:has-text("Import")');
      if (importBtn) await importBtn.click();
      await sleep(5000);

      // Claim USDC
      const claimBtn = await page.$('button:has-text("Claim")');
      if (claimBtn) await claimBtn.click();
      console.log(`[${w.index}] ✅ Claim sent`);
      await sleep(5000);

      // Go to trade page
      await page.goto(`https://testnet.flipt.fun/trade/0xbf2f2a377fa9e8357a59fbc84798eda3732f69d2/`, { waitUntil: 'networkidle2', timeout: 30000 });
      await sleep(3000);

      // Buy loop
      let spent = 0;
      while (spent < 500000) {
        const amt = Math.floor(Math.random() * (100000 - 50000 + 1)) + 50000;
        const rem = 500000 - spent;
        const amount = Math.min(amt, rem);

        const input = await page.$('input[type="number"]');
        if (input) await input.type(amount.toString());
        await sleep(500);

        const buyBtn = await page.$('button:has-text("Buy")');
        if (buyBtn) await buyBtn.click();
        await sleep(4000);

        spent += amount;
        console.log(`[${w.index}] 💰 Bought ${amount} | Total: ${spent}/500000`);
      }

    } catch (err) {
      console.error(`[${w.index}] Error: ${err.message}`);
    }
    await sleep(2000); // Buffer between wallets
  }

  await browser.close();
  console.log('✅ Test batch complete!');
})();