import subprocess
import os
import json
import shutil

def obter_extensao_video(json_info):
  try:
    data = json.loads(json_info)  # Converte a string JSON em um dicionário
    return data.get("ext", "")  # Retorna uma extensão ou uma string vazia se não existir
  except json.JSONDecodeError:
    return ""  # Retorna uma string vazia se houver erro na conversão

def obter_nome_video(json_info):
  try:
    data = json.loads(json_info)  # Converte a string JSON em um dicionário
    return data.get("fulltitle", "")  # Retorna o título do vídeo ou uma string vazia se não existir
  except json.JSONDecodeError:
    return ""  # Retorna uma string vazia se houver erro na conversão

def remover_caracteres_invalidos(nome_video):
    novo_nome = nome_video.replace(" ", "_")  # Substituir espaços por sublinhados
    novo_nome = novo_nome.replace(".", "")  # Substituir espaços por sublinhados
    novo_nome = novo_nome.replace("/", "")  # Remover barras
    novo_nome = novo_nome.replace("\\", "")  # Remover barras invertidas
    novo_nome = novo_nome.replace(">","")  # Remover sinal de maior
    novo_nome = novo_nome.replace("<","")  # Remover sinal de menor
    novo_nome = novo_nome.replace(":","")  # Remover sinal de dois pontos
    novo_nome = novo_nome.replace('"',"")  # Remover asterisco
    novo_nome = novo_nome.replace("|","")  # Remover ponto de interrogação
    novo_nome = novo_nome.replace("?","")  # Remover ponto de interrogação
    novo_nome = novo_nome.replace("*","")  # Remover asterisco
    return novo_nome

def baixar_video(link_video):
    arquivo = f"video" # Define o nome do arquivo

    if os.path.exists(arquivo):
        print(f"O arquivo {arquivo} já existe. Removendo...")
        os.remove(arquivo)
        print(f"Arquivo {arquivo} removido. Continuando...")

    # Comando yt-dlp para baixar o vídeo
    comando = [
        "yt-dlp",
        "--progress",
        "--restrict-filenames",
        "--write-info-json",
        "-o",
        arquivo,
        link_video
    ]

    # Executar o comando com Popen para capturar a saída em tempo real
    processo = subprocess.Popen(comando, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    # Ler a saída do processo em tempo real
    for linha in processo.stdout:
        # limpa a tela do terminal
        os.system("cls")
        print(linha, end="")  # Exibir a saída no terminal conforme ela ocorre

    # Aguardar o processo terminar e pegar o código de retorno
    processo.wait()

    # Verificar o código de retorno
    if processo.returncode != 0:
        print("Erro ao baixar o vídeo. Código de erro:", processo.returncode)
        return False
    
    ext = "" 
    # Passo 2: Obter a extensão do vídeo através do arquivo JSON
    with open(f"{arquivo}.info.json", "r", encoding="utf-8") as f:
        json_info = f.read()
        ext = obter_extensao_video(json_info)
    
    if ext == "":
        print("Extensão do vídeo não encontrada. Usando a extensão padrão 'mp4'.")
        ext = "mp4"

    # Passe 3: Obter o nome do vídeo através do arquivo JSON
    nome_video = ""
    with open(f"{arquivo}.info.json", "r", encoding="utf-8") as f:
        json_info = f.read()
        nome_video = remover_caracteres_invalidos(obter_nome_video(json_info))
    
    if nome_video == "":
        print("Nome do vídeo não encontrado. Usando o nome padrão 'video'.")
        nome_video = "video"

    # Passo 4: Verificar se existe uma pasta com o nome do vídeo dentro da pasta Downloads no diretório atual
    if os.path.exists(f"Downloads/{nome_video}"):
        print(f"A pasta '{nome_video}' já existe. Deseja substituí-la?")
        resposta = input("Digite 's' ou deixe em branco para substituir ou 'n' para cancelar: ")
        if resposta.lower() == "n":
            print("O download foi cancelado.")
            return False
        else:
            print(f"Removendo a pasta '{nome_video}'...")
            shutil.rmtree(f"Downloads/{nome_video}")

    # Passo 5: Renomear o arquivo para adicionar a extensão correta
    arquivo_completo = f"{arquivo}.{ext}"  # Nome completo do arquivo
    novo_nome = f"{nome_video}.{ext}"  # Novo nome do arquivo
    print(f"Renomeando o arquivo para: {novo_nome}")
    os.rename(arquivo_completo, novo_nome)

    # Passo 6: Remover o arquivo JSON
    os.remove(f"{arquivo}.info.json")

    # Passo 7: Verificar se o arquivo foi baixado corretamente 
    print(f"Verificando o arquivo baixado: {novo_nome}")
    
    if os.path.exists(novo_nome):
        print(f"Tamanho do arquivo: {os.path.getsize(novo_nome)} bytes")
    else:
        print("Arquivo não encontrado.")

    if os.path.exists(novo_nome) and os.path.getsize(novo_nome) > 0:
        print("\nDownload concluído com sucesso!")
        return novo_nome
    else:
        print("\nErro: Arquivo não encontrado ou está vazio.")
        return False

