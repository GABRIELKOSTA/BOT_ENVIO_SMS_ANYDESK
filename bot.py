# Para iniciar, digite no terminal: python bot.py

import pyautogui
import time
import pyperclip
import random

pyautogui.FAILSAFE = True


# -----------------------------
# Funções de reconhecimento
# -----------------------------

def encontrar(img):
    try:
        return pyautogui.locateCenterOnScreen(img, confidence=0.75)
    except pyautogui.ImageNotFoundException:
        return None


def procurar_varios(imgs, tempo=5):

    inicio = time.time()

    while time.time() - inicio < tempo:

        for img in imgs:

            try:
                pos = pyautogui.locateCenterOnScreen(img, confidence=0.75)

                if pos:
                    return img, pos

            except pyautogui.ImageNotFoundException:
                pass

        time.sleep(0.5)

    return None, None


def clicar_varios(imgs, tempo=5):

    img, pos = procurar_varios(imgs, tempo)

    if pos:
        pyautogui.click(pos)
        time.sleep(1)
        return True

    return False


# -----------------------------
# Carregar dados
# -----------------------------

with open("numeros.txt", "r", encoding="utf-8") as f:
    numeros = [n.strip() for n in f]


# mensagens RCS
with open("mensagem.txt", "r", encoding="utf-8") as f:
    mensagens_rcs = f.read().split("\n---\n")


# mensagens SMS
with open("mensagem2.txt", "r", encoding="utf-8") as f:
    mensagens_sms = f.read().split("\n---\n")


print("Começando em 5 segundos...")
time.sleep(5)


# -----------------------------
# Loop principal
# -----------------------------

for numero in numeros:

    tentativas = 0
    enviado = False

    while not enviado and tentativas < 3:

        tentativas += 1
        print(f"Tentativa {tentativas} enviando para: {numero}")


        # iniciar chat
        if not clicar_varios([
            "imagens/iniciar_chat.png"
        ]):
            print("Erro ao abrir iniciar chat")
            continue


        # campo numero
        if not clicar_varios([
            "imagens/campo_numero.png"
        ]):
            print("Erro ao encontrar campo numero")
            continue


        pyautogui.write(numero)
        time.sleep(2)

        pyautogui.press("enter")
        time.sleep(2)


        # detectar tipo de chat
        img_detectada, pos = procurar_varios([
            "imagens/selecionar_mensagem.png",
            "imagens/selecionar_mensagem2.png"
        ], 5)


        if pos is None:

            print("Tela incorreta detectada, voltando...")

            clicar_varios([
                "imagens/voltar.png"
            ])

            time.sleep(2)
            continue


        pyautogui.click(pos)
        time.sleep(2)


        # escolher mensagem baseada no tipo

        if "selecionar_mensagem2" in img_detectada:

            mensagem = random.choice(mensagens_sms)
            print("Tipo detectado: SMS")

        else:

            mensagem = random.choice(mensagens_rcs)
            print("Tipo detectado: RCS")


        pyperclip.copy(mensagem)


        # campo mensagem
        pyautogui.click(800,900)
        time.sleep(0.5)

        pyautogui.click(800,900)
        time.sleep(1)


        # segurar campo mensagem
        if not clicar_varios([
            "imagens/segurar_mensagem.png",
            "imagens/segurar_mensagem2.png"
        ]):

            print("Erro ao encontrar campo mensagem")

            clicar_varios([
                "imagens/voltar.png"
            ])

            continue


        pyautogui.mouseDown()
        time.sleep(1.5)
        pyautogui.mouseUp()

        time.sleep(1)


        # colar
        if not clicar_varios([
            "imagens/colar.png"
        ]):

            print("Erro ao encontrar botão colar")

            clicar_varios([
                "imagens/voltar.png"
            ])

            continue


        # enviar
        if not clicar_varios([
            "imagens/enviar.png"
        ]):

            print("Erro ao encontrar botão enviar")

            clicar_varios([
                "imagens/voltar.png"
            ])

            continue


        time.sleep(3)


        # voltar
        clicar_varios([
            "imagens/voltar.png"
        ])

        time.sleep(2)

        enviado = True


    if not enviado:
        print(f"Falha após 3 tentativas: {numero}")


print("Finalizado")