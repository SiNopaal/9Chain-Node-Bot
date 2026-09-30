// Direct Funding Script - Sends 0.5 USDC to 600 wallets
// Uses raw transaction signing to avoid ethers estimation issues
const { ethers } = require('ethers');
const wallets = require('../wallets_600.json');
const fs = require('fs');

const RPC = "https://rpc.testnet.arc.network";
const provider = new ethers.JsonRpcProvider(RPC);
const SEED = "0x9fb95c74f5d3f304ec71f9dac229aeb5f6f5ce40dd49f28e638c771e59cad262";
const wallet = new ethers.Wallet(SEED, provider);

const delay = ms => new Promise(r => setTimeout(r, ms));

async function fundAll() {
  console.log(`📡 Seed: ${wallet.address}`);
  console.log(`Funding ${wallets.length} wallets...\n`);

  const results = [];
  for (let i = 0; i < wallets.length; i++) {
    const w = wallets[i];
    try {
      // Use raw transaction with fixed gas price to avoid estimation issues
      const tx = await wallet.sendTransaction({
        to: w.address,
        value: ethers.parseEther("0.5"),
        gasLimit: 21000,
        gasPrice: 20477218923n
      });
      const receipt = await tx.wait();
      console.log(`✅ [${i+1}/600] ${tx.hash.slice(0,16)}... confirmed`);
      results.push({ index: i, txHash: tx.hash, status: "confirmed" });
    } catch (err) {
      console.log(`❌ [${i+1}] ${err.message.split(' ')[0]}`);
      results.push({ index: i, error: err.message });
    }
    await delay(600); // 600ms delay to prevent rate limits
  }

  const success = results.filter(r => r.status === "confirmed").length;
  console.log(`\n🎉 FINISH! Funded ${success}/${wallets.length}`);
  fs.writeFileSync('../funding_proof.json', JSON.stringify({
    seed: wallet.address,
    success,
    total: wallets.length,
    results: results
  }, null, 2));
  console.log("💾 Proof saved to funding_proof.json");
}

fundAll().catch(console.error);