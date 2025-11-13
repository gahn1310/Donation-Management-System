"""
main.py - Donation Management System GUI (Professional + Soothing Theme)

- Uses: customtkinter + mysql-connector-python
- Make sure to: pip install customtkinter mysql-connector-python
- Edit DB_CONFIG['password'] to your MySQL password before running.
- This GUI does NOT create stored routines or triggers. It only shows the SQL
  (read-only) and CALLS / RUNS them (so you can demo).
"""

import customtkinter as ctk
from tkinter import ttk, messagebox
import mysql.connector
from datetime import date, datetime
import random, string
import decimal

# ------------------ CONFIG - EDIT YOUR PASSWORD ------------------
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'root',   # <<-- CHANGE THIS
    'database': 'donationmanagementsystem'
}
# -----------------------------------------------------------------

def connect_db():
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except mysql.connector.Error as e:
        messagebox.showerror("DB Error", f"Could not connect to DB:\n{e}")
        return None

def gen_id(prefix):
    ts = datetime.now().strftime("%y%m%d%H%M%S")
    rnd = ''.join(random.choices(string.ascii_uppercase + string.digits, k=3))
    return f"{prefix}{ts}{rnd}"

# ---------- UI helper ----------
def show_rows_in_tree(tree, rows):
    tree.delete(*tree.get_children())
    for r in rows:
        tree.insert("", "end", values=r)

def fetch_table(table_name, cols, tree):
    conn = connect_db()
    if not conn:
        return
    cur = conn.cursor()
    try:
        cur.execute(f"SELECT {', '.join(cols)} FROM {table_name}")
        rows = cur.fetchall()
        show_rows_in_tree(tree, rows)
    except Exception as e:
        messagebox.showerror("DB Read Error", str(e))
    finally:
        cur.close()
        conn.close()

# ---------- INSERT functions for each table ----------
def insert_donor(entries, tree):
    conn = connect_db()
    if not conn:
        return
    cur = conn.cursor()
    try:
        DonorID = entries['DonorID'].get().strip() or gen_id("DNR")
        FN = entries['FN'].get().strip()
        if not FN:
            messagebox.showwarning("Missing", "First Name (FN) is required.")
            return
        MN = entries['MN'].get().strip() or None
        LN = entries['LN'].get().strip() or None
        email = entries['email'].get().strip() or None
        h_no = entries['h_no'].get().strip() or None
        strret = entries['strret'].get().strip() or None
        pincod = entries['pincod'].get().strip() or None
        area = entries['area'].get().strip() or None
        city = entries['city'].get().strip() or None
        state = entries['state'].get().strip() or None
        total = decimal.Decimal(entries['total_donated'].get().strip() or "0.00")
        cur.execute(
            """INSERT INTO donor
               (DonorID, FN, MN, LN, email, h_no, strret, pincod, area, city, state, total_donated)
               VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
            (DonorID, FN, MN, LN, email, h_no, strret, pincod, area, city, state, total)
        )
        conn.commit()
        messagebox.showinfo("Success", f"Donor '{FN}' saved.")
        fetch_table("donor", donor_cols, tree)
        for e in entries.values():
            e.delete(0, "end")
    except Exception as e:
        messagebox.showerror("Insert Error", str(e))
    finally:
        cur.close()
        conn.close()

def insert_donor_phone(entries, tree):
    conn = connect_db()
    if not conn:
        return
    cur = conn.cursor()
    try:
        Donor_id = entries['Donor_id'].get().strip()
        ph_no = entries['ph_no'].get().strip()
        if not Donor_id or not ph_no:
            messagebox.showwarning("Missing", "Donor_id and ph_no are required.")
            return
        cur.execute(
            "INSERT INTO donor_phone (Donor_id, ph_no) VALUES (%s,%s)",
            (Donor_id, ph_no)
        )
        conn.commit()
        messagebox.showinfo("Success", "Phone added.")
        fetch_table("donor_phone", donorphone_cols, tree)
        for e in entries.values():
            e.delete(0, "end")
    except Exception as e:
        messagebox.showerror("Insert Error", str(e))
    finally:
        cur.close()
        conn.close()

def insert_beneficiary(entries, tree):
    conn = connect_db()
    if not conn:
        return
    cur = conn.cursor()
    try:
        b_id = entries['b_id'].get().strip() or gen_id("BEN")
        FN = entries['FN'].get().strip()
        if not FN:
            messagebox.showwarning("Missing", "First Name required")
            return
        MN = entries['MN'].get().strip() or None
        LN = entries['LN'].get().strip() or None
        DOB = entries['DOB'].get().strip() or None
        Age = int(entries['Age'].get().strip()) if entries['Age'].get().strip() else None
        Need_type = entries['Need_type'].get().strip() or None
        phone = entries['phone'].get().strip() or None
        state = entries['state'].get().strip() or None
        city = entries['city'].get().strip() or None
        area = entries['area'].get().strip() or None
        pin = entries['pin'].get().strip() or None
        strret = entries['strret'].get().strip() or None
        H_no = entries['H_no'].get().strip() or None
        cur.execute(
            """INSERT INTO beneficiary
               (b_id, FN, MN, LN, DOB, Age, Need_type, phone, state, city, area, pin, strret, H_no)
               VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
            (b_id, FN, MN, LN, DOB, Age, Need_type, phone, state, city, area, pin, strret, H_no)
        )
        conn.commit()
        messagebox.showinfo("Success", "Beneficiary added.")
        fetch_table("beneficiary", beneficiary_cols, tree)
        for e in entries.values():
            e.delete(0, "end")
    except Exception as e:
        messagebox.showerror("Insert Error", str(e))
    finally:
        cur.close()
        conn.close()

def insert_campaign(entries, tree):
    conn = connect_db()
    if not conn:
        return
    cur = conn.cursor()
    try:
        C_Id = entries['C_Id'].get().strip() or gen_id("CMP")
        C_name = entries['C_name'].get().strip()
        if not C_name:
            messagebox.showwarning("Missing", "Campaign name required")
            return
        start_date = entries['start_date'].get().strip() or None
        end_date = entries['end_date'].get().strip() or None
        target_amt = decimal.Decimal(entries['target_amt'].get().strip() or "0")
        collected_amt = decimal.Decimal(entries['collected_amt'].get().strip() or "0")
        O_Id = entries['O_Id'].get().strip() or None
        cur.execute(
            """INSERT INTO campaign (C_Id, C_name, start_date, end_date, target_amt, collected_amt, O_Id)
               VALUES (%s,%s,%s,%s,%s,%s,%s)""",
            (C_Id, C_name, start_date, end_date, target_amt, collected_amt, O_Id)
        )
        conn.commit()
        messagebox.showinfo("Success", "Campaign added.")
        fetch_table("campaign", campaign_cols, tree)
        for e in entries.values():
            e.delete(0, "end")
    except Exception as e:
        messagebox.showerror("Insert Error", str(e))
    finally:
        cur.close()
        conn.close()

def insert_donation(entries, tree):
    conn = connect_db()
    if not conn:
        return
    cur = conn.cursor()
    try:
        Dot_id = entries['Dot_id'].get().strip() or gen_id("DOT")
        Donation_type = entries['Donation_type'].get().strip() or None
        Donation_date = entries['Donation_date'].get().strip() or date.today().isoformat()
        amt = decimal.Decimal(entries['amt'].get().strip() or "0")
        Description = entries['Description'].get().strip() or None
        tax = decimal.Decimal(entries['tax_deductible_amt'].get().strip() or "0")
        Donor_id = entries['Donor_id'].get().strip() or None
        C_id = entries['C_id'].get().strip() or None
        cur.execute(
            """INSERT INTO donation
               (Dot_id, Donation_type, Donation_date, amt, Description, tax_deductible_amt, Donor_id, C_id)
               VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""",
            (Dot_id, Donation_type, Donation_date, amt, Description, tax, Donor_id, C_id)
        )
        conn.commit()
        messagebox.showinfo("Success", "Donation added.")
        fetch_table("donation", donation_cols, tree)
        for e in entries.values():
            e.delete(0, "end")
    except Exception as e:
        messagebox.showerror("Insert Error", str(e))
    finally:
        cur.close()
        conn.close()

def insert_donation_item(entries, tree):
    conn = connect_db()
    if not conn:
        return
    cur = conn.cursor()
    try:
        Item_no = entries['Item_no'].get().strip() or gen_id("ITM")
        Item_description = entries['Item_description'].get().strip() or None
        Item_quantity = int(entries['Item_quantity'].get().strip() or 0)
        Unit = entries['Unit'].get().strip() or None
        cur.execute(
            "INSERT INTO donation_item (Item_no, Item_description, Item_quantity, Unit) VALUES (%s,%s,%s,%s)",
            (Item_no, Item_description, Item_quantity, Unit)
        )
        conn.commit()
        messagebox.showinfo("Success", "Donation item added.")
        fetch_table("donation_item", donationitem_cols, tree)
        for e in entries.values():
            e.delete(0, "end")
    except Exception as e:
        messagebox.showerror("Insert Error", str(e))
    finally:
        cur.close()
        conn.close()

def insert_distribution(entries, tree):
    conn = connect_db()
    if not conn:
        return
    cur = conn.cursor()
    try:
        DistId = entries['DistId'].get().strip() or gen_id("DST")
        Dist_date = entries['Dist_date'].get().strip() or date.today().isoformat()
        Quantity = int(entries['Quantity'].get().strip() or 0)
        Status = entries['Status'].get().strip() or None
        Dot_ID = entries['Dot_ID'].get().strip() or None
        Reg_no = entries['Reg_no'].get().strip() or None
        cur.execute(
            "INSERT INTO distribution (DistId, Dist_date, Quantity, Status, Dot_ID, Reg_no) VALUES (%s,%s,%s,%s,%s,%s)",
            (DistId, Dist_date, Quantity, Status, Dot_ID, Reg_no)
        )
        conn.commit()
        messagebox.showinfo("Success", "Distribution added.")
        fetch_table("distribution", distribution_cols, tree)
        for e in entries.values():
            e.delete(0, "end")
    except Exception as e:
        messagebox.showerror("Insert Error", str(e))
    finally:
        cur.close()
        conn.close()

def insert_organisation(entries, tree):
    conn = connect_db()
    if not conn:
        return
    cur = conn.cursor()
    try:
        O_Id = entries['O_Id'].get().strip() or gen_id("ORG")
        Org_name = entries['Org_name'].get().strip()
        if not Org_name:
            messagebox.showwarning("Missing", "Organization name required")
            return
        city = entries['city'].get().strip() or None
        state = entries['state'].get().strip() or None
        contact_no = entries['contact_no'].get().strip() or None
        cur.execute(
            "INSERT INTO organisation (O_Id, Org_name, city, state, contact_no) VALUES (%s,%s,%s,%s,%s)",
            (O_Id, Org_name, city, state, contact_no)
        )
        conn.commit()
        messagebox.showinfo("Success", "Organisation added.")
        fetch_table("organisation", organisation_cols, tree)
        for e in entries.values():
            e.delete(0, "end")
    except Exception as e:
        messagebox.showerror("Insert Error", str(e))
    finally:
        cur.close()
        conn.close()

def insert_registration(entries, tree):
    conn = connect_db()
    if not conn:
        return
    cur = conn.cursor()
    try:
        Reg_no = entries['Reg_no'].get().strip() or gen_id("REG")
        PAN_no = entries['PAN_no'].get().strip() or None
        Date_of_Reg = entries['Date_of_Reg'].get().strip() or None
        O_Id = entries['O_Id'].get().strip() or None
        cur.execute(
            "INSERT INTO registration_details (Reg_no, PAN_no, Date_of_Reg, O_Id) VALUES (%s,%s,%s,%s)",
            (Reg_no, PAN_no, Date_of_Reg, O_Id)
        )
        conn.commit()
        messagebox.showinfo("Success", "Registration added.")
        fetch_table("registration_details", registration_cols, tree)
        for e in entries.values():
            e.delete(0, "end")
    except Exception as e:
        messagebox.showerror("Insert Error", str(e))
    finally:
        cur.close()
        conn.close()

# ---------- SQL Tools - show code and RUN (no creation) ----------
sql_function = """-- Function: total_donation_by_donor
CREATE FUNCTION total_donation_by_donor(p_donor_id VARCHAR(50))
RETURNS DECIMAL(12,2)
DETERMINISTIC
RETURN (SELECT IFNULL(SUM(amt),0) FROM donation WHERE Donor_id = p_donor_id);
"""
sql_procedure = """-- Procedure: add_donation_proc
CREATE PROCEDURE add_donation_proc(
  IN p_Dot_id VARCHAR(50),
  IN p_Donation_type VARCHAR(50),
  IN p_Donation_date DATE,
  IN p_amt DECIMAL(12,2),
  IN p_Description TEXT,
  IN p_tax DECIMAL(12,2),
  IN p_Donor_id VARCHAR(50),
  IN p_C_id VARCHAR(50)
)
BEGIN
  INSERT INTO donation (Dot_id, Donation_type, Donation_date, amt, Description, tax_deductible_amt, Donor_id, C_id)
  VALUES (p_Dot_id, p_Donation_type, p_Donation_date, p_amt, p_Description, p_tax, p_Donor_id, p_C_id);
  IF p_C_id IS NOT NULL THEN
    UPDATE campaign
    SET collected_amt = collected_amt + p_amt
    WHERE C_Id = p_C_id;
  END IF;
END
"""
sql_trigger = """-- Trigger: trg_after_insert_donation
CREATE TRIGGER trg_after_insert_donation
AFTER INSERT ON donation
FOR EACH ROW
BEGIN
  UPDATE donor
  SET total_donated = IFNULL(total_donated,0) + NEW.amt
  WHERE DonorID = NEW.Donor_id;
END
"""
sql_nested = """-- Nested query: donors with total_donated > average
SELECT DonorID, FN, total_donated
FROM donor
WHERE total_donated > (SELECT IFNULL(AVG(total_donated),0) FROM donor);
"""

# ---------- Runner functions (now accept output boxes) ----------
def call_procedure_add_donation(values_tuple, outbox):
    conn = connect_db()
    if not conn:
        return
    cur = conn.cursor()
    try:
        cur.callproc('add_donation_proc', values_tuple)
        conn.commit()
        msg = f"✅ Procedure executed: add_donation_proc\nValues: {values_tuple}"
        messagebox.showinfo("Procedure", "Procedure called successfully (add_donation_proc).")
        outbox.configure(state="normal")
        outbox.delete("1.0", "end")
        outbox.insert("1.0", msg)
        outbox.configure(state="disabled")
    except mysql.connector.Error as e:
        msg = f"❌ Procedure Error: {e}"
        messagebox.showerror("Procedure Error", str(e))
        outbox.configure(state="normal")
        outbox.delete("1.0", "end")
        outbox.insert("1.0", msg)
        outbox.configure(state="disabled")
    finally:
        cur.close()
        conn.close()

def call_function_total_donations(donor_id, result_tree, outbox):
    conn = connect_db()
    if not conn:
        return
    cur = conn.cursor()
    try:
        cur.execute("SELECT total_donation_by_donor(%s)", (donor_id,))
        res = cur.fetchone()
        total = res[0] if res else 0
        show_rows_in_tree(result_tree, [(donor_id, total)])
        msg = f"🧮 Function result: total_donation_by_donor('{donor_id}') = {total}"
        outbox.configure(state="normal")
        outbox.delete("1.0", "end")
        outbox.insert("1.0", msg)
        outbox.configure(state="disabled")
    except mysql.connector.Error as e:
        msg = f"❌ Function Error: {e}"
        messagebox.showerror("Function Error", str(e))
        outbox.configure(state="normal")
        outbox.delete("1.0", "end")
        outbox.insert("1.0", msg)
        outbox.configure(state="disabled")
    finally:
        cur.close()
        conn.close()

def run_nested_query_and_show(tree, outbox):
    conn = connect_db()
    if not conn:
        return
    cur = conn.cursor()
    try:
        cur.execute(
            "SELECT DonorID, FN, total_donated FROM donor "
            "WHERE total_donated > (SELECT IFNULL(AVG(total_donated),0) FROM donor)"
        )
        rows = cur.fetchall()
        show_rows_in_tree(tree, rows)
        msg = f"📊 Nested query executed successfully — {len(rows)} rows."
        outbox.configure(state="normal")
        outbox.delete("1.0", "end")
        outbox.insert("1.0", msg)
        outbox.configure(state="disabled")
    except Exception as e:
        msg = f"❌ Query Error: {e}"
        messagebox.showerror("Query Error", str(e))
        outbox.configure(state="normal")
        outbox.delete("1.0", "end")
        outbox.insert("1.0", msg)
        outbox.configure(state="disabled")
    finally:
        cur.close()
        conn.close()

def trigger_demo_insert_donation_then_show(donation_values, donation_tree, donor_tree, outbox):
    conn = connect_db()
    if not conn:
        return
    cur = conn.cursor()
    try:
        cur.execute(
            """INSERT INTO donation
               (Dot_id, Donation_type, Donation_date, amt, Description, tax_deductible_amt, Donor_id, C_id)
               VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""",
            donation_values
        )
        conn.commit()
        fetch_table("donation", donation_cols, donation_tree)
        fetch_table("donor", donor_cols, donor_tree)
        msg = (
            "🚨 Trigger demo: Donation inserted.\n"
            "If trigger exists, donor.total_donated was auto-updated.\n\n"
            f"Values: {donation_values}"
        )
        messagebox.showinfo("Trigger demo", "Inserted donation — trigger effect (if exists) applied.")
        outbox.configure(state="normal")
        outbox.delete("1.0", "end")
        outbox.insert("1.0", msg)
        outbox.configure(state="disabled")
    except Exception as e:
        msg = f"❌ Trigger Demo Error: {e}"
        messagebox.showerror("Trigger Demo Error", str(e))
        outbox.configure(state="normal")
        outbox.delete("1.0", "end")
        outbox.insert("1.0", msg)
        outbox.configure(state="disabled")
    finally:
        cur.close()
        conn.close()
        
 
 # ---------- REFRESH FUNCTION (NEW) ----------
def refresh_all_tables():
    """Reload all data tables in the GUI."""
    try:
        fetch_table("donor", donor_cols, donor_table)
        fetch_table("donor_phone", donorphone_cols, donorphone_table)
        fetch_table("beneficiary", beneficiary_cols, beneficiary_table)
        fetch_table("campaign", campaign_cols, campaign_table)
        fetch_table("donation", donation_cols, donation_table)
        fetch_table("donation_item", donationitem_cols, donationitem_table)
        fetch_table("distribution", distribution_cols, distribution_table)
        fetch_table("organisation", organisation_cols, org_table)
        fetch_table("registration_details", registration_cols, reg_table)
        messagebox.showinfo("Refreshed", "All tables reloaded successfully ✅")
    except Exception as e:
        messagebox.showerror("Refresh Error", str(e))
       

# -------------------- Build UI (soothing theme) --------------------
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")  # base accents

app = ctk.CTk()
app.title("Donation Management System (Soothing Theme)")
app.geometry("1180x780")
app.configure(fg_color="#E8F7F2")   # soothing mint background

# Header
header = ctk.CTkFrame(app, height=90, fg_color="#DFF7F1")
header.pack(fill="x")

# App title (left side)
title = ctk.CTkLabel(
    header,
    text="Donation Management System",
    font=("Helvetica", 22, "bold"),
    text_color="#075E54"
)
title.pack(side="left", padx=20, pady=18)

# 🔄 Refresh Data Button (right side)
refresh_btn = ctk.CTkButton(
    header,
    text="🔄 Refresh Data",
    fg_color="#34c59f",
    hover_color="#2aa886",
    text_color="white",
    command=refresh_all_tables
)
refresh_btn.pack(side="right", padx=20, pady=20)


# Body (tabs)
body = ctk.CTkFrame(app, fg_color="#F7FFFD")
body.pack(fill="both", expand=True, padx=16, pady=12)

tabs = ctk.CTkTabview(body, width=1120)
tabs.pack(fill="both", expand=True, padx=12, pady=12)

# ---------- prepare column lists used repeatedly ----------
donor_cols = ["DonorID", "FN", "MN", "LN", "email", "h_no", "strret", "pincod", "area", "city", "state", "total_donated"]
donorphone_cols = ["Donor_id", "ph_no"]
beneficiary_cols = ["b_id", "FN", "MN", "LN", "DOB", "Age", "Need_type", "phone", "state", "city", "area", "pin", "strret", "H_no"]
campaign_cols = ["C_Id", "C_name", "start_date", "end_date", "target_amt", "collected_amt", "O_Id"]
donation_cols = ["Dot_id", "Donation_type", "Donation_date", "amt", "Description", "tax_deductible_amt", "Donor_id", "C_id"]
donationitem_cols = ["Item_no", "Item_description", "Item_quantity", "Unit"]
distribution_cols = ["DistId", "Dist_date", "Quantity", "Status", "Dot_ID", "Reg_no"]
organisation_cols = ["O_Id", "Org_name", "city", "state", "contact_no"]
registration_cols = ["Reg_no", "PAN_no", "Date_of_Reg", "O_Id"]

# ---------- Tab: Donor ----------
tabs.add("Donor")
donor_tab = tabs.tab("Donor")
donor_scroll = ctk.CTkScrollableFrame(donor_tab, fg_color="#F0FFF9")
donor_scroll.pack(fill="both", expand=True, padx=12, pady=12)
donor_frame = donor_scroll
donor_scroll._scrollbar.configure(width=14)


donor_form = ctk.CTkFrame(donor_frame, fg_color="#E6FBF4", corner_radius=8)
donor_form.pack(side="left", fill="y", padx=12, pady=8)
ctk.CTkLabel(donor_form, text="Add Donor", font=("Helvetica", 16, "bold"), text_color="#056162").pack(pady=8)

donor_entries = {}
for lab in donor_cols:
    ctk.CTkLabel(donor_form, text=lab, text_color="#064e47").pack(anchor="w", padx=8, pady=(6, 0))
    ent = ctk.CTkEntry(donor_form, width=280)
    ent.pack(padx=8, pady=4)
    donor_entries[lab] = ent

ctk.CTkButton(
    donor_form,
    text="Save Donor",
    fg_color="#34c59f",
    hover_color="#2aa886",
    command=lambda: insert_donor(donor_entries, donor_table)
).pack(pady=10)

donor_table_frame = ctk.CTkFrame(donor_frame, fg_color="#F9FFFB")
donor_table_frame.pack(side="right", fill="both", expand=True, padx=12, pady=8)
donor_table = ttk.Treeview(donor_table_frame, columns=donor_cols, show="headings", height=18)
for c in donor_cols:
    donor_table.heading(c, text=c)
    donor_table.column(c, width=100)
donor_table.pack(fill="both", expand=True, padx=8, pady=8)
fetch_table("donor", donor_cols, donor_table)

# ---------- Tab: Donor Phone ----------
tabs.add("Donor Phone")
dp_tab = tabs.tab("Donor Phone")
dp_scroll = ctk.CTkScrollableFrame(dp_tab, fg_color="#F0FFF9")
dp_scroll.pack(fill="both", expand=True, padx=12, pady=12)
dp_frame = dp_scroll
dp_scroll._scrollbar.configure(width=14)

dp_entries = {}
for lab in donorphone_cols:
    ctk.CTkLabel(dp_frame, text=lab, text_color="#064e47").pack(anchor="w", padx=8, pady=(6, 0))
    e = ctk.CTkEntry(dp_frame, width=300)
    e.pack(padx=8, pady=4)
    dp_entries[lab] = e

ctk.CTkButton(
    dp_frame,
    text="Save Phone",
    fg_color="#34c59f",
    command=lambda: insert_donor_phone(dp_entries, donorphone_table)
).pack(pady=8)

donorphone_table = ttk.Treeview(dp_frame, columns=donorphone_cols, show="headings", height=16)
for c in donorphone_cols:
    donorphone_table.heading(c, text=c)
    donorphone_table.column(c, width=200)
donorphone_table.pack(fill="both", expand=True, padx=8, pady=8)
fetch_table("donor_phone", donorphone_cols, donorphone_table)

# ---------- Tab: Beneficiary ----------
tabs.add("Beneficiary")
ben_tab = tabs.tab("Beneficiary")
ben_scroll = ctk.CTkScrollableFrame(ben_tab, fg_color="#F0FFF9")
ben_scroll.pack(fill="both", expand=True, padx=12, pady=12)
ben_frame = ben_scroll
ben_scroll._scrollbar.configure(width=14)

ben_form = ctk.CTkFrame(ben_frame, fg_color="#E6FBF4")
ben_form.pack(side="left", padx=12, pady=8)
ben_entries = {}
for lab in beneficiary_cols:
    ctk.CTkLabel(ben_form, text=lab, text_color="#064e47").pack(anchor="w", padx=8, pady=(6, 0))
    e = ctk.CTkEntry(ben_form, width=260)
    e.pack(padx=8, pady=4)
    ben_entries[lab] = e

ctk.CTkButton(
    ben_form,
    text="Save Beneficiary",
    fg_color="#34c59f",
    command=lambda: insert_beneficiary(ben_entries, beneficiary_table)
).pack(pady=8)

beneficiary_table = ttk.Treeview(ben_frame, columns=beneficiary_cols, show="headings", height=16)
for c in beneficiary_cols:
    beneficiary_table.heading(c, text=c)
    beneficiary_table.column(c, width=110)
beneficiary_table.pack(side="right", fill="both", expand=True, padx=8, pady=8)
fetch_table("beneficiary", beneficiary_cols, beneficiary_table)

# ---------- Tab: Campaign ----------
tabs.add("Campaign")
camp_tab = tabs.tab("Campaign")
camp_scroll = ctk.CTkScrollableFrame(camp_tab, fg_color="#F0FFF9")
camp_scroll.pack(fill="both", expand=True, padx=12, pady=12)
camp_frame = camp_scroll
camp_scroll._scrollbar.configure(width=14)

camp_form = ctk.CTkFrame(camp_frame, fg_color="#E6FBF4")
camp_form.pack(side="left", padx=12, pady=8)
camp_entries = {}
for lab in campaign_cols:
    ctk.CTkLabel(camp_form, text=lab, text_color="#064e47").pack(anchor="w", padx=8, pady=(6, 0))
    e = ctk.CTkEntry(camp_form, width=260)
    e.pack(padx=8, pady=4)
    camp_entries[lab] = e

ctk.CTkButton(
    camp_form,
    text="Save Campaign",
    fg_color="#34c59f",
    command=lambda: insert_campaign(camp_entries, campaign_table)
).pack(pady=8)

campaign_table = ttk.Treeview(camp_frame, columns=campaign_cols, show="headings", height=16)
for c in campaign_cols:
    campaign_table.heading(c, text=c)
    campaign_table.column(c, width=120)
campaign_table.pack(side="right", fill="both", expand=True, padx=8, pady=8)
fetch_table("campaign", campaign_cols, campaign_table)

# ---------- Tab: Donation ----------
tabs.add("Donation")
don_tab = tabs.tab("Donation")
don_scroll = ctk.CTkScrollableFrame(don_tab, fg_color="#F0FFF9")
don_scroll.pack(fill="both", expand=True, padx=12, pady=12)
don_frame = don_scroll
don_scroll._scrollbar.configure(width=14)

don_form = ctk.CTkFrame(don_frame, fg_color="#E6FBF4")
don_form.pack(side="left", padx=12, pady=8)
don_entries = {}
for lab in donation_cols:
    ctk.CTkLabel(don_form, text=lab, text_color="#064e47").pack(anchor="w", padx=8, pady=(6, 0))
    e = ctk.CTkEntry(don_form, width=260)
    e.pack(padx=8, pady=4)
    don_entries[lab] = e

ctk.CTkButton(
    don_form,
    text="Save Donation",
    fg_color="#34c59f",
    command=lambda: insert_donation(don_entries, donation_table)
).pack(pady=8)

donation_table = ttk.Treeview(don_frame, columns=donation_cols, show="headings", height=14)
for c in donation_cols:
    donation_table.heading(c, text=c)
    donation_table.column(c, width=120)
donation_table.pack(side="right", fill="both", expand=True, padx=8, pady=8)
fetch_table("donation", donation_cols, donation_table)

# ---------- Tab: Donation Item ----------
tabs.add("Donation Item")
item_tab = tabs.tab("Donation Item")
item_scroll = ctk.CTkScrollableFrame(item_tab, fg_color="#F0FFF9")
item_scroll.pack(fill="both", expand=True, padx=12, pady=12)
item_frame = item_scroll
item_scroll._scrollbar.configure(width=14)

item_form = ctk.CTkFrame(item_frame, fg_color="#E6FBF4")
item_form.pack(side="left", padx=12, pady=8)
item_entries = {}
for lab in donationitem_cols:
    ctk.CTkLabel(item_form, text=lab, text_color="#064e47").pack(anchor="w", padx=8, pady=(6, 0))
    e = ctk.CTkEntry(item_form, width=260)
    e.pack(padx=8, pady=4)
    item_entries[lab] = e

ctk.CTkButton(
    item_form,
    text="Save Item",
    fg_color="#34c59f",
    command=lambda: insert_donation_item(item_entries, donationitem_table)
).pack(pady=8)

donationitem_table = ttk.Treeview(item_frame, columns=donationitem_cols, show="headings", height=14)
for c in donationitem_cols:
    donationitem_table.heading(c, text=c)
    donationitem_table.column(c, width=140)
donationitem_table.pack(side="right", fill="both", expand=True, padx=8, pady=8)
fetch_table("donation_item", donationitem_cols, donationitem_table)

# ---------- Tab: Distribution ----------
tabs.add("Distribution")
dist_tab = tabs.tab("Distribution")
dist_scroll = ctk.CTkScrollableFrame(dist_tab, fg_color="#F0FFF9")
dist_scroll.pack(fill="both", expand=True, padx=12, pady=12)
dist_frame = dist_scroll
dist_scroll._scrollbar.configure(width=14)

dist_form = ctk.CTkFrame(dist_frame, fg_color="#E6FBF4")
dist_form.pack(side="left", padx=12, pady=8)
dist_entries = {}
for lab in distribution_cols:
    ctk.CTkLabel(dist_form, text=lab, text_color="#064e47").pack(anchor="w", padx=8, pady=(6, 0))
    e = ctk.CTkEntry(dist_form, width=260)
    e.pack(padx=8, pady=4)
    dist_entries[lab] = e

ctk.CTkButton(
    dist_form,
    text="Save Distribution",
    fg_color="#34c59f",
    command=lambda: insert_distribution(dist_entries, distribution_table)
).pack(pady=8)

distribution_table = ttk.Treeview(dist_frame, columns=distribution_cols, show="headings", height=14)
for c in distribution_cols:
    distribution_table.heading(c, text=c)
    distribution_table.column(c, width=120)
distribution_table.pack(side="right", fill="both", expand=True, padx=8, pady=8)
fetch_table("distribution", distribution_cols, distribution_table)

# ---------- Tab: Organisation ----------
tabs.add("Organisation")
org_tab = tabs.tab("Organisation")
org_scroll = ctk.CTkScrollableFrame(org_tab, fg_color="#F0FFF9")
org_scroll.pack(fill="both", expand=True, padx=12, pady=12)
org_frame = org_scroll
org_scroll._scrollbar.configure(width=14)

org_form = ctk.CTkFrame(org_frame, fg_color="#E6FBF4")
org_form.pack(side="left", padx=12, pady=8)
org_entries = {}
for lab in organisation_cols:
    ctk.CTkLabel(org_form, text=lab, text_color="#064e47").pack(anchor="w", padx=8, pady=(6, 0))
    e = ctk.CTkEntry(org_form, width=260)
    e.pack(padx=8, pady=4)
    org_entries[lab] = e

ctk.CTkButton(
    org_form,
    text="Save Org",
    fg_color="#34c59f",
    command=lambda: insert_organisation(org_entries, org_table)
).pack(pady=8)

org_table = ttk.Treeview(org_frame, columns=organisation_cols, show="headings", height=14)
for c in organisation_cols:
    org_table.heading(c, text=c)
    org_table.column(c, width=140)
org_table.pack(side="right", fill="both", expand=True, padx=8, pady=8)
fetch_table("organisation", organisation_cols, org_table)

# ---------- Tab: Registration ----------
tabs.add("Registration")
reg_tab = tabs.tab("Registration")
reg_scroll = ctk.CTkScrollableFrame(reg_tab, fg_color="#F0FFF9")
reg_scroll.pack(fill="both", expand=True, padx=12, pady=12)
reg_frame = reg_scroll
reg_scroll._scrollbar.configure(width=14)

reg_form = ctk.CTkFrame(reg_frame, fg_color="#E6FBF4")
reg_form.pack(side="left", padx=12, pady=8)
reg_entries = {}
for lab in registration_cols:
    ctk.CTkLabel(reg_form, text=lab, text_color="#064e47").pack(anchor="w", padx=8, pady=(6, 0))
    e = ctk.CTkEntry(reg_form, width=260)
    e.pack(padx=8, pady=4)
    reg_entries[lab] = e

ctk.CTkButton(
    reg_form,
    text="Save Registration",
    fg_color="#34c59f",
    command=lambda: insert_registration(reg_entries, reg_table)
).pack(pady=8)

reg_table = ttk.Treeview(reg_frame, columns=registration_cols, show="headings", height=14)
for c in registration_cols:
    reg_table.heading(c, text=c)
    reg_table.column(c, width=140)
reg_table.pack(side="right", fill="both", expand=True, padx=8, pady=8)
fetch_table("registration_details", registration_cols, reg_table)

# ---------- Tab: SQL Tools ----------
from sql_tools import (
    run_function_total_donation_by_donor,
    run_procedure_add_donation,
    run_trigger_demo_insert,
    run_nested_query
)

tabs.add("SQL Tools")
sql_tab = tabs.tab("SQL Tools")
sql_scroll = ctk.CTkScrollableFrame(sql_tab, fg_color="#F7FFFB")
sql_scroll.pack(fill="both", expand=True, padx=12, pady=12)
sql_frame = sql_scroll  # now your existing code uses sql_frame as the scrollable area



ctk.CTkLabel(sql_frame,
    text="SQL Tools — Functions | Procedures | Triggers | Nested Query",
    font=("Helvetica", 18, "bold"),
    text_color="#056162").pack(pady=10)

# ---------------- PROCEDURE SECTION ----------------
proc_frame = ctk.CTkFrame(sql_frame, fg_color="#E8FBF6", corner_radius=10)
proc_frame.pack(fill="x", padx=16, pady=8)

ctk.CTkLabel(proc_frame, text="Stored Procedure: add_donation_proc",
             font=("Helvetica", 15, "bold"), text_color="#056162").pack(anchor="w", padx=10, pady=(6, 4))

# Frame for entries
proc_entry_frame = ctk.CTkFrame(proc_frame, fg_color="#E8FBF6")
proc_entry_frame.pack(padx=10, pady=4)

proc_entries = {}
proc_params = ["Dot_id", "Donation_type", "Donation_date(YYYY-MM-DD)", "amt", "Description", "tax", "Donor_id", "C_id"]

for i, p in enumerate(proc_params):
    e = ctk.CTkEntry(proc_entry_frame, placeholder_text=p, width=150)
    e.grid(row=i//4, column=i%4, padx=6, pady=4)
    proc_entries[p] = e

# Output Box
proc_output_box = ctk.CTkTextbox(proc_frame, width=1000, height=100)
proc_output_box.pack(padx=10, pady=8)
proc_output_box.insert("1.0", "Procedure output will appear here...")
proc_output_box.configure(state="disabled")

def on_call_procedure():
    vals = [proc_entries[p].get().strip() or None for p in proc_params]
    try:
        amt = decimal.Decimal(vals[3]) if vals[3] else decimal.Decimal("0")
        tax = decimal.Decimal(vals[5]) if vals[5] else decimal.Decimal("0")
        call_vals = (vals[0] or gen_id("DOT"), vals[1], vals[2] or date.today().isoformat(),
                     amt, vals[4], tax, vals[6], vals[7])
        result = run_procedure_add_donation(call_vals)
        proc_output_box.configure(state="normal")
        proc_output_box.delete("1.0", "end")
        proc_output_box.insert("1.0", result)
        proc_output_box.configure(state="disabled")
    except Exception as e:
        messagebox.showerror("Procedure Error", str(e))

ctk.CTkButton(proc_frame, text="Execute Procedure", fg_color="#00b894",
              command=on_call_procedure).pack(padx=8, pady=6)

# ---------------- FUNCTION SECTION ----------------
func_frame = ctk.CTkFrame(sql_frame, fg_color="#E8FBF6", corner_radius=10)
func_frame.pack(fill="x", padx=16, pady=8)

ctk.CTkLabel(func_frame, text="Function: total_donation_by_donor",
             font=("Helvetica", 15, "bold"), text_color="#056162").pack(anchor="w", padx=10, pady=(6, 4))

func_entry = ctk.CTkEntry(func_frame, placeholder_text="Enter DonorID", width=200)
func_entry.pack(padx=10, pady=6)

func_output_box = ctk.CTkTextbox(func_frame, width=1000, height=80)
func_output_box.pack(padx=10, pady=8)
func_output_box.insert("1.0", "Function output will appear here...")
func_output_box.configure(state="disabled")

def on_run_function():
    donor_id = func_entry.get().strip()
    if not donor_id:
        messagebox.showwarning("Missing", "Please enter DonorID")
        return
    result = run_function_total_donation_by_donor(donor_id)
    func_output_box.configure(state="normal")
    func_output_box.delete("1.0", "end")
    func_output_box.insert("1.0", result)
    func_output_box.configure(state="disabled")

ctk.CTkButton(func_frame, text="Execute Function", fg_color="#6c5ce7",
              command=on_run_function).pack(padx=8, pady=6)

# ---------------- TRIGGER SECTION ----------------
trig_frame = ctk.CTkFrame(sql_frame, fg_color="#E8FBF6", corner_radius=10)
trig_frame.pack(fill="x", padx=16, pady=8)

ctk.CTkLabel(trig_frame, text="Trigger Demo: Insert Donation (fires trigger if exists)",
             font=("Helvetica", 15, "bold"), text_color="#056162").pack(anchor="w", padx=10, pady=(6, 4))

# Frame for trigger entries
trig_entry_frame = ctk.CTkFrame(trig_frame, fg_color="#E8FBF6")
trig_entry_frame.pack(padx=10, pady=4)

trigger_fields = ["Dot_id", "Donation_type", "Donation_date", "amt", "Description", "tax_deductible_amt", "Donor_id", "C_id"]
td_entries = {}

for i, f in enumerate(trigger_fields):
    e = ctk.CTkEntry(trig_entry_frame, placeholder_text=f, width=150)
    e.grid(row=i//4, column=i%4, padx=6, pady=4)
    td_entries[f] = e

trigger_output_box = ctk.CTkTextbox(trig_frame, width=1000, height=90)
trigger_output_box.pack(padx=10, pady=8)
trigger_output_box.insert("1.0", "Trigger output will appear here...")
trigger_output_box.configure(state="disabled")

def on_trigger_demo():
    vals = [td_entries[k].get().strip() or None for k in trigger_fields]
    try:
        amt = decimal.Decimal(vals[3]) if vals[3] else decimal.Decimal("0")
        tax = decimal.Decimal(vals[5]) if vals[5] else decimal.Decimal("0")
        donation_values = (vals[0] or gen_id("DOT"), vals[1], vals[2] or date.today().isoformat(),
                           amt, vals[4], tax, vals[6], vals[7])
        result = run_trigger_demo_insert(donation_values)
        trigger_output_box.configure(state="normal")
        trigger_output_box.delete("1.0", "end")
        trigger_output_box.insert("1.0", result)
        trigger_output_box.configure(state="disabled")
    except Exception as e:
        messagebox.showerror("Trigger Error", str(e))

ctk.CTkButton(trig_frame, text="Run Trigger Demo", fg_color="#0984e3",
              command=on_trigger_demo).pack(padx=8, pady=6)

# ---------------- NESTED QUERY SECTION ----------------
nest_frame = ctk.CTkFrame(sql_frame, fg_color="#E8FBF6", corner_radius=10)
nest_frame.pack(fill="x", padx=16, pady=8)

ctk.CTkLabel(nest_frame, text="Nested Query: Donors with total_donated > average",
             font=("Helvetica", 15, "bold"), text_color="#056162").pack(anchor="w", padx=10, pady=(6, 4))

nested_output_box = ctk.CTkTextbox(nest_frame, width=1000, height=100)
nested_output_box.pack(padx=10, pady=8)
nested_output_box.insert("1.0", "Nested query output will appear here...")
nested_output_box.configure(state="disabled")

def on_run_nested_query():
    result = run_nested_query()
    nested_output_box.configure(state="normal")
    nested_output_box.delete("1.0", "end")
    nested_output_box.insert("1.0", result)
    nested_output_box.configure(state="disabled")

ctk.CTkButton(nest_frame, text="Execute Nested Query", fg_color="#ff7675",
              command=on_run_nested_query).pack(padx=8, pady=6)

# ---------- Start main loop ----------
app.mainloop()
