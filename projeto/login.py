import sqlite3 # importa o banco de dados
import customtkinter as ctk # importa o customtkinter e faço abreviação do nome 
from relatorio import gerar_relatorio # importa o relatorio 

# Conectar ao banco de dados (ou criar se não existir)
conn = sqlite3.connect('usuarios.db')
cursor = conn.cursor()

# Cria uma tabela de usuários se não existir
cursor.execute('''
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL,
    senha TEXT NOT NULL
)
''')
conn.commit()

# Cadastrar novo usuário
def nuser():
    def salvar_usuario():
        novo_email = email_entry.get()
        nova_senha = senha_entry.get()
        cursor.execute("INSERT INTO usuarios (email, senha) VALUES (?, ?)", 
                    (novo_email, nova_senha))
        conn.commit()
        print('Usuário cadastrado com sucesso!')
        cadastro_janela.destroy()
    
    cadastro_janela = ctk.CTkToplevel(janela)
    cadastro_janela.geometry('300x250')
    cadastro_janela.title("Cadastrar Novo Usuário")
    
    ctk.CTkLabel(cadastro_janela, text='Email:', font=femail).pack(pady=10)
    email_entry = ctk.CTkEntry(cadastro_janela, font=femail)
    email_entry.pack(pady=5)
    
    ctk.CTkLabel(cadastro_janela, text='Senha:', font=femail).pack(pady=10)
    senha_entry = ctk.CTkEntry(cadastro_janela, font=femail, show='*')
    senha_entry.pack(pady=5)
    
    ctk.CTkButton(cadastro_janela, text='Salvar', command=salvar_usuario).pack(pady=10)

# Validação de senha
def clickbtn():
    email_value = email.get()
    senha_value = senha.get()
    cursor.execute("SELECT * FROM usuarios WHERE email=? AND senha=?", (email_value, senha_value))
    result = cursor.fetchone()
    if result:
        print(f'Seja bem-vindo {email_value}')
    else:
        print('Senha incorreta! Tente novamente.')

# Função para verificar a senha de administrador
def verificar_senha_admin(senha_admin):
    senha_admin_correta = 'admin'
    return senha_admin == senha_admin_correta

# Criação da janela
janela = ctk.CTk()
janela.title("Bar do Zé")

# Dimensão da janela
janela.geometry('300x430')

# Estilo da fonte
fonte = ctk.CTkFont(family='urw geometric', size=20) # principal
femail = ctk.CTkFont(family='urw geometric', size=18) #email + senha
cbox = ctk.CTkFont(family='urw geometric', size=16) # checkbox

# Cabeçalho
titulo = ctk.CTkLabel(janela, text='🔥 zé'.upper(), font=fonte)
titulo.pack(padx=10, pady=10)

# Input de email
email = ctk.CTkEntry(janela, placeholder_text='Digite seu email'.upper(),
                    font=femail, width=180, height=32)
email.pack(padx=10, pady=10)

# Input de senha
senha = ctk.CTkEntry(janela, placeholder_text='Digite sua senha'.upper(),
                    show='*', font=femail, width=180, height=32)
senha.pack(padx=10, pady=10)

# Checkbox
check = ctk.CTkCheckBox(janela, text='Salvar senha'.upper(), font=cbox)
check.pack(padx=10, pady=10)

# Botão de login
btn = ctk.CTkButton(janela, text='Login'.upper(), command=clickbtn)
btn.pack(padx=10, pady=10)

# Botão de cadastrar novo usuário, vai abrir outra tela para cadastro
user = ctk.CTkButton(janela, text='Cadastrar'.upper(), command=nuser)
user.pack(padx=10, pady=10)

# Entrada de senha do administrador para gerar relatório
senha_admin_label = ctk.CTkLabel(janela, text='Senha de Administrador:',
                                font=femail)
senha_admin_label.pack(pady=5)

senha_admin_entry = ctk.CTkEntry(janela, font=femail, show='*')
senha_admin_entry.pack(pady=5)

# Botão para gerar relatório
def gerar_relatorio_admin():
    senha_admin = senha_admin_entry.get()
    if verificar_senha_admin(senha_admin):
        gerar_relatorio(janela)
    else:
        print('Senha de administrador incorreta!')

relatorio = ctk.CTkButton(janela, text='Relatório'.upper(), command=gerar_relatorio_admin)
relatorio.pack(padx=10, pady=10)

# Executar o loop principal da janela
janela.mainloop()

# Fechar a conexão com o banco de dados
conn.close()