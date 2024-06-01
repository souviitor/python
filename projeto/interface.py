import tkinter as tk
from tkinter import messagebox
import sqlite3

# Conectar ao banco de dados (ou criar se não existir)
conn = sqlite3.connect('usuarios.db')
cursor = conn.cursor()

# Criar uma tabela de usuários se não existir
cursor.execute('''
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL,
    senha TEXT NOT NULL
)
''')
conn.commit()

# Função para cadastrar novo usuário
def cadastrar_usuario():
    def salvar_usuario():
        novo_email = email_entry.get()
        nova_senha = senha_entry.get()
        cursor.execute("INSERT INTO usuarios (email, senha) VALUES (?, ?)", (novo_email, nova_senha))
        conn.commit()
        messagebox.showinfo("Cadastro", "Usuário cadastrado com sucesso!")
        cadastro_janela.destroy()
    
    cadastro_janela = tk.Toplevel(janela)
    cadastro_janela.geometry('300x300')
    cadastro_janela.title("Cadastrar Novo Usuário")
    
    tk.Label(cadastro_janela, text='Email:', font=('Arial', 12, 'bold')).pack(pady=10)
    email_entry = tk.Entry(cadastro_janela, font=('Arial', 12))
    email_entry.pack(pady=5)
    
    tk.Label(cadastro_janela, text='Senha:', font=('Arial', 12, 'bold')).pack(pady=10)
    senha_entry = tk.Entry(cadastro_janela, show='*', font=('Arial', 12))
    senha_entry.pack(pady=5)
    
    tk.Button(cadastro_janela, text='Salvar', command=salvar_usuario, font=('Arial', 12, 'bold')).pack(pady=10)

# Função para verificar login
def fazer_login():
    email_value = email.get()
    senha_value = senha.get()
    cursor.execute("SELECT * FROM usuarios WHERE email=? AND senha=?", (email_value, senha_value))
    result = cursor.fetchone()
    if result:
        messagebox.showinfo("Login", f"Seja bem-vindo {email_value}")
    else:
        messagebox.showerror("Login", "Email ou senha incorretos!")

# Criar a janela principal
janela = tk.Tk()
janela.title("Bar do Zé")
janela.geometry('400x500')
janela.configure(bg='#ff9933')

# Widgets da interface gráfica
titulo_label = tk.Label(janela, text='🔥 Zé', font=('Helvetica', 36, 'bold'), bg='#ff9933')
titulo_label.pack(pady=20)

email_label = tk.Label(janela, text='Email:', font=('Arial', 14, 'bold'), bg='#ff9933')
email_label.pack(pady=10)
email = tk.Entry(janela, font=('Arial', 12))
email.pack(pady=5)

senha_label = tk.Label(janela, text='Senha:', font=('Arial', 14, 'bold'), bg='#ff9933')
senha_label.pack(pady=10)
senha = tk.Entry(janela, show='*', font=('Arial', 12))
senha.pack(pady=5)

login_btn = tk.Button(janela, text='Login', command=fazer_login, font=('Arial', 14, 'bold'))
login_btn.pack(pady=20)

cadastro_btn = tk.Button(janela, text='Cadastrar Novo Usuário', command=cadastrar_usuario, font=('Arial', 12, 'bold'))
cadastro_btn.pack(pady=10)

# Executar o loop principal da janela
janela.mainloop()

# Fechar a conexão com o banco de dados
conn.close()
