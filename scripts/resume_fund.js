// Resume Funding - Continue from where we left off
const { ethers } = require('ethers');
const wallets = require('../wallets_600.json');

const RPC = "https://rpc.testnet.arc.network";
const provider = new ethers.JsonRpcProvider(RPC);
const SEED = "0x9fb95c74f5d3f304ec71f9dac229aeb5f6f5ce40dd49f28e638c771e59cad262";
const wallet = new ethers.Wallet(SEED, provider);

const delay = ms => new Promise(r => setTimeout(r, ms));

async function fund() {
  console.log(`Seed: ${wallet.address}`);
  console.log(`Funding 600 wallets (sequential, 300ms delay)\n`);

  let success = 0;
  for (let i = 0; i < wallets.length; i++) {
    const w = wallets[i];
    try {
      const tx = await wallet.sendTransaction({ to: w.address, value: ethers.parseEther("0.5") });
      await tx.wait();
      success++;
      console.log(`✅ [${i+1}/${wallets.length}] ${tx.hash.slice(0, 12)}...`);
    } catch (e) {
      console.log(`❌ [${i+1}] ${e.message}`);
    }
    await delay(300); // 300ms delay to avoid rate limits
  }
  console.log(`\n🎉 Done! Final fund count: ${success}/${wallets.length}`);
}

fund();