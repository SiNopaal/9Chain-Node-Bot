// Direct Flipt.fun Claim + Buy - No Browser
const { ethers } = require('ethers');
const wallets = require('../wallets_600.json');

const RPC = "https://rpc.testnet.arc.network";
const provider = new ethers.JsonRpcProvider(RPC);
const CONTRACT = "0xbf2f2a377fa9e8357a59fbc84798eda3732f69d2";
const ABI = [
  "function claimTokens() external",
  "function swapExactTokensForTokens(uint256 amountIn, uint256 amountOutMin, address[] calldata path, address to, uint256 deadline) external returns (uint256[] memory amounts)",
  "function balanceOf(address) view returns (uint256)"
];

async function main() {
  console.log('🚀 Direct Claim + Buy 600 wallets\n');
  
  const results = [];
  for (let i = 0; i < wallets.length; i++) {
    const w = wallets[i];
    try {
      const signer = new ethers.Wallet(w.privateKey, provider);
      const contract = new ethers.Contract(CONTRACT, ABI, signer);
      
      // Claim USDC
      const claimTx = await contract.claimTokens({ gasLimit: 300000, gasPrice: 20477218923n });
      await claimTx.wait();
      console.log(`[${i+1}] ✅ Claim TX: ${claimTx.hash.slice(0,12)}...`);
      
      // Buy tokens
      const amt = Math.floor(Math.random() * (100000 - 50000 + 1)) + 50000;
      const swapTx = await contract.swapExactTokensForTokens(
        ethers.parseUnits(amt.toString(), 18),
        0,
        [CONTRACT],
        w.address,
        Math.floor(Date.now()/1000) + 600,
        { gasLimit: 400000, gasPrice: 20477218923n }
      );
      await swapTx.wait();
      console.log(`      💰 Buy TX: ${swapTx.hash.slice(0,12)}... | ${amt} USDC`);
      
      results.push({ index: i+1, claim: claimTx.hash, swap: swapTx.hash });
    } catch (err) {
      console.log(`[${i+1}] ❌ ${err.message.split('\n')[0]}`);
    }
    if (i < wallets.length - 1) await new Promise(r => setTimeout(r, 500));
  }
  
  console.log(`\n🎉 Done! Processed ${results.length}/${wallets.length} wallets`);
}

main();