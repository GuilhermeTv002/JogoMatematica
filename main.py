import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import time
import os
import sys
import json

# Caminho de arquivos
def caminho_arquivo(rel_path):
    base_path = sys._MEIPASS if getattr(sys, 'frozen', False) else os.path.abspath(".")
    return os.path.join(base_path, rel_path)

# Dados globais


tentativas = 0
max_tentativas = 6
tempo_inicio = None
tempo_pausado = 0
jogador_nome = ""
melhores_tempos = {}
jogo_pausado = False
jogo_finalizado = False
ingredientes_possiveis=[]


# Janela
janela = tk.Tk()
janela.title("Alquimia Suprema")
janela.geometry("400x600")
janela.resizable(False, False)
try:
    janela.iconbitmap(caminho_arquivo("imagens/logo.ico"))
except:
    pass

# Variáveis
tempo_var = tk.StringVar()
tentativas_var = tk.StringVar()
resultado_var = tk.StringVar()
melhor_tempo_var = tk.StringVar()
dificuldade = tk.StringVar(value="Escolha a dificuldade")
# Containers
frame_inicio = tk.Frame(janela)
frame_instrucao = tk.Frame(janela)
frame_jogo = tk.Frame(janela)
frame_pause = tk.Frame(janela)

variaveis_dropdowns = []
dropdowns = []

# ===== TELA INICIAL =====
def mostrar_tela_instrucao():
    frame_inicio.pack_forget()
    frame_instrucao.pack()

tk.Label(frame_inicio, text="🧪 Bem-vindo ao Alquimia Suprema!", font=("Arial", 16)).pack(pady=20)
tk.Button(frame_inicio, text="Jogar", command=mostrar_tela_instrucao).pack()
frame_inicio.pack()

# ===== TELA DE INSTRUÇÕES =====
nome_entry = tk.Entry(frame_instrucao)

descricao_dificuldade_var = tk.StringVar()
descricao_dificuldade_var.set("Selecione uma dificuldade.")

def atualizar_descricao_dificuldade(*args):
    nivel = dificuldade.get()
    if nivel == "Fácil":
        descricao_dificuldade_var.set("🟢 Fácil: 3 ingredientes disponíveis e 3 espaços para a poção. Você tem 10 tentativas.")
    elif nivel == "Média":
        descricao_dificuldade_var.set("🟡 Médio: 4 ingredientes disponíveis e 4 espaços para a poção. Você tem 7 tentativas.")
    elif nivel == "Difícil":
        descricao_dificuldade_var.set("🔴 Difícil: 5 ingredientes disponíveis e 5 espaços para a poção. Você tem 5 tentativas.")
    else:
        descricao_dificuldade_var.set("Selecione uma dificuldade.")
def iniciar_jogo():
    global jogador_nome, tempo_inicio, tentativas, ordem_correta, ingredientes_possiveis, max_tentativas,combinacoes_possiveis,jogo_ativo,jogo_finalizado,jogo_pausado
    jogo_ativo = True
    jogo_finalizado = False
    jogo_pausado = False
    jogador_nome = nome_entry.get().strip()
    if not jogador_nome:
        messagebox.showwarning("Nome obrigatório", "Digite seu nome antes de começar.")
        return

    # Ajustar a dificuldade
    if dificuldade.get() == "Fácil":
        combinacoes_possiveis = 3
        ingredientes_possiveis = ['Sangue de Barata', 'Pó de Fada', 'Dente de Morcego']
        ordem_correta = random.sample(ingredientes_possiveis, combinacoes_possiveis)  # 3 combinações
        max_tentativas = 10  # 10 tentativas
    elif dificuldade.get() == "Média":
        combinacoes_possiveis = 4
        ingredientes_possiveis = ['Sangue de Barata', 'Pó de Fada', 'Dente de Morcego', 'Baba de Dragão']
        ordem_correta = random.sample(ingredientes_possiveis, combinacoes_possiveis)  # 4 combinações
        max_tentativas = 7  # 7 tentativas
    elif dificuldade.get() == "Difícil":
        combinacoes_possiveis = 5
        ingredientes_possiveis = ['Sangue de Barata', 'Pó de Fada', 'Dente de Morcego', 'Baba de Dragão', 'Raiz Mágica']
        ordem_correta = random.sample(ingredientes_possiveis, combinacoes_possiveis)  # 5 combinações
        max_tentativas = 5  # 5 tentativas

        
    tentativas = 0
    tempo_inicio = time.time()
    
    tentativas_var.set(f"🎯 Tentativas: 0/{max_tentativas}")
    resultado_var.set("")
    melhor_tempo_var.set(f"🏆 Melhor tempo: {carregar_melhor_tempo(jogador_nome)} segundos")
    atualizar_caldeirao()
    
    for dropdown in dropdowns:
        dropdown.destroy()
    variaveis_dropdowns.clear()
    dropdowns.clear()

    frame_instrucao.pack_forget()
    frame_jogo.pack()
    atualizar_tempo()
    
    for i in range(combinacoes_possiveis):
        var = tk.StringVar()
        var.set(ingredientes_possiveis[i % len(ingredientes_possiveis)])
        variaveis_dropdowns.append(var)

        menu = tk.OptionMenu(frame_jogo, var, *ingredientes_possiveis)
        menu.pack()
        dropdowns.append(menu)

tk.Label(frame_instrucao, text="📜 Instruções:", font=("Arial", 14)).pack(pady=10)
tk.Label(frame_instrucao, text="Descubra a combinação correta de ingredientes mágicos!").pack(pady=5)
tk.Label(frame_instrucao, text="Digite seu nome:").pack(pady=5)
nome_entry.pack(pady=5)

tk.Label(frame_instrucao, text="Escolha a dificuldade:").pack(pady=5)
tk.OptionMenu(frame_instrucao, dificuldade, "Fácil", "Média", "Difícil", command=atualizar_descricao_dificuldade).pack(pady=5)
tk.Label(frame_instrucao, textvariable=descricao_dificuldade_var, wraplength=300).pack(pady=5)
tk.Button(frame_instrucao, text="Começar", command=iniciar_jogo).pack(pady=10)

# ===== TELA DE PAUSE =====
def pausar_jogo(event=None):
    global jogo_pausado, tempo_pausado
    if frame_jogo.winfo_ismapped() and not jogo_pausado:
        jogo_pausado = True
        tempo_pausado = time.time()
        frame_pause.place(relx=0.5, rely=0.5, anchor="center")
        desabilitar_interacao(True)

def continuar_jogo():
    global jogo_pausado, tempo_inicio
    jogo_pausado = False
    delta = time.time() - tempo_pausado
    tempo_inicio += delta
    frame_pause.place_forget()
    desabilitar_interacao(False)

def reiniciar_jogo():
    global jogo_pausado, tempo_inicio, jogo_ativo
    delta = time.time() - tempo_pausado
    tempo_inicio += delta
    frame_pause.place_forget()
    desabilitar_interacao(False)
    iniciar_jogo()
    
def sair_jogo():
    janela.destroy()

tk.Label(frame_pause, text="⏸️ Jogo pausado", font=("Arial", 16)).pack(pady=10)
tk.Button(frame_pause, text="Continuar", command=continuar_jogo).pack(pady=5)
tk.Button(frame_pause, text="Sair", command=sair_jogo).pack(pady=5)
tk.Button(frame_pause, text="Reiniciar", command=reiniciar_jogo).pack(pady=5)

# ===== TELA DO JOGO =====
def atualizar_tempo():
    if not jogo_pausado and not jogo_finalizado and frame_jogo.winfo_ismapped():
        tempo_decorrido = int(time.time() - tempo_inicio)
        minutos = tempo_decorrido // 60
        segundos = tempo_decorrido % 60
        tempo_var.set(f"⏱️ Tempo: {minutos:02d}:{segundos:02d}")
    janela.after(1000, atualizar_tempo)

def desabilitar_interacao(status):
    estado = "disabled" if status else "normal"
    for widget in dropdowns + [botao_misturar]:
        widget.config(state=estado)

def atualizar_caldeirao(status="erro"):
    global tentativas
    if status == "vitoria":
        img = "Caldeirao_Vitoria.png"
    elif status == "perdeu":
        img = "Caldeirao_Perdeu.png"
    else:
        img = f"Caldeirao_{tentativas}.png"

    caminho = caminho_arquivo(f"imagens/{img}")
    if os.path.exists(caminho):
        imagem = Image.open(caminho).resize((200, 200))
        imagem_tk = ImageTk.PhotoImage(imagem)
        caldeirao_label.config(image=imagem_tk)
        caldeirao_label.image = imagem_tk
        
def verificar_combinação():
    global tentativas,tempo_inicio, tempo_pausado, jogo_ativo, jogo_finalizado
    if tentativas >= max_tentativas or jogo_pausado or jogo_finalizado:
        return

    tentativa = [var.get() for var in variaveis_dropdowns]

    tentativas += 1
    tentativas_var.set(f"🎯 Tentativas: {tentativas}/{max_tentativas}")

    corretos = sum(tentativa[i] == ordem_correta[i] for i in range(len(ordem_correta)))
    presentes = sum(i in ordem_correta for i in tentativa)

    if tentativa == ordem_correta:
        jogo_finalizado = True
        tempo_total = int(time.time() - tempo_inicio)
        resultado_var.set(f"✨ Você criou a poção perfeita em {tempo_total} segundos!")
        atualizar_caldeirao("vitoria")
        salvar_melhor_tempo(tempo_total)
        if messagebox.askyesno("Parabéns!", "Deseja jogar novamente?"):
            iniciar_jogo()
        else:
            jogo_ativo=False
            tempo_pausado=time.time() - tempo_inicio
    else:
        reacoes = [
            "Mistura muito instável!",
            "Reação fizzing errada!",
            "Poção com efeito bizarro!",
            "Poção de invisibilidade falhou!",
            "O caldeirão quase explodiu!"
        ]
        resultado_var.set(f"{random.choice(reacoes)}\n{corretos} corretos, {presentes - corretos} fora de ordem.")
        atualizar_caldeirao()

        if tentativas == max_tentativas:
            resultado_var.set("💥 O caldeirão explodiu!")
            atualizar_caldeirao("perdeu")
            jogo_ativo = False  # Congelar o tempo
            jogo_finalizado=True
            tempo_pausado = time.time() - tempo_inicio  # Armazenar tempo final
            if messagebox.askyesno("Game Over", "Deseja tentar novamente?"):
                iniciar_jogo()
                

# Dropdowns

botao_misturar = tk.Button(frame_jogo, text="Misturar!", command=verificar_combinação)
botao_misturar.pack(pady=10)

tk.Label(frame_jogo, textvariable=resultado_var, wraplength=300, fg="purple").pack(pady=5)
tk.Label(frame_jogo, textvariable=tempo_var, fg="blue").pack()
tk.Label(frame_jogo, textvariable=tentativas_var, fg="green").pack()
tk.Label(frame_jogo, textvariable=melhor_tempo_var, fg="orange").pack()

caldeirao_label = tk.Label(frame_jogo)
caldeirao_label.pack(pady=10)



# ===== SALVAR TEMPO =====
def salvar_melhor_tempo(novo_tempo):
    arquivo = "melhores_tempos.json"
    tempos = {}
    if os.path.exists(arquivo):
        with open(arquivo, "r") as f:
            tempos = json.load(f)

    anterior = tempos.get(jogador_nome)
    if anterior is None or novo_tempo < anterior:
        tempos[jogador_nome] = novo_tempo
        with open(arquivo, "w") as f:
            json.dump(tempos, f)
        melhor_tempo_var.set(f"🏆 Melhor tempo: {carregar_melhor_tempo(jogador_nome)} segundos")

def carregar_melhor_tempo(nome):
    if os.path.exists("melhores_tempos.json"):
        with open("melhores_tempos.json", "r") as f:
            tempos = json.load(f)
            return tempos.get(nome, "N/A")
    return "N/A"

# Tecla ESC ativa o pause
janela.bind("<Escape>", pausar_jogo)

# Rodar janela
janela.mainloop()
