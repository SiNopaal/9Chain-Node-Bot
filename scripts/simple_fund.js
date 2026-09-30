// Simple Sequential Funding - One wallet at a time with retry
const { ethers } = require('ethers');
const wallets = require('../wallets_600.json');
const fs = require('fs');

const RPC = "https://rpc.testnet.arc.network";
const provider = new ethers.JsonRpcProvider(RPC);
const SEED = "0x9fb95c74f5d3f304ec71f9dac229aeb5f6f5ce40dd49f28e638c771e59cad262";
const wallet = new ethers.Wallet(SEED, provider);

const DELAY_MS = 600;
const MAX_RETRIES = 3;

async function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

async function fund() {
  console.log(`Seed: ${wallet.address}`);
  console.log(`Funding ${wallets.length} wallets...\n`);

  let success = 0;
  for (let i = 0; i < wallets.length; i++) {
    const w = wallets[i];
    for (let retry = 0; retry < MAX_RETRIES; retry++) {
      try {
        const tx = await wallet.sendTransaction({ to: w.address, value: ethers.parseEther("0.5") });
        await tx.wait();
        success++;
        process.stdout.write(`✅ [${i+1}/600] ${tx.hash.slice(0,10)}... | Balance: ~${((300-success*0.5)).toFixed(1)} USDC left\r`);
        break;
      } catch (e) {
        if (retry === MAX_RETRIES - 1) console.log(`❌ [${i+1}] ${e.message}`);
        else await sleep(DELAY_MS * 2);
      }
    }
    await sleep(DELAY_MS);
  }
  console.log(`\n\n🎉 Done! Funded ${success}/600 wallets`);
}

fund();