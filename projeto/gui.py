import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class LoginWindow(tk.Tk):
    """Janela de Login."""
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.title("Login do Sistema")
        self.geometry("300x150")
        self.resizable(False, False)

        self.username_label = tk.Label(self, text="Usuário:")
        self.username_label.pack(pady=5)
        self.username_entry = tk.Entry(self)
        self.username_entry.pack(pady=5)

        self.password_label = tk.Label(self, text="Senha:")
        self.password_label.pack(pady=5)
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack(pady=5)

        self.login_button = tk.Button(self, text="Entrar", command=self.check_login)
        self.login_button.pack(pady=10)

    def check_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        user = self.db_manager.fetch_one(
            "SELECT * FROM users WHERE username = %s AND password = %s",
            (username, password)
        )

        if user:
            self.destroy()
            main_app = MainWindow(self.db_manager)
            main_app.mainloop()
        else:
            messagebox.showerror("Erro de Login", "Usuário ou senha inválidos.")

class MainWindow(tk.Tk):
    """Janela Principal da Aplicação."""
    def __init__(self, db_manager):
        super().__init__()
        self.db_manager = db_manager
        self.title("Sistema de Gerenciamento de Vendas")
        self.geometry("900x700")

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill='both', padx=10, pady=10)

        # Aba de Produtos
        self.products_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.products_frame, text='Produtos')
        self.setup_products_ui()

        #Aba de Clientes
        self.clients_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.clients_frame, text='Clientes')
        self.setup_clients_ui()

        #Aba de Vendas
        self.sales_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.sales_frame, text='Registrar Venda')
        self.setup_sales_ui()

        # Aba de Gráfico
        self.graph_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.graph_frame, text='Gráfico de Vendas')
        self.setup_graph_ui()
        
        # Carregar dados iniciais
        self.load_products()
        self.load_clients()
        self.load_sales()

    def setup_products_ui(self):
        form_frame = ttk.LabelFrame(self.products_frame, text="Gerenciar Produto")
        form_frame.pack(fill='x', padx=10, pady=10)

        tk.Label(form_frame, text="Nome:").grid(row=0, column=0, padx=5, pady=5)
        self.product_name_entry = tk.Entry(form_frame)
        self.product_name_entry.grid(row=0, column=1, padx=5, pady=5)
        tk.Label(form_frame, text="Preço:").grid(row=1, column=0, padx=5, pady=5)
        self.product_price_entry = tk.Entry(form_frame)
        self.product_price_entry.grid(row=1, column=1, padx=5, pady=5)
        tk.Label(form_frame, text="Estoque:").grid(row=2, column=0, padx=5, pady=5)
        self.product_stock_entry = tk.Entry(form_frame)
        self.product_stock_entry.grid(row=2, column=1, padx=5, pady=5)
        self.product_id_entry = tk.Entry(form_frame)

        btn_frame = ttk.Frame(self.products_frame)
        btn_frame.pack(fill='x', padx=10, pady=5)
        tk.Button(btn_frame, text="Adicionar", command=self.add_product).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Atualizar", command=self.update_product).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Excluir", command=self.delete_product).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Limpar", command=self.clear_product_form).pack(side='left', padx=5)

        tree_frame = ttk.Frame(self.products_frame)
        tree_frame.pack(expand=True, fill='both', padx=10, pady=10)
        self.product_tree = ttk.Treeview(tree_frame, columns=("ID", "Nome", "Preço", "Estoque"), show='headings')
        self.product_tree.heading("ID", text="ID"); self.product_tree.heading("Nome", text="Nome")
        self.product_tree.heading("Preço", text="Preço"); self.product_tree.heading("Estoque", text="Estoque")
        self.product_tree.column("ID", width=50); self.product_tree.pack(expand=True, fill='both')
        self.product_tree.bind('<<TreeviewSelect>>', self.on_product_select)

    def setup_clients_ui(self):
        form_frame = ttk.LabelFrame(self.clients_frame, text="Gerenciar Cliente")
        form_frame.pack(fill='x', padx=10, pady=10)

        tk.Label(form_frame, text="Nome:").grid(row=0, column=0, padx=5, pady=5)
        self.client_name_entry = tk.Entry(form_frame)
        self.client_name_entry.grid(row=0, column=1, padx=5, pady=5)
        tk.Label(form_frame, text="Email:").grid(row=1, column=0, padx=5, pady=5)
        self.client_email_entry = tk.Entry(form_frame)
        self.client_email_entry.grid(row=1, column=1, padx=5, pady=5)
        tk.Label(form_frame, text="Telefone:").grid(row=2, column=0, padx=5, pady=5)
        self.client_phone_entry = tk.Entry(form_frame)
        self.client_phone_entry.grid(row=2, column=1, padx=5, pady=5)
        self.client_id_entry = tk.Entry(form_frame)

        btn_frame = ttk.Frame(self.clients_frame)
        btn_frame.pack(fill='x', padx=10, pady=5)
        tk.Button(btn_frame, text="Adicionar", command=self.add_client).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Atualizar", command=self.update_client).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Excluir", command=self.delete_client).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Limpar", command=self.clear_client_form).pack(side='left', padx=5)

        tree_frame = ttk.Frame(self.clients_frame)
        tree_frame.pack(expand=True, fill='both', padx=10, pady=10)
        self.client_tree = ttk.Treeview(tree_frame, columns=("ID", "Nome", "Email", "Telefone"), show='headings')
        self.client_tree.heading("ID", text="ID"); self.client_tree.heading("Nome", text="Nome")
        self.client_tree.heading("Email", text="Email"); self.client_tree.heading("Telefone", text="Telefone")
        self.client_tree.column("ID", width=50); self.client_tree.pack(expand=True, fill='both')
        self.client_tree.bind('<<TreeviewSelect>>', self.on_client_select)

    def setup_sales_ui(self):
        form_frame = ttk.LabelFrame(self.sales_frame, text="Registrar Nova Venda")
        form_frame.pack(fill='x', padx=10, pady=10)

        tk.Label(form_frame, text="Produto:").grid(row=0, column=0, padx=5, pady=5)
        self.sale_product_combo = ttk.Combobox(form_frame, state="readonly")
        self.sale_product_combo.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_frame, text="Quantidade:").grid(row=1, column=0, padx=5, pady=5)
        self.sale_quantity_entry = tk.Entry(form_frame)
        self.sale_quantity_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Button(form_frame, text="Registrar Venda", command=self.add_sale).grid(row=2, column=0, columnspan=2, pady=10)

        tree_frame = ttk.LabelFrame(self.sales_frame, text="Histórico de Vendas")
        tree_frame.pack(expand=True, fill='both', padx=10, pady=10)
        self.sales_tree = ttk.Treeview(tree_frame, columns=("ID", "Produto", "Quantidade", "Data"), show='headings')
        self.sales_tree.heading("ID", text="ID Venda"); self.sales_tree.heading("Produto", text="Produto")
        self.sales_tree.heading("Quantidade", text="Quantidade"); self.sales_tree.heading("Data", text="Data da Venda")
        self.sales_tree.column("ID", width=60); self.sales_tree.pack(expand=True, fill='both')

    # --- UI DO GRÁFICO ---
    def setup_graph_ui(self):
        btn_generate = tk.Button(self.graph_frame, text="Gerar/Atualizar Gráfico de Vendas", command=self.plot_sales_graph)
        btn_generate.pack(pady=20)
        self.canvas_frame = ttk.Frame(self.graph_frame)
        self.canvas_frame.pack(expand=True, fill='both')

    # --- LÓGICA DE PRODUTOS ---
    def load_products(self):
        for item in self.product_tree.get_children(): self.product_tree.delete(item)
        products = self.db_manager.fetch_all("SELECT * FROM products ORDER BY name")
        for p in products: self.product_tree.insert("", "end", values=(p['id'], p['name'], p['price'], p['stock']))
        # Atualiza a combobox de vendas
        self.sale_product_combo['values'] = [p['name'] for p in products]

    def add_product(self):
        name, price, stock = self.product_name_entry.get(), self.product_price_entry.get(), self.product_stock_entry.get()
        if not all([name, price, stock]): messagebox.showwarning("Campos Vazios", "Todos os campos devem ser preenchidos."); return
        query = "INSERT INTO products (name, price, stock) VALUES (%s, %s, %s)"
        if self.db_manager.execute_query(query, (name, price, stock)): self.clear_product_form(); self.load_products()
        else: messagebox.showerror("Erro", "Falha ao adicionar produto.")

    def update_product(self):
        product_id = self.product_id_entry.get()
        if not product_id: messagebox.showwarning("Seleção", "Selecione um produto para atualizar."); return
        name, price, stock = self.product_name_entry.get(), self.product_price_entry.get(), self.product_stock_entry.get()
        query = "UPDATE products SET name = %s, price = %s, stock = %s WHERE id = %s"
        if self.db_manager.execute_query(query, (name, price, stock, product_id)): self.clear_product_form(); self.load_products()
        else: messagebox.showerror("Erro", "Falha ao atualizar produto.")

    def delete_product(self):
        product_id = self.product_id_entry.get()
        if not product_id: messagebox.showwarning("Seleção", "Selecione um produto para excluir."); return
        if messagebox.askyesno("Confirmar", "Tem certeza que deseja excluir este produto?"):
            query = "DELETE FROM products WHERE id = %s"
            if self.db_manager.execute_query(query, (product_id,)): self.clear_product_form(); self.load_products()
            else: messagebox.showerror("Erro", "Falha ao excluir produto. Verifique se ele não está associado a vendas.")

    def on_product_select(self, event):
        selected_item = self.product_tree.focus()
        if not selected_item: return
        item_data = self.product_tree.item(selected_item)['values']
        self.clear_product_form()
        self.product_id_entry.insert(0, item_data[0]); self.product_name_entry.insert(0, item_data[1])
        self.product_price_entry.insert(0, item_data[2]); self.product_stock_entry.insert(0, item_data[3])

    def clear_product_form(self):
        self.product_id_entry.delete(0, 'end'); self.product_name_entry.delete(0, 'end')
        self.product_price_entry.delete(0, 'end'); self.product_stock_entry.delete(0, 'end')

    # --- LÓGICA DE CLIENTES ---
    def load_clients(self):
        for item in self.client_tree.get_children(): self.client_tree.delete(item)
        clients = self.db_manager.fetch_all("SELECT * FROM clients ORDER BY name")
        for c in clients: self.client_tree.insert("", "end", values=(c['id'], c['name'], c['email'], c['phone']))

    def add_client(self):
        name, email, phone = self.client_name_entry.get(), self.client_email_entry.get(), self.client_phone_entry.get()
        if not name: messagebox.showwarning("Campo Vazio", "O nome do cliente é obrigatório."); return
        query = "INSERT INTO clients (name, email, phone) VALUES (%s, %s, %s)"
        if self.db_manager.execute_query(query, (name, email, phone)): self.clear_client_form(); self.load_clients()
        else: messagebox.showerror("Erro", "Falha ao adicionar cliente.")

    def update_client(self):
        client_id = self.client_id_entry.get()
        if not client_id: messagebox.showwarning("Seleção", "Selecione um cliente para atualizar."); return
        name, email, phone = self.client_name_entry.get(), self.client_email_entry.get(), self.client_phone_entry.get()
        query = "UPDATE clients SET name = %s, email = %s, phone = %s WHERE id = %s"
        if self.db_manager.execute_query(query, (name, email, phone, client_id)): self.clear_client_form(); self.load_clients()
        else: messagebox.showerror("Erro", "Falha ao atualizar cliente.")
    
    def delete_client(self):
        client_id = self.client_id_entry.get()
        if not client_id: messagebox.showwarning("Seleção", "Selecione um cliente para excluir."); return
        if messagebox.askyesno("Confirmar", "Tem certeza que deseja excluir este cliente?"):
            if self.db_manager.execute_query("DELETE FROM clients WHERE id = %s", (client_id,)): self.clear_client_form(); self.load_clients()
            else: messagebox.showerror("Erro", "Falha ao excluir cliente.")

    def on_client_select(self, event):
        selected_item = self.client_tree.focus()
        if not selected_item: return
        item_data = self.client_tree.item(selected_item)['values']
        self.clear_client_form()
        self.client_id_entry.insert(0, item_data[0]); self.client_name_entry.insert(0, item_data[1])
        self.client_email_entry.insert(0, item_data[2]); self.client_phone_entry.insert(0, item_data[3])
    
    def clear_client_form(self):
        self.client_id_entry.delete(0, 'end'); self.client_name_entry.delete(0, 'end')
        self.client_email_entry.delete(0, 'end'); self.client_phone_entry.delete(0, 'end')

    # --- LÓGICA DE VENDAS ---
    def load_sales(self):
        for item in self.sales_tree.get_children(): self.sales_tree.delete(item)
        query = """
            SELECT s.id, p.name, s.quantity, s.sale_date 
            FROM sales s JOIN products p ON s.product_id = p.id 
            ORDER BY s.sale_date DESC
        """
        sales = self.db_manager.fetch_all(query)
        for s in sales: self.sales_tree.insert("", "end", values=(s['id'], s['name'], s['quantity'], s['sale_date']))

    def add_sale(self):
        product_name = self.sale_product_combo.get()
        quantity_str = self.sale_quantity_entry.get()

        if not product_name or not quantity_str: messagebox.showwarning("Campos Vazios", "Selecione um produto e uma quantidade."); return
        
        try: quantity = int(quantity_str)
        except ValueError: messagebox.showerror("Erro", "Quantidade deve ser um número inteiro."); return

        # Buscar ID e estoque do produto
        product = self.db_manager.fetch_one("SELECT id, stock FROM products WHERE name = %s", (product_name,))
        if not product: messagebox.showerror("Erro", "Produto não encontrado."); return
        
        if product['stock'] < quantity: messagebox.showerror("Estoque Insuficiente", f"Estoque disponível: {product['stock']}"); return

        # Inserir venda e atualizar estoque
        sale_query = "INSERT INTO sales (product_id, quantity) VALUES (%s, %s)"
        stock_query = "UPDATE products SET stock = stock - %s WHERE id = %s"
        
        if self.db_manager.execute_query(sale_query, (product['id'], quantity)) and \
           self.db_manager.execute_query(stock_query, (quantity, product['id'])):
            messagebox.showinfo("Sucesso", "Venda registrada com sucesso!")
            self.sale_quantity_entry.delete(0, 'end')
            self.sale_product_combo.set('')
            self.load_sales(); self.load_products() # Recarrega produtos para mostrar novo estoque
        else:
            messagebox.showerror("Erro", "Falha ao registrar a venda. A transação foi revertida.")

    def plot_sales_graph(self):
        for widget in self.canvas_frame.winfo_children(): widget.destroy()
        query = """
            SELECT p.name, SUM(s.quantity) as total_quantity FROM sales s
            JOIN products p ON s.product_id = p.id
            GROUP BY p.name ORDER BY total_quantity DESC
        """
        sales_data = self.db_manager.fetch_all(query)
        if not sales_data: messagebox.showinfo("Sem Dados", "Não há vendas para gerar o gráfico."); return

        product_names = [item['name'] for item in sales_data]
        quantities = [item['total_quantity'] for item in sales_data]

        fig = Figure(figsize=(6, 4), dpi=100)
        ax = fig.add_subplot(111)
        ax.bar(product_names, quantities, color='skyblue')
        ax.set_title('Quantidade de Vendas por Produto'); ax.set_xlabel('Produto'); ax.set_ylabel('Quantidade Vendida')
        fig.autofmt_xdate()

        canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(expand=True, fill='both')