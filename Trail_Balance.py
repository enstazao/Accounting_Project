from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp, sp
import pymysql

class TrailBalanceScreen(Screen):
     # Creating Trail Balance

    def show_trial_balance(self):
        # Need to Add Total
        con = pymysql.connect(host="LocalHost",  user="root",
                              password="JawadAhmed", db="General_Journal_information")
        mycursor = con.cursor()
        mycursor.execute(
            "SELECT account_title, debit_amount, credit_amount FROM trail_balance")
        trail_table_row = mycursor.fetchall()
        trail_table_row = list(trail_table_row)
        print(trail_table_row)
        trail_table_col = [("Account Title", dp(40)),
                           ("Debit", dp(20)), ("Credit", dp(20))]
        print("T=",trail_table_row)
        total = ["", "", ""]
        debit_sum = 0
        credit_sum = 0
        for tupl in trail_table_row:
            debit_sum += int(tupl[1])
            credit_sum += int(tupl[2])
        total[0] = "Total"
        total[1] = str(debit_sum)
        total[2] = str(credit_sum)
        total = tuple(total)
        trail_table_row.append(total)
        self.trail_table = MDDataTable(
            size_hint=(0.6, 0.7),
            use_pagination=True,
            column_data=trail_table_col,
            row_data=trail_table_row,
            elevation=2,
        )
        self.manager.ids.trail_balance.ids.data_layout.add_widget(
            self.trail_table)
        con.commit()
        con.close()