from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix import screen
from kivymd.uix.datatables import TableData
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp, sp
from kivymd.uix.label import MDLabel
import pymysql

# Class For Balance sheet Screen
class BalanceSheetScreen(Screen):
    # Add Data To Balance Sheet Table
    def Add_Balance_Sheet_Data(self):
        con = pymysql.connect(host="LocalHost",  user="root",
                              password="JawadAhmed", db="General_Journal_information")
        mycursor = con.cursor()
        mycursor.execute(
            "SELECT account_title, debit_amount, credit_amount FROM trail_balance")
        trail_data = mycursor.fetchall()
        trail_data = list(trail_data)
        balance_sheet_data = []
        data_tpl = ["", "", ""]
        for tupl in trail_data:
            data_tpl[2] = str(int(tupl[1]) + int(tupl[2]))
            data_tpl[0] = tupl[0]
            data_tpl = tuple(data_tpl)
            balance_sheet_data.append(data_tpl)
            data_tpl = list(data_tpl)
        balance_sheet_data2 = []
        mycursor.execute(
            "SELECT account_title, account_type FROM accounts_info")
        accounts_info_data = mycursor.fetchall()
        for tupl in accounts_info_data:
            for tupl2 in balance_sheet_data:
                if (tupl2[0] == tupl[0]):
                    tupl2 = list(tupl2)
                    tupl2[1] = tupl[1]
                    tupl2 = tuple(tupl2)
                    balance_sheet_data2.append(tupl2)
                    break
         # Cleaning the db
        mycursor.execute("DELETE FROM balance_sheet_accounts")
        for tupl in balance_sheet_data2:
            account_title = tupl[0]
            account_type = tupl[1]
            total = tupl[2]
            query = "INSERT INTO balance_sheet_accounts(account_title, account_type, total) VALUES (%s,%s,%s)"
            vl = (account_title, account_type, total)
            mycursor.execute(query, vl)
        con.commit()
        con.close()
    
     # Function That will show the Balane Sheet
    def show_balance_sheet(self):
        con = pymysql.connect(host="LocalHost",  user="root",
                              password="JawadAhmed", db="General_Journal_information")
        mycursor = con.cursor()
        mycursor.execute(
            "SELECT account_title, account_type, total FROM balance_sheet_accounts")
        balance_sheet_data = mycursor.fetchall()
        balance_sheet_data = list(balance_sheet_data)
        balance_sheet_head = [("ASSETS", dp(70)), ("LIABILITIES AND SHAREHOLDERS EQUITY", dp(70))]
        # print(balance_sheet_data)
        left_data = ['Current Asset', 'Fixed Asset', 'Asset']
        right_data = ['Current Liabilities', 'Long Term Liabilities',
                      'Liability Account', 'Equity Account', 'ShareHolder Equity', 'Revenue Account']
        balance_sheet_row = []
        dummy_list = ["", ""]
        total = 0
        spacer = "          "
        # Right Side Data
        for acc_type in left_data:
            for tupl in balance_sheet_data:
                if (acc_type == tupl[1]):
                    dummy_list[0] = tupl[0]             # Account Name
                    total += int(tupl[2])
                    dummy_list[0] = dummy_list[0] + spacer + tupl[2]
                    dummy_list = tuple(dummy_list)
                    balance_sheet_row.append(dummy_list)
                    dummy_list = list(dummy_list)
        left_data_total = total
        dummy_list = list(dummy_list)
        total = 0
        counter = 0
        dummy_list = ["", ""]
        for i in range(len(balance_sheet_row)):
            balance_sheet_row[i] = list(balance_sheet_row[i])
        for acc_type in right_data:
            for tupl in balance_sheet_data:
                # If Liabilities accounts are larger then the assets
                if ((counter == len(balance_sheet_row) and (acc_type == tupl[1]))):
                    dummy_list[1] = tupl[0]
                    total += int(tupl[2])
                    dummy_list[1] = dummy_list[1] + spacer + tupl[2]
                    balance_sheet_row.append(dummy_list)
                    continue
                if (acc_type == tupl[1]):
                    balance_sheet_row[counter][1] = tupl[0]
                    total += int(tupl[2])
                    balance_sheet_row[counter][1] = balance_sheet_row[counter][1] + spacer + tupl[2]
                    counter += 1
        dummy_list[0] = "Total" + spacer + str(left_data_total)
        dummy_list[1] = "Total" + spacer + str(total)
        dummy_list = tuple(dummy_list)
        balance_sheet_row.append(dummy_list)
        balance_sheet = MDDataTable(
            size_hint=(0.6, 0.7),
            use_pagination=True,
            column_data=balance_sheet_head,
            row_data=balance_sheet_row,
            elevation=2,
        )
        
        # Data
        # [('Cash Account', 'Current Asset', '22000')]

        self.manager.ids.balance_sheet.ids.balance_sheet_table.add_widget(balance_sheet)
        con.commit()
        con.close()