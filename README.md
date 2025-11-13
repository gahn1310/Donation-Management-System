Donation Management System
A simple Python + MySQL based GUI application to manage donors, donations, campaigns, beneficiaries, organisations, and distributions for an NGO or charity.

Features
Add and manage donors
Add campaigns and track collected amount
Record donations (cash/online/items)
Maintain beneficiary and organisation details
Automatic donor total update using trigger
Update campaign collected amount using stored procedure
Check total donated amount using stored function
Run nested & join queries
GUI built using customtkinter

Technologies Used
Python
customtkinter
MySQL
mysql-connector-python

Setup
1. Install requirements
pip install customtkinter mysql-connector-python
2. Import database
Run in MySQL:
SOURCE donation_system.sql;
3. Update DB credentials
In main.py:
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'yourpassword',
    'database': 'donationmanagementsystem'
}
4. Run the app
python main.py

Project Files
main.py
sql_tools.py
donation_system.sql
requirements.txt
