"""
Main Entrypoint for 9Chain Automation Bot.
Provides interactive CLI menu and direct argument-based execution.
"""
import sys
import os

if sys.platform.startswith("win"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace", line_buffering=True)
        sys.stderr.reconfigure(encoding="utf-8", errors="replace", line_buffering=True)
    except Exception:
        pass
from config import load_accounts, DELAY_BETWEEN_ACCOUNTS, LOOP_REST_MINUTES
from bot_runner import NineChainRunner

BANNER = r"""
==================================================================
   ___        ____ _           _         ____        _   
  / _ \      / ___| |__   __ _(_)_ __   | __ )  ___ | |_ 
 | (_) |____| |   | '_ \ / _` | | '_ \  |  _ \ / _ \| __|
  \__, |____| |___| | | | (_| | | | | | | |_) | (_) | |_ 
    /_/      \____|_| |_|\__,_|_|_| |_| |____/ \___/ \__| 
             Automated Multi-Account Bot (9Chain v2)
==================================================================
"""

def print_menu(account_count):
    print(BANNER)
    print(f" Terdeteksi {account_count} akun tersimpan di accounts.txt")
    print("-" * 66)
    print(" [1] Jalankan 1 Siklus Penuh (Semua Akun)")
    print(" [2] Jalankan Mode Harian 1x Per Hari (Loop 24 Jam Otomatis)")
    print(" [3] Cek Status, XP, dan Sisa Tap Semua Akun (Read-only)")
    print(" [4] Jalankan Satu Akun Tertentu")
    print(" [0] Keluar")
    print("=" * 66)

def main():
    accounts = load_accounts()
    if not accounts:
        print("[!] Tidak ada akun yang dimuat dari accounts.txt. Silakan cek file accounts.txt.")
        sys.exit(1)

    runner = NineChainRunner()

    # Direct argument mode
    if len(sys.argv) > 1:
        choice = sys.argv[1].strip()
        if choice == "1":
            runner.run_all(accounts, delay_between=DELAY_BETWEEN_ACCOUNTS)
            return
        elif choice == "2":
            runner.run_loop(accounts, loop_rest_minutes=LOOP_REST_MINUTES, delay_between=DELAY_BETWEEN_ACCOUNTS)
            return
        elif choice == "3":
            runner.check_all_status(accounts)
            return
        elif choice == "4":
            acc_idx = int(sys.argv[2]) - 1 if len(sys.argv) > 2 else 0
            if 0 <= acc_idx < len(accounts):
                acc = accounts[acc_idx]
                runner.run_account(acc["email"], acc["password"], index=acc_idx + 1, total=len(accounts))
            else:
                print(f"[!] Nomor akun {acc_idx + 1} tidak valid (Total: {len(accounts)})")
            return
        else:
            print(f"[!] Argumen tidak valid: {choice}")
            print("Gunakan: python main.py [1|2|3|4]")
            return

    # Interactive menu mode
    while True:
        print_menu(len(accounts))
        try:
            pilihan = input("Pilih menu [0-4]: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n[!] Program ditutup.")
            break

        if pilihan == "1":
            runner.run_all(accounts, delay_between=DELAY_BETWEEN_ACCOUNTS)
        elif pilihan == "2":
            runner.run_loop(accounts, loop_rest_minutes=LOOP_REST_MINUTES, delay_between=DELAY_BETWEEN_ACCOUNTS)
        elif pilihan == "3":
            runner.check_all_status(accounts)
        elif pilihan == "4":
            print(f"\nDaftar Akun (Total: {len(accounts)}):")
            for idx, a in enumerate(accounts, 1):
                print(f"  [{idx}] {a['email']}")
            try:
                sel = input(f"\nPilih nomor akun [1-{len(accounts)}]: ").strip()
                sel_idx = int(sel) - 1
                if 0 <= sel_idx < len(accounts):
                    acc = accounts[sel_idx]
                    runner.run_account(acc["email"], acc["password"], index=sel_idx + 1, total=len(accounts))
                else:
                    print("[!] Pilihan nomor tidak valid.")
            except ValueError:
                print("[!] Masukkan angka yang valid.")
        elif pilihan == "0":
            print("[+] Terima kasih telah menggunakan 9Chain Bot!")
            break
        else:
            print("[!] Pilihan tidak valid, silakan coba lagi.")

        input("\nTekan Enter untuk kembali ke menu...")

if __name__ == "__main__":
    main()
