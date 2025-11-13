#Code Snippet for Invoking the Stored Procedure
def call_procedure_add_donation(values_tuple):
    conn = mysql.connector.connect(**DB_CONFIG)
    cur = conn.cursor()
    try:
        cur.callproc('add_donation_proc', values_tuple)
        conn.commit()
        print("Procedure executed successfully.")
    except mysql.connector.Error as e:
        print("Procedure Error:", e)
    finally:
        cur.close()
        conn.close()



#Code Snippet for Invoking the Stored Function
def call_function_total_donations(donor_id):
    conn = mysql.connector.connect(**DB_CONFIG)
    cur = conn.cursor()
    try:
        cur.execute("SELECT total_donation_by_donor(%s)", (donor_id,))
        result = cur.fetchone()
        print("Total Donation =", result[0])
    except mysql.connector.Error as e:
        print("Function Error:", e)
    finally:
        cur.close()
        conn.close()


#Code Snippet for Trigger Invocation (Automatic Execution)

def trigger_demo_insert():
    conn = mysql.connector.connect(**DB_CONFIG)
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO donation
            (Dot_id, Donation_type, Donation_date, amt, Description, tax_deductible_amt, Donor_id, C_id)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        """, ("DOT002", "Online", "2025-01-12", 2500.00,
              "Trigger Test", 100.00, "DNR123", "CMP89"))
        
        conn.commit()
        print("Inserted donation — Trigger executed automatically!")
    except Exception as e:
        print("Trigger Error:", e)
    finally:
        cur.close()
        conn.close()

