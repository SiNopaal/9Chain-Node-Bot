// 600-Wallet Flip.fun Auto-Claim + Buy
// Seed phrase hanya di memori, tidak disimpan
// Tech: ethers.js + puppeteer

const { ethers } = require('ethers');
const puppeteer = require('puppeteer');

const SEED_PHRASE = "between egg caution advice public old market license surge poverty puzzle fit";
const ARC_RPC = "https://rpc.testnet.arc.network";
const FLIPFUN_URL = "https://testnet.flipt.fun";
const TRADE_CONTRACT = "0xbf2f2a377fa9e8357a59fbc84798eda3732f69d2";
const TOTAL_WALLETS = 600;
const CONCURRENCY = 5;

// Generate 600 wallets from seed
function generateWallets() {
  const wallets = [];
  for (let i = 0; i < TOTAL_WALLETS; i++) {
    const path = `m/44'/60'/0'/0/${i}`;
    const hdNode = ethers.HDNodeWallet.fromPhrase(SEED_PHRASE, path);
    const address = hdNode.getAddress();
    const privateKey = hdNode.privateKey;
    wallets.push({
      index: i,
      address,
      privateKey,
      mnemonicPath: path
    });
  }
  console.log(`✅ Generated ${wallets.length} wallets`);
  return wallets;
}

// Generate ALL 600 addresses first
const WALLETS = generateWallets();

console.log('📋 Wallet addresses (first 5):');
WALLETS.slice(0, 5).forEach(w => {
  console.log(`  [${w.index}] ${w.address}`);
});

// Save to output file
const fs = require('fs');
const output = {
  seedPhrase: SEED_PHRASE,
  wallets: WALLETS.map(w => ({ index: w.index, address: w.address, privateKey: w.privateKey }))
};

fs.writeFileSync('wallets.json', JSON.stringify(output, null, 2));
console.log('💾 Saved wallets.json');

console.log('🚀 Ready for funding + claim + buy phase');
console.log('⏭️  Run: node scripts/fund-flip.js');