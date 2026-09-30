// Funding 0.5 USDC to 600 wallets

const { ethers } = require('ethers');
const wallets = require('../wallets_600.json');

const PRIVATE_KEY = "0x9fb95c74f5d3f304ec71f9dac229aeb5f6f5ce40dd49f28e638c771e59cad262";
const ARC_RPC = "https://rpc.testnet.arc.network";
const provider = new ethers.JsonRpcProvider(ARC_RPC);
const SENDER = new ethers.Wallet(PRIVATE_KEY, provider);

async function fund() {
  console.log(`Funding 0.5 USDC to ${wallets.length} wallets...`);
  for (const [i, w] of wallets.entries()) {
    try {
      const tx = await SENDER.sendTransaction({ to: w.address, value: ethers.parseUnits("0.5", 18) });
      console.log(`[${i+1}] ✅ ${tx.hash.substring(0,12)}...`);
    } catch (e) {
      console.error(`[${i+1}] ❌ ${e.message}`);
    }
  }
  console.log("Done!");
}

fund().catch(console.error);