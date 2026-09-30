// Quick verification script
const fs = require('fs');
const { ethers } = require('ethers');

try {
  const data = JSON.parse(fs.readFileSync('wallets_600.json', 'utf8'));
  console.log(`Wallets generated: ${data.length}`);
  
  let valid = 0;
  for (const w of data) {
    try {
      const wallet = new ethers.Wallet(w.privateKey);
      if (wallet.address.toLowerCase() === w.address.toLowerCase()) valid++;
    } catch (e) {}
  }
  
  console.log(`Valid wallets: ${valid}/${data.length}`);
  console.log(valid === data.length ? '✅ PASS' : '❌ FAIL');
} catch (err) {
  console.error('Error:', err.message);
  process.exit(1);
}