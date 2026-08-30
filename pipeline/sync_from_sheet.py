"""
sync_from_sheet.py
Uploads all 82 members from CSV into Django Admin:
- Maps Domain Leads to 'DL' (Section 02)
- Normalizes branches (Electrical -> ELEC, Biomed -> BIOMED, Biotech -> BIOTECH, Mining -> MIN, Meta -> META)
- Robust Google Drive thumbnail URL generation
- Keeps all domains separate
"""

import sys
import os
import csv
import re
import requests

BASE_URL = "https://codeutsava.nitrr.ac.in"
ADMIN_USER = os.environ.get("DJANGO_ADMIN_USER", "TCP26-27")
ADMIN_PASS = os.environ.get("DJANGO_ADMIN_PASS", "Codeutsava@2026#Glitch")
TEAM_YEAR = int(os.environ.get("TEAM_YEAR", 2026))

ROLE_MAP = {
    "oc": "OCO",
    "overall coordinator": "OCO",
    "overall cordinator": "OCO",
    "domain lead": "DL",
    "domain-lead": "DL",
    "lead": "DL",
    "dl": "DL",
    "hc": "HCO",
    "head coordinator": "HCO",
    "head cordinator": "HCO",
    "manager": "MNG",
    "mng": "MNG",
    "executive": "EXC",
    "exc": "EXC",
    "exec": "EXC",
}

BRANCH_MAP = {
    "cse": "CSE",
    "computer science": "CSE",
    "it": "IT",
    "information technology": "IT",
    "ece": "ECE",
    "electronics": "ECE",
    "electrical": "ELEC",
    "elec": "ELEC",
    "ee": "ELEC",
    "mech": "MECH",
    "mechanical": "MECH",
    "chem": "CHEM",
    "chemical": "CHEM",
    "civil": "CIVIL",
    "meta": "META",
    "metallurgy": "META",
    "min": "MIN",
    "mining": "MIN",
    "biomed": "BIOMED",
    "biomedical": "BIOMED",
    "biotech": "BIOTECH",
    "biotechnology": "BIOTECH",
    "mca": "MCA",
}

def normalize_role(raw):
    if not raw:
        return "EXC"
    r = str(raw).strip().lower()
    return ROLE_MAP.get(r, "EXC")

def normalize_branch(raw):
    if not raw:
        return "CSE"
    b = str(raw).strip().lower()
    return BRANCH_MAP.get(b, "CSE")

def normalize_domain(raw, role_code=""):
    # For OCs, use blank (frontend hides domain for OCs)
    if role_code == "OCO":
        return " "

    if not raw:
        return "PR & Marketing"

    d = str(raw).strip()
    d_lower = d.lower()

    if d_lower in ("n/a", "na", "none", "-", ""):
        return " "

    # Keep every domain separate — order matters for combined values like "PR, Doc"
    if "snm" in d_lower or "mentorship" in d_lower or "skill" in d_lower:
        return "Skills & Mentorship"
    if "project" in d_lower:
        return "Project"
    if "social" in d_lower:
        return "Social Media"
    if "video" in d_lower:
        return "Video Editing"
    if "design" in d_lower:
        return "Design"
    if "spons" in d_lower:
        return "sponsorship"
    if "doc" in d_lower:
        return "Documentation"
    if "pr" in d_lower or "marketing" in d_lower:
        return "PR & Marketing"
    if "tech" in d_lower:
        return "Technical"

    return "PR & Marketing"

def format_drive_url(url):
    if not url:
        return ""
    url = str(url).strip()
    match = (
        re.search(r"/file/d/([a-zA-Z0-9_-]+)", url)
        or re.search(r"/d/([a-zA-Z0-9_-]+)", url)
        or re.search(r"[?&]id=([a-zA-Z0-9_-]+)", url)
        or re.search(r"id=([a-zA-Z0-9_-]+)", url)
    )
    if match:
        return f"https://lh3.googleusercontent.com/d/{match.group(1)}=w600"
    return url if url.startswith("http") else ""

def clean_url(url):
    if not url:
        return ""
    url = str(url).strip()
    return url if url.startswith("http") else ""

def get_admin_session():
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
    headers = {"Referer": login_url}
    res_login = session.post(login_url, data=data, headers=headers)
    if "Log out" not in res_login.text and "Welcome" not in res_login.text:
        raise RuntimeError("Django Admin login failed. Check credentials.")
    print("[OK] Successfully logged into Django Admin as", ADMIN_USER)
    return session

def upload_member(session, member):
    add_url = f"{BASE_URL}/server/admin/Team/teammember/add/"
    res_add = session.get(add_url)
    csrf_add = session.cookies.get("csrftoken")

    payload = {
        "csrfmiddlewaretoken": csrf_add,
        "name": member["name"],
        "branch": member.get("branch") or "CSE",
        "member_type": member.get("member_type") or "EXC",
        "domain": member.get("domain") or "Technical",
        "year": TEAM_YEAR,
        "linkedin": member.get("linkedin") or "",
        "instagram": member.get("instagram") or "",
        "github": member.get("github") or "",
        "email": member.get("email") or "",
        "drive_image_url": member.get("drive_image_url") or "",
        "_save": "Save",
    }
    res = session.post(add_url, data=payload, headers={"Referer": add_url})
    if "Select team member to change" in res.text or res.status_code == 200:
        return True
    return False

def main():
    if len(sys.argv) > 1:
        csv_file = sys.argv[1]
    elif os.path.exists("responses.csv"):
        csv_file = "responses.csv"
    elif os.path.exists("pipeline/responses.csv"):
        csv_file = "pipeline/responses.csv"
    else:
        csv_file = "responses.csv"

    if csv_file.startswith("http"):
        sheet_match = re.search(r"/spreadsheets/d/([^/]+)", csv_file)
        if sheet_match:
            sheet_id = sheet_match.group(1)
            csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
            print(f"Downloading CSV from Google Sheet...")
            res = requests.get(csv_url)
            save_path = "pipeline/responses.csv" if os.path.exists("pipeline") else "responses.csv"
            with open(save_path, "wb") as f:
                f.write(res.content)
            csv_file = save_path

    if not os.path.exists(csv_file):
        print(f"ERROR: File '{csv_file}' not found.")
        return

    session = get_admin_session()

    with open(csv_file, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    print(f"Found {len(rows)} entries in {csv_file}. Syncing to Django...")

    success_count = 0
    for i, row in enumerate(rows, start=1):
        name = row.get("Name", "").strip()
        if not name:
            continue

        role_code = normalize_role(row.get("Designation in TCP", ""))
        domain = normalize_domain(row.get("Domain", ""), role_code)
        branch = normalize_branch(row.get("Branch", ""))
        photo = format_drive_url(row.get("Photo", ""))
        linkedin = clean_url(row.get("LinkedIn", ""))
        instagram = clean_url(row.get("Instagram", ""))
        github = clean_url(row.get("GitHub", ""))

        member = {
            "name": name,
            "member_type": role_code,
            "domain": domain,
            "branch": branch,
            "drive_image_url": photo,
            "linkedin": linkedin,
            "instagram": instagram,
            "github": github,
            "email": "",
        }

        ok = upload_member(session, member)
        if ok:
            success_count += 1
            print(f"[{i:02d}/{len(rows)}] [OK] Added: {name} -> Role: {role_code} | Branch: {branch} | Domain: {domain}")
        else:
            print(f"[{i:02d}/{len(rows)}] [FAIL] Failed: {name} (Branch: {branch}, Role: {role_code})")

    print(f"\n==========================================")
    print(f"Successfully uploaded {success_count} / {len(rows)} team members!")
    print(f"Check your API: {BASE_URL}/server/team/{TEAM_YEAR}/")
    print(f"==========================================")

if __name__ == "__main__":
    main()
