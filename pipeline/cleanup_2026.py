"""
cleanup_2026.py — Helper to delete 2026 test entries from Django Admin before clean re-sync.
"""
import requests
import re

BASE_URL = "https://codeutsava.nitrr.ac.in"
ADMIN_USER = "TCP26-27"
ADMIN_PASS = "Codeutsava@2026#Glitch"

session = requests.Session()
login_url = f"{BASE_URL}/server/admin/login/"
res = session.get(login_url)
csrf = session.cookies.get("csrftoken")

data = {
    "username": ADMIN_USER,
    "password": ADMIN_PASS,
    "csrfmiddlewaretoken": csrf,
    "next": "/server/admin/",
}
session.post(login_url, data=data, headers={"Referer": login_url})

# Get list of 2026 members
res_api = requests.get(f"{BASE_URL}/server/team/2026/")
members = res_api.json().get("data", [])
print(f"Found {len(members)} entries for 2026 to delete before clean re-sync...")

for m in members:
    mid = m["id"]
    del_url = f"{BASE_URL}/server/admin/Team/teammember/{mid}/delete/"
    r_page = session.get(del_url)
    csrf_del = session.cookies.get("csrftoken")
    session.post(del_url, data={"csrfmiddlewaretoken": csrf_del, "post": "yes"}, headers={"Referer": del_url})
    print(f"Deleted ID {mid}: {m['name']}")

print("Cleanup complete!")
