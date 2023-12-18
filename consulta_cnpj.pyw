import tkinter as tk
from tkinter import filedialog
import requests
import re

data = {}  # Variável global para armazenar os dados do CNPJ

def obter_informacoes_cnpj():
    global data  # Acessa a variável global

    cnpj = entry_cnpj.get()
    cnpj = re.sub(r"\D", "", cnpj)
    
    if cnpj:
        limpar_campos() # Limpa os campos antes de inserir novas informações
        
        url = f"https://www.receitaws.com.br/v1/cnpj/{cnpj}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()

            text_info.delete("1.0", tk.END)

            text_info.config(state=tk.NORMAL)  # Habilita a edição do widget

            text_info.insert(tk.END, f"Informações para o CNPJ: {cnpj}\n\n")
            text_info.insert(tk.END, f"Abertura: {data['abertura']}\n")
            text_info.insert(tk.END, f"Nome: {data['nome']}\n")
            text_info.insert(tk.END, f"Fantasia: {data['fantasia']}\n")
            text_info.insert(tk.END, f"Situação: {data['situacao']}\n")
            text_info.insert(tk.END, f"Data da Situação: {data['data_situacao']}\n")
            text_info.insert(tk.END, f"E-mail: {data['email']}\n")
            text_info.insert(tk.END, f"Telefone: {data['telefone']}\n")
            text_info.insert(tk.END, f"\n")
            text_info.insert(tk.END, f"Atividade Principal: {data['atividade_principal'][0]['text']}\n")
            text_info.insert(tk.END, f"Atividades Secundárias: {', '.join([atividade['text'] for atividade in data['atividades_secundarias']])}\n")
            text_info.insert(tk.END, f"Natureza Jurídica: {data['natureza_juridica']}\n")
            text_info.insert(tk.END, f"Logradouro: {data['logradouro']}\n")
            text_info.insert(tk.END, f"Número: {data['numero']}\n")
            text_info.insert(tk.END, f"Complemento: {data['complemento']}\n")
            text_info.insert(tk.END, f"CEP: {data['cep']}\n")
            text_info.insert(tk.END, f"Bairro: {data['bairro']}\n")
            text_info.insert(tk.END, f"Município: {data['municipio']}\n")
            text_info.insert(tk.END, f"UF: {data['uf']}\n")
            text_info.insert(tk.END, f"Situação: {data['situacao']}\n")
            text_info.insert(tk.END, f"Data da Situação: {data['data_situacao']}\n")
            text_info.insert(tk.END, f"Motivo Situação: {data['motivo_situacao']}\n")
            text_info.insert(tk.END, f"Situação Especial: {data['situacao_especial']}\n")
            text_info.insert(tk.END, f"Data da Situação Especial: {data['data_situacao_especial']}\n")
            text_info.insert(tk.END, f"Capital Social: {data['capital_social']}\n")
            
            text_info.insert(tk.END, "QSA:\n")
            for qsa in data['qsa']:
                text_info.insert(tk.END, f"- Nome: {qsa['nome']} ({qsa['qual']})\n")

            ultima_atualizacao = data['ultima_atualizacao'].split('T')[0]
            text_info.insert(tk.END, f"Última Atualização: {ultima_atualizacao}\n")

            text_info.config(state=tk.DISABLED)  # Desabilita a edição do widget

def limpar_campos():
    global data
    text_info.config(state=tk.NORMAL)  # Habilita a edição do widget
    text_info.delete("1.0", tk.END)
    data = {}


def exportar_para_bloco_notas():
    texto = text_info.get("1.0", tk.END)

    if data:
        cnpj = entry_cnpj.get().strip()
        cnpj = re.sub(r"\D", "", cnpj)
        nome_empresa = data.get('fantasia') or data['nome']
        nome_empresa = nome_empresa.replace(" ", "_")
        nome_arquivo = f"Informações para o CNPJ {cnpj}_{nome_empresa}"

        path = filedialog.asksaveasfilename(defaultextension=".txt", initialfile=nome_arquivo, filetypes=[("Arquivo de Texto", "*.txt")])

        if path:
            with open(path, "w") as file:
                file.write(texto)


def exibir_info_label():
    if button_info_label["text"] == "Sobre":
        text_info_label.pack()
        button_info_label["text"] = "Ocultar"
    else:
        text_info_label.pack_forget()
        button_info_label["text"] = "Sobre"

window = tk.Tk()
window.title("Consulta de CNPJ")
window.geometry("600x460")

label_cnpj = tk.Label(window, text="CNPJ:")
label_cnpj.pack()

entry_cnpj = tk.Entry(window, width=20)
entry_cnpj.pack()

button_consultar = tk.Button(window, text="Consultar", command=obter_informacoes_cnpj)
button_consultar.pack(pady=5)

text_info_frame = tk.Frame(window)
text_info_frame.pack(pady=10)

text_info = tk.Text(text_info_frame, height=15)
text_info.pack()

button_exportar = tk.Button(window, text="Exportar para Bloco de Notas", command=exportar_para_bloco_notas)
button_exportar.pack(pady=10)

button_info_label = tk.Button(window, text="Sobre", command=exibir_info_label)
button_info_label.pack(pady=0, padx=10)  # Adiciona um espaçamento horizontal de 10 pixels

text_info_label = tk.Label(window, text="Versão 2 - 28/06/2023\n Dúvidas: eduardo.kochenn@gmail.com\n", wraplength=500)

# Adicione um label vazio com um espaçamento vertical para criar o espaço desejado

text_info.pack_propagate(0)

window.mainloop()

