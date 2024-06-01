import sqlite3
import customtkinter as ctk
from relatorio import gerar_relatorio
import openpyxl
import datetime
from tkinter import filedialog 

bdUser = sqlite3.connect('user.db')
cursor = bdUser.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user TEXT NOT NULL,
    password TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')
bdUser.commit()

def exportToExcel():
    # Abrir o diálogo para salvar o arquivo
    filename = filedialog.asksaveasfilename(defaultextension='.xlsx',
                                            filetypes=[('Excel files', '*.xlsx')],
                                            title='Salvar arquivo xlsx como...')

    if not filename:  # Verificar se o usuário cancelou
        return

    # Conexão com o banco de dados
    bdUser = sqlite3.connect('user.db')
    cursor = bdUser.cursor()

    # Criar o arquivo xlsx e adicionar uma planilha
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = 'Usuários'

    # Executar a consulta SQL para obter os dados
    cursor.execute('SELECT * FROM user')
    usuarios = cursor.fetchall()

    # Adicionar os dados na planilha
    sheet['A1'] = 'ID'
    sheet['B1'] = 'Usuário'
    sheet['C1'] = 'Senha'

    for i, usuario in enumerate(usuarios, start=2):
        sheet[f'A{i}'] = usuario[0]  # ID
        sheet[f'B{i}'] = usuario[1]  # Usuário
        sheet[f'C{i}'] = usuario[2]  # Senha

    # Salvar o arquivo xlsx com o nome escolhido pelo usuário
    workbook.save(filename)


#função dos botoes
# Cadastro de novo usuário
def newUser():
    def cad():
        nUser = user_entry.get()  # Pega o novo usuário
        nPass = pass_entry.get()  # Pega a nova password
        created_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Data atual
        
        # Verificar se o usuário já existe no banco de dados
        cursor.execute('SELECT * FROM user WHERE user = ?', (nUser,))
        existing_user = cursor.fetchone()
        
        if existing_user:
            print('Usuário já existe. Tente outro nome de usuário.')
        else:
            cursor.execute('INSERT INTO user (user, password, created_at) VALUES (?, ?, ?)', (nUser, nPass, created_at))
            bdUser.commit()
            print('Usuário cadastrado')
            cadastroJanela.destroy()

    cadastroJanela = ctk.CTkToplevel(janela)
    cadastroJanela.geometry('300x250')
    cadastroJanela.title('Cadastrar novo usuário'.upper())

    # Novo usuário label e entry
    ctk.CTkLabel(cadastroJanela, text='Usuário', font=fTexto).pack(pady=5)
    user_entry = ctk.CTkEntry(cadastroJanela, placeholder_text='Novo Usuário', font=finput)
    user_entry.pack(pady=5)

    # Nova senha label e entry
    ctk.CTkLabel(cadastroJanela, text='Senha', font=fTexto).pack(pady=5)
    pass_entry = ctk.CTkEntry(cadastroJanela, placeholder_text='Nova senha', font=finput, show=' ')
    pass_entry.pack(pady=5)

    #  Botão de salvar
    ctk.CTkButton(cadastroJanela, text='Salvar', command=cad).pack(pady=10)

# validação de login para acessar o portal
def btnLog():
  nUser = user.get()
  nPass = password.get()
  cursor.execute('SELECT * FROM user WHERE user = ? and password = ?', (nUser, nPass))
  resultado = cursor.fetchone()
  if resultado:
    print(f'Seja bem-vindo {nUser}')
  else:
    print('Login ou senha invalidos! Tente novamente.')
    
def verificarSenhaAdmin(senhaAdmin):
  senhaCorreta = 'admin'
  return senhaAdmin == senhaCorreta

# atribuição de janela + dimenssionamento + titulo
janela = ctk.CTk()
janela.geometry('300x450')
janela.title('Import Express'.upper())

# estilização de fonte
fTexto = ctk.CTkFont(family='urw geometric', size=18, weight='bold') # principal
finput = ctk.CTkFont(family='urw geometric', size=15, weight='normal') #INPUT

# 'h1' da janela
texto = ctk.CTkLabel(janela, text='import express'.upper(), font=fTexto)
texto.pack(padx=10, pady=10)

#campo de usuário
user = ctk.CTkEntry(janela, placeholder_text='Digite o seu usuário.', font=finput)
user.pack(padx=10, pady=10)

#campo de senha
password = ctk.CTkEntry(janela, placeholder_text='Digite sua senha.',
                        show=' ', font=finput)
password.pack(padx=10, pady=10)

# checkbox para manter salva a senha
login = ctk.CTkCheckBox(janela, text='Salvar senha'.upper()).pack(padx=10, pady=10)

#botoes
btnLogin = ctk.CTkButton(janela, text='login'.upper(),
                        command=btnLog).pack(padx=1, pady=10)

btnNuser = ctk.CTkButton(janela, text='Cadastrar usuário'.upper(), 
                        command=newUser).pack(padx=10, pady=10)

#gerar relatorio
def btnRelatorio():
  senha_admin = passRelatorio.get()
  if verificarSenhaAdmin(senha_admin):
    gerar_relatorio(janela)
  else:
    print('Senha incorreta, tente novamente!')

passRelatorio = ctk.CTkEntry(janela, placeholder_text='Senha admin',
                            show=' ')
passRelatorio.pack(padx=10, pady=10)
btnRel = ctk.CTkButton(janela, text='Gerar relátorio'.upper(),
                        font=finput, command=btnRelatorio).pack(padx=10, pady=10)

btnExport = ctk.CTkButton(janela, text='Exportar para Excel'.upper(),
                          font=finput, command=exportToExcel).pack(padx=10, pady=10)


# finaliza a janela
janela.mainloop()
# finaliza o banco de dados
bdUser.close()