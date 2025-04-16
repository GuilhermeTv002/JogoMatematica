import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import time
import os
import sys

ingredientes_possiveis = ['Raiz Mágica', 'Líquido da Lua', 'Pó de Fada', 'Flor Enfeitiçada']
ordem_correta = random.sample(ingredientes_possiveis, 4)
tentativas = 0
max_tentativas = 6
tempo_inicio = time.time()

# Função para obter o caminho correto dos arquivos, mesmo no .exe
def caminho_arquivo(rel_path):
    """Retorna o caminho correto, mesmo se o app estiver empacotado"""
    base_path = sys._MEIPASS if getattr(sys, 'frozen', False) else os.path.abspath(".")
    return os.path.join(base_path, rel_path)

# Janela principal
janela = tk.Tk()
janela.title("Alquimia Suprema")

# Ícone da janela
try:
    janela.iconbitmap(caminho_arquivo("imagens/logo.ico"))
except Exception as e:
    print("Erro ao carregar o ícone:", e)

# Função para reiniciar o jogo
def reiniciar_jogo():
    global ordem_correta, tentativas, tempo_inicio
    ordem_correta = random.sample(ingredientes_possiveis, 4)
    tentativas = 0
    tempo_inicio = time.time()
    tentativas_var.set(f"🎯 Tentativas: 0/{max_tentativas}")
    resultado_var.set("")
    atualizar_caldeirao()
    var1.set(ingredientes_possiveis[0])
    var2.set(ingredientes_possiveis[1])
    var3.set(ingredientes_possiveis[2])
    var4.set(ingredientes_possiveis[3])

# Função para atualizar o tempo
def atualizar_tempo():
    tempo_decorrido = int(time.time() - tempo_inicio)
    minutos = tempo_decorrido // 60
    segundos = tempo_decorrido % 60
    tempo_var.set(f"⏱️ Tempo: {minutos:02d}:{segundos:02d}")
    janela.after(1000, atualizar_tempo)

# Função para atualizar a imagem do caldeirão
def atualizar_caldeirao(status="erro"):
    global tentativas
    if status == "vitoria":
        nome_imagem = caminho_arquivo("imagens/Caldeirao_Vitoria.png")
    elif status == "perdeu":
        nome_imagem = caminho_arquivo("imagens/Caldeirao_Perdeu.png")
    else:
        nome_imagem = caminho_arquivo(f"imagens/Caldeirao_{tentativas}.png")

    if os.path.exists(nome_imagem):
        imagem = Image.open(nome_imagem)
        imagem = imagem.resize((200, 200))
        imagem_tk = ImageTk.PhotoImage(imagem)
        caldeirao_label.config(image=imagem_tk)
        caldeirao_label.image = imagem_tk

# Função principal de verificação
def verificar_combinação():
    global tentativas
    if tentativas >= max_tentativas:
        return

    tentativa = [var1.get(), var2.get(), var3.get(), var4.get()]
    tentativas += 1
    tentativas_var.set(f"🎯 Tentativas: {tentativas}/{max_tentativas}")

    corretos = sum([tentativa[i] == ordem_correta[i] for i in range(4)])
    presentes = sum([ingrediente in ordem_correta for ingrediente in tentativa])

    if tentativa == ordem_correta:
        texto = f"✨ Parabéns! Você criou a poção perfeita em {tentativas} tentativas! ✨"
        resultado_var.set(texto)
        atualizar_caldeirao("vitoria")
        if messagebox.askyesno("Vitória!", f"{texto}\n\nDeseja jogar novamente?"):
            reiniciar_jogo()
    else:
        reações = [
            "Mistura muito instável!",
            "Reação fizzing errada!",
            "Poção com efeito bizarro!",
            "Poção de invisibilidade falhou: você ainda está visível!",
            "O caldeirão quase explodiu!"
        ]
        texto = f"{random.choice(reações)}\n"
        texto += f"{corretos} ingredientes na posição correta.\n"
        texto += f"{presentes - corretos} ingredientes presentes, mas fora de ordem."
        resultado_var.set(texto)
        atualizar_caldeirao()

        if tentativas == max_tentativas:
            resultado_var.set("💥 O caldeirão explodiu! A poção foi perdida...")
            atualizar_caldeirao("perdeu")
            if messagebox.askyesno("Perdeu!", f"{texto}\n\nDeseja jogar novamente?"):
                reiniciar_jogo()

# Layout da interface
tk.Label(janela, text="Escolha os ingredientes na ordem correta:").pack()

opcoes = ingredientes_possiveis[:]
var1 = tk.StringVar(value=opcoes[0])
var2 = tk.StringVar(value=opcoes[1])
var3 = tk.StringVar(value=opcoes[2])
var4 = tk.StringVar(value=opcoes[3])

for var in [var1, var2, var3, var4]:
    tk.OptionMenu(janela, var, *ingredientes_possiveis).pack()

tk.Button(janela, text="Misturar!", command=verificar_combinação).pack(pady=10)

resultado_var = tk.StringVar()
tk.Label(janela, textvariable=resultado_var, fg="purple", wraplength=300).pack(pady=5)

tempo_var = tk.StringVar(value="⏱️ Tempo: 00:00")
tk.Label(janela, textvariable=tempo_var, fg="blue").pack()

tentativas_var = tk.StringVar(value=f"🎯 Tentativas: 0/{max_tentativas}")
tk.Label(janela, textvariable=tentativas_var, fg="green").pack()

# Imagem inicial
caldeirao_label = tk.Label(janela)
caldeirao_label.pack(pady=10)
atualizar_caldeirao()

# Inicia o cronômetro
atualizar_tempo()

# Executa a janela
janela.mainloop()
