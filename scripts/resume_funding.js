// Resume Funding Script - Only processes wallets without confirmed funding
const { ethers } = require('ethers');
const fs = require('fs');

const RPC = "https://rpc.testnet.arc.network";
const provider = new ethers.JsonRpcProvider(RPC);
const SEED_PK = "0x9fb95c74f5d3f304ec71f9dac229aeb5f6f5ce40dd49f28e638c771e59cad262";
const seedWallet = new ethers.Wallet(SEED_PK, provider);

const delay = (ms) => new Promise(r => setTimeout(r, ms));

async function checkBalance(addr) {
  try {
    const balance = await provider.getBalance(addr);
    return balance >= ethers.parseEther("0.49"); // Allow small margin
  } catch {
    return false;
  }
}

async function main() {
  const wallets = JSON.parse(fs.readFileSync('../wallets_600.json'));
  const completed = JSON.parse(fs.readFileSync('../funding_progress.json') || '[]');

  console.log(`Seed wallet: ${seedWallet.address}`);
  console.log(`Wallets to process: ${wallets.length - completed.length}\n`);

  const pending = wallets.filter(w => !completed.find(c => c.index === w.index));

  for (const w of pending) {
    try {
      const hasFunds = await checkBalance(w.address);
      if (hasFunds) {
        console.log(`⏭️ [${w.index+1}] Already funded - skipping`);
        completed.push({ index: w.index, address: w.address, skipped: true });
        continue;
      }

      console.log(`🔄 [${w.index+1}] Funding 0.5 USDC → ${w.address.slice(0,10)}...`);
      const tx = await seedWallet.sendTransaction({ to: w.address, value: ethers.parseEther("0.5") });
      await tx.wait();
      console.log(`✅ [${w.index+1}] TX: ${tx.hash.slice(0,16)}...`);

      completed.push({ index: w.index, address: w.address, txHash: tx.hash });
      fs.writeFileSync('../funding_progress.json', JSON.stringify(completed, null, 2));

    } catch (err) {
      console.error(`❌ [${w.index+1}] ${err.message}`);
    }
    await delay(1000); // 1s delay to avoid overwhelming RPC
  }

  console.log(`\n🎉 Done! Total funded: ${completed.filter(c => !c.skipped).length}`);
}

main().catch(console.error);