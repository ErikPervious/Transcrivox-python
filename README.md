# 🎥 Extrator de vídeo, áudio e texto  
Projeto em python que baixa vídeos do YouTube, extrai o áudio e converte em texto.

## 📝 Funcionalidades

- Baixar vídeos do YouTube  
- Extrair áudio de vídeos  
- Converter áudio em texto  

## 🛠️ Requisitos

Antes de iniciar, verifique se possui os seguintes componentes instalados:

- Python 3.x  
- yt-dlp (necessário para baixar vídeos do YouTube)  
  - O `yt-dlp` pode ser obtido [aqui](https://github.com/yt-dlp/yt-dlp?tab=readme-ov-file#installation).  
- moviepy (`pip install moviepy`)  
- SpeechRecognition (`pip install SpeechRecognition`)  
- pydub (`pip install pydub`)  
- ffmpeg (necessário para manipular áudio e vídeo)  
  - O `ffmpeg` pode ser obtido [aqui](https://ffmpeg.org/download.html) ou instalado via gerenciador de pacotes como o [choco](https://community.chocolatey.org/packages/ffmpeg).

## 🚀 Como Utilizar

1. Clone este repositório:
   ```bash
   git clone https://github.com/ErikPervious/video-extractor.git
   ```
2. Acesse a pasta do projeto:
   ```bash
   cd video-extractor
   ```
3. Execute o arquivo main.py:
   ```bash
   python main.py
   ```
4. Informe o link para download quando solicitado.
5. Escolha entre as opções disponíveis: salvar vídeo, texto, áudio ou todos.
6. Aguarde a criação da pasta `downloads`, que conterá subpastas nomeadas para cada vídeo.

## 📂 Estrutura do Projeto

```
├── src/[nome_do_video]/          # Pasta do vídeo baixado
├──── [nome_do_video].[formato]   # Vídeo baixado
├──── [nome_do_video].wav         # Áudio extraído
├──── [nome_do_video].txt         # Texto extraído
├── main.py                       # Script principal
├── baixar_video.py               # Função para baixar vídeos
├── README.md                     # Documentação do projeto
```

## 🛡️ Licenciamento

Este projeto está sob a licença MIT. Consulte o arquivo LICENSE para mais informações.