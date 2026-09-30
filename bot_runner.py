"""
Bot Runner module for 9Chain Automation Bot.
Manages automated lifecycle: Login -> Check-in -> Auto-Tap -> Smart Upgrade -> Reporting.
"""
import sys
import time
from api_client import NineChainClient

if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace", line_buffering=True)
        sys.stderr.reconfigure(encoding="utf-8", errors="replace", line_buffering=True)
    except Exception:
        pass
from config import (
    TAP_BATCH_SIZE,
    DELAY_BETWEEN_ACCOUNTS,
    LOOP_REST_MINUTES,
    AUTO_UPGRADE_TIER,
    AUTO_UPGRADE_COMPONENTS,
    RESERVE_TIER_COST
)

def format_number(val):
    """Formats numbers with commas."""
    try:
        fval = float(val)
        if fval.is_integer():
            return f"{int(fval):,}"
        return f"{fval:,.2f}"
    except (ValueError, TypeError):
        return str(val)

class NineChainRunner:
    def __init__(self):
        pass

    def run_account(self, email, password, index=1, total=1):
        """Executes full automated workflow for a single account."""
        username = email.split("@")[0]
        print(f"\n{'='*60}")
        print(f"[*] AKUN [{index}/{total}]: {email}")
        print(f"{'='*60}")

        client = NineChainClient()

        # Step 1: Login
        print("[*] Melakukan login...")
        success, res = client.login(email, password)
        if not success:
            print(f"[-] Gagal Login ({email}): {res}")
            return {"status": "login_failed", "email": email, "error": str(res)}
        print("[+] Login berhasil!")

        # Step 2: Daily Check-in
        print("[*] Memeriksa Check-in harian...")
        ok, ci_data = client.get_checkin_status()
        if ok:
            if ci_data.get("checkedInToday"):
                streak = ci_data.get("streak", 0)
                print(f"[i] Check-in harian: Sudah diklaim hari ini (Streak: {streak} hari).")
            else:
                claim_ok, reward = client.claim_checkin()
                if claim_ok:
                    print(f"[+] Check-in berhasil diklaim! +{format_number(reward)} XP")
                else:
                    print(f"[-] Gagal klaim check-in: {reward}")
        else:
            print(f"[!] Gagal mengecek status check-in: {ci_data}")

        # Step 3: Fetch State & Auto-Tap
        ok, state = client.get_program_state()
        if not ok:
            print(f"[-] Gagal mengambil data program/state: {state}")
            return {"status": "state_failed", "email": email}

        rem_taps = state.get("tapsRemaining", 0)
        total_tapped = 0
        print(f"[*] Taps tersisa: {format_number(rem_taps)}")

        if rem_taps > 0:
            print(f"[*] Menjalankan Auto-Tap ({rem_taps} taps)...")
            while rem_taps > 0:
                batch = min(rem_taps, TAP_BATCH_SIZE)
                tap_ok, tap_res = client.tap(batch)
                if not tap_ok:
                    print(f"[!] Gagal tap batch {batch}: {tap_res}")
                    break
                total_tapped += batch
                print(f"    [TAP] Berhasil tap {batch}x (Total siklus ini: {total_tapped}x)")

                s_data = tap_res.get("state", tap_res) if isinstance(tap_res, dict) else {}
                rem_taps = s_data.get("tapsRemaining", rem_taps - batch)
                time.sleep(0.3)
            print(f"[+] Auto-Tap selesai! Total tap dikirim: {total_tapped}")
        else:
            print("[i] Tidak ada tap tersisa untuk diklaim.")

        # Step 4: Smart Upgrades
        upgrades_log = []
        ok, state = client.get_program_state()
        if ok:
            xp = float(state.get("xpTotal", 0))
            current_tier = state.get("nodeTier", state.get("tier", 1))
            next_tier = state.get("nextTier")

            # A. Node Tier Upgrade
            if AUTO_UPGRADE_TIER and next_tier:
                tier_cost = float(next_tier.get("cost", 0))
                target_tier = next_tier.get("tier")
                while next_tier and tier_cost <= xp:
                    print(f"[*] Upgrading Node Tier ke Tier {target_tier} (Biaya: {format_number(tier_cost)} XP)...")
                    u_ok, u_res = client.upgrade_node_tier(target_tier)
                    if u_ok:
                        upgrades_log.append(f"NodeTier->{target_tier}")
                        print(f"[+] Node Tier berhasil diupgrade ke Tier {target_tier}!")
                        state = u_res if isinstance(u_res, dict) else {}
                        xp = float(state.get("xpTotal", xp - tier_cost))
                        next_tier = state.get("nextTier")
                        if next_tier:
                            tier_cost = float(next_tier.get("cost", 0))
                            target_tier = next_tier.get("tier")
                    else:
                        print(f"[-] Gagal upgrade Node Tier: {u_res}")
                        break
                    time.sleep(0.3)

            # B. Component Upgrades (Best ROI / Payback Hours)
            if AUTO_UPGRADE_COMPONENTS:
                reserve = float(next_tier.get("cost", 0)) if (next_tier and RESERVE_TIER_COST) else 0
                spendable = max(0, xp - reserve)
                print(f"[*] Total XP: {format_number(xp)} | Cadangan Tier: {format_number(reserve)} | XP Tersedia: {format_number(spendable)}")

                cat_ok, catalog = client.get_catalog()
                if cat_ok:
                    components = catalog.get("components", [])
                    candidates = []
                    for comp in components:
                        if comp.get("unlocked") and comp.get("level", 0) < comp.get("maxLevel", 999):
                            next_cost = float(comp.get("nextCost", 0))
                            payback = float(comp.get("paybackHours") or 999999)
                            key = comp.get("componentKey")
                            next_lvl = comp.get("level", 0) + 1
                            if 0 < next_cost <= spendable:
                                candidates.append((payback, next_cost, key, next_lvl))

                    # Sort by payback hours ascending (best ROI first)
                    candidates.sort()
                    for pb, cost, key, lvl in candidates:
                        if cost > spendable:
                            continue
                        print(f"    [UPGRADE] {key} -> Level {lvl} (Biaya: {format_number(cost)} XP, Payback: {pb:.1f}h)...")
                        u_ok, u_res = client.upgrade_component(key, lvl)
                        if u_ok:
                            spendable -= cost
                            upgrades_log.append(f"{key}->L{lvl}")
                        else:
                            print(f"    [-] Gagal upgrade {key}: {u_res}")
                            break
                        time.sleep(0.3)

        # Step 5: Final Summary
        ok, final_state = client.get_program_state()
        final_xp = final_state.get("xpTotal", 0) if ok else "?"
        rate = final_state.get("contributionRate", 0) if ok else "?"
        final_tier = final_state.get("nodeTier", final_state.get("tier", "?")) if ok else "?"
        
        print(f"\n[SUMMARY AKUN #{index}]")
        print(f"  - Node Tier        : {final_tier}")
        print(f"  - Total XP         : {format_number(final_xp)}")
        print(f"  - Contribution Rate: {format_number(rate)} / jam")
        print(f"  - Total Tap Siklus : {total_tapped}")
        print(f"  - Upgrades Selesai : {', '.join(upgrades_log) if upgrades_log else 'Tidak ada'}")

        return {
            "status": "success",
            "email": email,
            "tier": final_tier,
            "xp": final_xp,
            "rate": rate,
            "taps": total_tapped,
            "upgrades": upgrades_log
        }

    def run_all(self, accounts, delay_between=DELAY_BETWEEN_ACCOUNTS):
        """Runs single full cycle for all accounts."""
        total = len(accounts)
        print(f"\n{'#'*60}")
        print(f"# MEMULAI SIKLUS OTOMASI 9CHAIN ({total} AKUN)")
        print(f"{'#'*60}")

        results = []
        for i, acc in enumerate(accounts, 1):
            res = self.run_account(acc["email"], acc["password"], index=i, total=total)
            results.append(res)
            if i < total:
                print(f"\n[*] Menunggu {delay_between} detik sebelum akun berikutnya...")
                time.sleep(delay_between)

        # Overall report
        print(f"\n{'='*60}")
        print(f"[*] REKAPITULASI SIKLUS SELESAI ({total} AKUN)")
        print(f"{'='*60}")
        success_count = sum(1 for r in results if r.get("status") == "success")
        fail_count = total - success_count
        print(f"Berhasil: {success_count} | Gagal: {fail_count}")
        for r in results:
            if r.get("status") == "success":
                print(f"  [OK] {r['email']:<30} | Tier: {r.get('tier')} | XP: {format_number(r.get('xp'))} | Rate: {format_number(r.get('rate'))}/jam")
            else:
                print(f"  [FAIL] {r['email']:<30} | Error: {r.get('error', 'Failed')}")
        print(f"{'='*60}\n")
        return results

    def run_loop(self, accounts, loop_rest_minutes=LOOP_REST_MINUTES, delay_between=DELAY_BETWEEN_ACCOUNTS):
        """Runs continuous 24h loop with sleep interval."""
        cycle = 1
        while True:
            print(f"\n{'='*60}")
            print(f"[*] MEMULAI SIKLUS #{cycle} - {time.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"{'='*60}")
            self.run_all(accounts, delay_between)
            cycle += 1

            rest_seconds = loop_rest_minutes * 60
            hours_rest = loop_rest_minutes / 60
            print(f"\n[Zzz] Siklus #{cycle-1} selesai. Istirahat harian selama {hours_rest:.1f} jam ({loop_rest_minutes} menit) sebelum siklus berikutnya...")
            try:
                for remaining in range(rest_seconds, 0, -10):
                    hours, rem = divmod(remaining, 3600)
                    mins, secs = divmod(rem, 60)
                    print(f"\r[*] Waktu istirahat tersisa: {hours:02d} jam {mins:02d} menit {secs:02d} detik...", end="", flush=True)
                    time.sleep(min(10, remaining))
                print("\n[*] Waktu istirahat selesai! Memulai siklus harian berikutnya!")
            except KeyboardInterrupt:
                print("\n[!] Loop dihentikan oleh pengguna.")
                break

    def check_all_status(self, accounts):
        """Quickly checks and displays status for all accounts without performing taps/upgrades."""
        total = len(accounts)
        print(f"\n{'='*75}")
        print(f"[*] MENGECEK STATUS {total} AKUN 9CHAIN")
        print(f"{'='*75}")
        print(f"{'No':<4} {'Email':<32} {'Tier':<6} {'XP Total':<14} {'Rate/h':<10} {'Taps':<8} {'Check-in'}")
        print("-" * 75)

        for i, acc in enumerate(accounts, 1):
            client = NineChainClient()
            ok, token = client.login(acc["email"], acc["password"])
            if not ok:
                print(f"{i:<4} {acc['email']:<32} {'LOGIN FAILED':<35}")
                continue

            ci_ok, ci = client.get_checkin_status()
            ci_status = "Claimed" if ci_ok and ci.get("checkedInToday") else "Ready"

            st_ok, st = client.get_program_state()
            if st_ok:
                tier = str(st.get("nodeTier", st.get("tier", "-")))
                xp = format_number(st.get("xpTotal", 0))
                rate = format_number(st.get("contributionRate", 0))
                taps = format_number(st.get("tapsRemaining", 0))
                print(f"{i:<4} {acc['email']:<32} {tier:<6} {xp:<14} {rate:<10} {taps:<8} {ci_status}")
            else:
                print(f"{i:<4} {acc['email']:<32} {'STATE ERROR':<35}")
            time.sleep(0.5)
        print("=" * 75 + "\n")
