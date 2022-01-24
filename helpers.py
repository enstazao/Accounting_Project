screens_handler = """
ScreenManager:
    AddAccountsScreen:
        name: 'add_account_screen'
    
    GeneralJournalScreen:
        name: 'general-journal'
    
    LeidgersScreen:
        name: 'leidgers'
        id: leidgers_account
    
    TrailBalanceScreen:
        name: 'trail-balance'
        id: trail_balance
    
    IncomeStatementScreen:
        name: 'income-statement'
        id: income_statement

    BalanceSheetScreen:
        name: 'balance-sheet'
        id: balance_sheet

<AddAccountsScreen>:
    MDToolbar:
        title: "Charts Of Accounts"
        pos_hint: {"top": 1}
        elevation: 10

    MDTextField:
        id: account_title
        hint_text: "Enter Title of Account"
        mode: "rectangle"
        required: True
        helper_text_mode: "on_focus"
        pos_hint:{'center_x': 0.5, 'center_y': 0.7}
        size_hint_x:None
        width:300

    MDTextField:
        id: account_type
        hint_text: "Enter Type of Account"
        mode: "rectangle"
        required: True
        helper_text_mode: "on_focus"
        pos_hint:{'center_x': 0.5, 'center_y': 0.6}
        size_hint_x:None
        width:300

    MDTextField:
        id: account_description
        hint_text: "Enter Description"
        mode: "rectangle"
        required: False
        multiline: True
        # helper_text_mode: "on_focus"
        pos_hint:{'center_x': 0.5, 'center_y': 0.5}
        size_hint_x:None
        width:300
    
    MDFillRoundFlatButton:
        text: 'Add'
        pos_hint:{'center_x': 0.4, 'center_y': 0.4}
        on_press: root.Add_Account_Info_To_db(account_title, account_type, account_description)
    
    MDFillRoundFlatButton:
        text: 'General Journal'
        pos_hint:{'center_x': 0.6, 'center_y': 0.4}
        on_press: root.manager.current = 'general-journal'
    
<GeneralJournalScreen>:
    MDToolbar:
        title: "General Journal"
        pos_hint: {"top": 1}
        elevation: 10

    MDRaisedButton:
        text: "                                     Select Date                                            "
        pos_hint: {'center_x': .5, 'center_y': .7}
        on_release: root.show_date_selector()


    MDTextField:
        id: g_account_title
        hint_text: "Enter Title of Account"
        mode: "rectangle"
        required: True
        helper_text_mode: "on_focus"
        pos_hint:{'center_x': 0.5, 'center_y': 0.6}
        size_hint_x:None
        width:300

    MDTextField:
        id: g_account_type
        hint_text: "Enter Type of Account"
        mode: "rectangle"
        required: True
        helper_text_mode: "on_focus"
        pos_hint:{'center_x': 0.5, 'center_y': 0.5}
        size_hint_x:None
        width:300

    MDTextField:
        id: g_account_description
        hint_text: "Enter Description"
        mode: "rectangle"
        # required: True
        # helper_text_mode: "on_focus"
        pos_hint:{'center_x': 0.5, 'center_y': 0.4}
        size_hint_x:None
        width:300

    MDTextField:
        id: g_account_debit
        hint_text: "Enter Debit Amount"
        mode: "rectangle"
        required: True
        helper_text_mode: "on_focus"
        pos_hint:{'center_x': 0.5, 'center_y': 0.3}
        size_hint_x:None
        width:300
    
    MDTextField:
        id: g_account_credit
        hint_text: "Enter Credit Amount"
        mode: "rectangle"
        required: True
        helper_text_mode: "on_focus"
        pos_hint:{'center_x': 0.5, 'center_y': 0.2}
        size_hint_x:None
        width:300
    
    MDFillRoundFlatButton:
        text: 'Search'
        pos_hint:{'center_x': 0.4, 'center_y': 0.1}
        on_press: root.Search_In_DB(g_account_title, g_account_description, g_account_type)


    MDFillRoundFlatButton:
        text: 'Add'
        pos_hint:{'center_x': 0.6, 'center_y': 0.1}
        on_press: root.Add_In_DB(g_account_title, g_account_description, g_account_type, g_account_debit, g_account_credit)
        
    MDFillRoundFlatButton:
        text: 'Back'
        pos_hint:{'center_x': 0.1, 'center_y': 0.1}
        on_press: root.manager.current = 'add_account_screen'

    # Button to go to Trial Balance
    MDFillRoundFlatButton:
        text: 'Trail Balance'
        pos_hint:{'center_x': 0.3, 'center_y': 0.8}
        on_release: 
            app.change_screen('trail-balance')
            root.manager.ids.trail_balance.show_trial_balance()
    MDFillRoundFlatButton:
        text: 'Leidgers'
        pos_hint:{'center_x': 0.1, 'center_y': 0.8}
        on_release: 
            app.change_screen('leidgers')
            root.manager.ids.leidgers_account.display_leidgers()
    MDFillRoundFlatButton:
        text: 'Balance Sheet'
        pos_hint:{'center_x': 0.5, 'center_y': 0.8}
        on_release:
            app.change_screen('balance-sheet')
            root.manager.ids.balance_sheet.Add_Balance_Sheet_Data()
            root.manager.ids.balance_sheet.show_balance_sheet()
    MDFillRoundFlatButton:
        text: 'Income Statement'
        pos_hint:{'center_x': 0.7, 'center_y': 0.8}
        on_release:
            app.change_screen('income-statement')
            root.manager.ids.income_statement.add_income_statement_to_db()
            root.manager.ids.income_statement.display_income_statement()

# Leidgers Screen
<LeidgersScreen>:
    MDBoxLayout:
        orientation: "vertical"
        id: box
            
    MDToolbar:
        title: "Leidgers Account"
        pos_hint: {"top": 1}
        elevation: 10

    ScrollView:
        id: scroll
        AnchorLayout:
            id: box
    MDFillRoundFlatButton:
        text: 'Back'
        pos_hint:{'center_x': 0.1, 'center_y': 0.8}
        on_press: root.manager.current = 'general-journal'
    MDRaisedButton:
        id: button
        text: "SELECT ACCOUNT"
        pos_hint: {"center_x": .9, "center_y": .8}
        on_release: root.menu.open()

# Trial Balance screen
<TrailBalanceScreen>:
    MDToolbar:
        title: "Trial Balance"
        pos_hint: {"top": 1}
        elevation: 10
    MDBoxLayout:
        AnchorLayout:
            id: data_layout
    MDFillRoundFlatButton:
        text: 'Back'
        pos_hint:{'center_x': 0.1, 'center_y': 0.8}
        on_press: root.manager.current = 'general-journal'

# Balance Sheet Screen
<BalanceSheetScreen>:
    MDToolbar:
        title: "Balance Sheet"
        pos_hint: {"top": 1}
        elevation: 10
    MDFillRoundFlatButton:
        text: 'Back'
        pos_hint:{'center_x': 0.1, 'center_y': 0.8}
        on_press: root.manager.current = 'general-journal'
    MDBoxLayout:
        AnchorLayout:
            id: balance_sheet_table
# Income Statement Screen
<IncomeStatementScreen>:
    MDToolbar:
        title: "Income Statement"
        pos_hint: {"top": 1}
        elevation: 10
    MDFillRoundFlatButton:
        text: 'Back'
        pos_hint:{'center_x': 0.1, 'center_y': 0.8}
        on_press: root.manager.current = 'general-journal'
    MDBoxLayout:
        AnchorLayout:
            id: income_statement_table
"""
