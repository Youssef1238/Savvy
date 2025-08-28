from tkinter import ttk


def applyStyles(root) :


    frameStyle = ttk.Style(root)
    frameStyle.theme_use("clam")
    frameStyle.configure("Normal.TFrame",background="#333333")

    drawerStyle = ttk.Style(root)
    drawerStyle.configure("Drawer.TFrame",background="black")

    expenseStyle = ttk.Style(root)
    expenseStyle.configure("expense.TFrame",background="red")

    incomeStyle = ttk.Style(root)
    incomeStyle.configure("income.TFrame",background="green")

    balanceStyle = ttk.Style(root)
    balanceStyle.configure("balance.TFrame",background="blue")

    FormStyle = ttk.Style(root)
    FormStyle.configure("Form.TFrame",background="#171716")

    entryStyle = ttk.Style(root)
    entryStyle.configure("Normal.TEntry",font=("Bodoni MT",13),fieldbackground="#555555",foreground="white",padding=5,relief="flat",highlightcolor="#666666")
    
    comboBoxStyle = ttk.Style(root)
    comboBoxStyle.configure("Normal.TCombobox",font=("Bodoni MT",13),fieldbackground="#555555",foreground="white",padding=5,relief="flat",highlightcolor="#666666")
    comboBoxStyle.map("Normal.TCombobox", fieldbackground=[("readonly", "#555555")], stateforeground=[("readonly", "white")],background=[("readonly", "#555555")])

    buttonStyle = ttk.Style(root)
    buttonStyle.configure("Normal.TButton",background="#666666",foreground="white",font=("Bodoni MT",16))
    buttonStyle.map("Normal.TButton",background=[("active", "#555555")],foreground=[("disabled", "gray"), ("active", "white")] )

    drawer_Labels_Style = ttk.Style(root)
    drawer_Labels_Style.configure("Drawer.TLabel",background="black",foreground="white",font=("Bodoni MT",14),padding=(10,5),anchor="w")
    drawer_Labels_Style.map("Drawer.TLabel", background=[("hover", "#555555")], effectforeground=[("hover", "#00bcd4")]) 

    hamButtonStyle = ttk.Style(root)
    hamButtonStyle.configure("ham.TButton",background="black",foreground="white",font=("Bodoni MT",16))
    hamButtonStyle.map("ham.TButton",background=[("active", "#212120")],foreground=[("disabled", "gray"), ("active", "white")] )

    TreeStyle = ttk.Style()
    TreeStyle.configure("Treeview",  background="#333333", foreground="white", rowheight=25, fieldbackground="#333333")
    TreeStyle.map("Treeview", background=[("selected", "#ff8800")], foreground=[("selected", "black")])

    CardStyle = ttk.Style()
    CardStyle.configure("Card.TFrame",background="#333333",foreground="white",borderwidth=2,relief="groove")
    hoveredCardStyle = ttk.Style()
    hoveredCardStyle.configure("hoverCard.TFrame",background="#b66b16",foreground="white",borderwidth=2,relief="groove")


    CardLabel = ttk.Style()
    CardLabel.configure("Card.TLabel",font=("Bodoni MT",12),background="#333333",foreground="#dbd6d0",anchor="center")
    TitleLabel = ttk.Style()
    TitleLabel.configure("CardTitle.TLabel",font=("Bodoni MT",16,"bold"),background="#333333",foreground="#b66b16",anchor="center")

