const puppeteer = require('puppeteer');
const { ethers } = require('ethers');
const wallets = require('./wallets_600.json');

const ARC_RPC = "https://rpc.testnet.arc.network";
const provider = new ethers.JsonRpcProvider(ARC_RPC);

async function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

(async () => {
  console.log('🚀 Launch browser...');
  const browser = await puppeteer.launch({
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage', '--disable-gpu']
  });
  const page = await browser.newPage();

  const w = wallets[0];
  console.log(`🧪 Testing Wallet 1: ${w.address}`);

  console.log('🌐 Navigating to flipt.fun...');
  await page.goto('https://testnet.flipt.fun', { waitUntil: 'networkidle2' });
  await delay(3000);

  try {
    // Inject wallet
    await page.evaluateOnNewDocument((pk, addr) => {
      window.__PRIVATE_KEY = pk;
      window.__WALLET_ADDRESS = addr;
    }, w.privateKey, w.address);

    console.log('🔗 Connecting wallet...');
    await page.click('button');
    await delay(2000);

    console.log('💰 Claiming USDC...');
    const btns = await page.$$('button');
    let claimed = false;
    for (const btn of btns) {
      const txtEl = await page.evaluate(el => el.textContent?.toLowerCase().trim(), btn);
      if (txtEl?.includes('claim')) {
        await btn.click();
        claimed = true;
        break;
      }
    }

    if (claimed) {
      console.log('✅ Claim sent!');
      await delay(5000);
    } else {
      console.log('⚠️ No claim button found');
    }

  } catch (err) {
    console.error('❌ Error:', err.message);
  } finally {
    await browser.close();
    console.log('🏁 Test complete!');
  }
})();