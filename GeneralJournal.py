from kivy.uix.screenmanager import Screen, ScreenManager
from kivymd.uix.datatables import TableData
from kivymd.uix.picker import MDDatePicker
from helpers import screens_handler
from kivymd.uix.button import MDRectangleFlatIconButton,  MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp, sp
from kivymd.uix.label import MDLabel
import pymysql

# Class where user can make entries
class GeneralJournalScreen(Screen):
    # Function That Will Search Given Account IN DB
    def Search_In_DB(self, g_account_title, g_account_description, g_account_type):
        if (g_account_title.text != ""):
            con = pymysql.connect(host="LocalHost",  user="root",
                                password="JawadAhmed", db="General_Journal_information")
            mycursor = con.cursor()
            mycursor.execute(
                'SELECT * FROM accounts_info WHERE account_title=%s', g_account_title.text)
            accounts_data = mycursor.fetchall()
            if not accounts_data:
                close_button = MDFlatButton(
                    text='Close', on_release=self.close_dialog)
                more_button = MDFlatButton(
                    text='Add Account', on_release=self.go_to_addaccount)
                account_name = g_account_title.text + " Not Exist."
                self.dialog = MDDialog(title='Account Not Exist', text=account_name, size_hint=(0.7, 1),
                                    buttons=[close_button, more_button])
                self.dialog.open()
            # User Given Account Exist
            else:
                g_account_description.text = accounts_data[0][2]
                g_account_type.text = accounts_data[0][1]
            con.commit()
            con.close()
        else:
            close_button = MDFlatButton(
                text='Close', on_release=self.close_dialog)
            show_warning = "Please Enter AccountTitle"
            self.dialog = MDDialog(title='Empty Fields', text=show_warning, size_hint=(0.7, 1),
                                   buttons=[close_button])
            self.dialog.open()
    # Take User to Add Account Screen

    def go_to_addaccount(self, obj):
        self.manager.current = 'add_account_screen'
        self.dialog.dismiss()
    # When User Press Save button

    def on_save(self, instance, value, date_range):
        self.date = value

    # On Press of cancel
    def on_cancel(self, instance, value):
        '''Events called when the "CANCEL" dialog box button is clicked.'''
    # Show Date Selector

    def show_date_selector(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        date_dialog.open()
    # Function THat will add data Into a DB

    def Add_In_DB(self, g_account_title, g_account_description, g_account_type, g_account_debit, g_account_credit):
        if (g_account_title.text != "" and g_account_debit.text != "" and g_account_credit.text != ""):
            con = pymysql.connect(host="LocalHost",  user="root",
                                password="JawadAhmed", db="General_Journal_information")
            mycursor = con.cursor()
            # print(type(self.date))
            query = "INSERT INTO general_journal_info(account_title, account_type, account_description, debit_amount, credit_amount, account_entry_date) VALUES (%s,%s,%s,%s,%s,%s)"
            vl = (g_account_title.text, g_account_type.text, g_account_description.text,
                g_account_debit.text, g_account_credit.text, self.date)
            mycursor.execute(query, vl)
            con.commit()
            con.close()
            # Clear the field
            g_account_title.text = ""
            g_account_type.text = ""
            g_account_description.text = ""
            g_account_debit.text = ""
            g_account_credit.text = ""
        else:
            close_button = MDFlatButton(
            text='Close', on_release=self.close_dialog)
            show_warning = "Please Fill All The Fields"
            self.dialog = MDDialog(title='Empty Fields', text=show_warning, size_hint=(0.7, 1),
                                   buttons=[close_button])
            self.dialog.open()
    # Close the dialog box
    def close_dialog(self, obj):
        self.dialog.dismiss()
    # Display Balance Sheet