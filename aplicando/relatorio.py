import sqlite3
import customtkinter as ctk

def gerar_relatorio(janela_principal):
    # Criação de uma nova janela para exibir o relatório
    relatorio_janela = ctk.CTkToplevel(janela_principal)
    relatorio_janela.geometry('300x400')
    relatorio_janela.title("Relatório de Usuários")
    
    # Conectar ao banco de dados
    conn = sqlite3.connect('user.db')
    cursor = conn.cursor()
    
    # Consultar todos os registros na tabela de usuários
    cursor.execute("SELECT * FROM user")
    usuarios = cursor.fetchall()
    
    # Exibir cada usuário na janela de relatório
    for idx, usuario in enumerate(usuarios):
        user_text = f"ID: {usuario[0]}, Login: {usuario[1]}, Senha: {usuario[2]}"
        ctk.CTkLabel(relatorio_janela, text=user_text).pack(pady=5)
    
    # Fechar a conexão com o banco de dados
    conn.close()