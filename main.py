import tkinter as tk
from tkinter import messagebox
import random
import time

ingredientes_possiveis = ['Raiz Mágica', 'Líquido da Lua', 'Pó de Fada', 'Flor Enfeitiçada']
ordem_correta = random.sample(ingredientes_possiveis, 4)
tentativas = 0
tempo_inicio = time.time()

def atualizar_tempo():
    tempo_decorrido = int(time.time() - tempo_inicio)
    minutos = tempo_decorrido // 60
    segundos = tempo_decorrido % 60
    tempo_var.set(f"⏱️ Tempo: {minutos:02d}:{segundos:02d}")
    janela.after(1000, atualizar_tempo)

def verificar_combinação():
    global tentativas
    tentativa = [var1.get(), var2.get(), var3.get(), var4.get()]
    tentativas += 1
    tentativas_var.set(f"🎯 Tentativas: {tentativas}")
    
    corretos = sum([tentativa[i] == ordem_correta[i] for i in range(4)])
    presentes = sum([ingrediente in ordem_correta for ingrediente in tentativa])
    
    texto = ""
    if tentativa == ordem_correta:
        texto = f"✨ Parabéns! Você criou a poção perfeita em {tentativas} tentativas! ✨"
        messagebox.showinfo("Vitória!", texto)
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

# Janela principal
janela = tk.Tk()
janela.title("Alquimia Suprema")

tk.Label(janela, text="Escolha os ingredientes na ordem correta:").pack()

opcoes = ingredientes_possiveis[:]
var1 = tk.StringVar(value=opcoes[0])
var2 = tk.StringVar(value=opcoes[1])
var3 = tk.StringVar(value=opcoes[2])
var4 = tk.StringVar(value=opcoes[3])

for i, var in enumerate([var1, var2, var3, var4]):
    tk.OptionMenu(janela, var, *ingredientes_possiveis).pack()

tk.Button(janela, text="Misturar!", command=verificar_combinação).pack(pady=10)

resultado_var = tk.StringVar()
tk.Label(janela, textvariable=resultado_var, fg="purple", wraplength=300).pack(pady=5)

# Tempo e tentativas
tempo_var = tk.StringVar(value="⏱️ Tempo: 00:00")
tk.Label(janela, textvariable=tempo_var, fg="blue").pack()

tentativas_var = tk.StringVar(value="🎯 Tentativas: 0")
tk.Label(janela, textvariable=tentativas_var, fg="green").pack()

# Inicia o cronômetro
atualizar_tempo()

janela.mainloop()
