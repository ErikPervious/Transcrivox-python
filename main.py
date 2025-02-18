from baixar_video import baixar_video
from moviepy import VideoFileClip
from pydub import AudioSegment
import speech_recognition as sr
import os
import math

def extrair_audio(video_path, audio_path):
    video = VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path)
    video.close()

def converter_audio(input_path, output_path):
    audio = AudioSegment.from_file(input_path)
    audio.export(output_path, format="wav")

def transcrever_chunk(audio_segment, start_ms, end_ms, recognizer, i, total_chunks):
    chunk = audio_segment[start_ms:end_ms]
    temp_chunk_path = f"temp_chunk_{i}.wav"
    chunk.export(temp_chunk_path, format="wav")
    progress_split = ((i + 1) / total_chunks) * 100
    print(f"Dividindo áudio: {progress_split:.1f}% concluído.", end="\r")
    
    with sr.AudioFile(temp_chunk_path) as source:
        audio = recognizer.record(source)
    try:
        texto = recognizer.recognize_google(audio, language="pt-BR")
    except sr.UnknownValueError:
        print(f"\nChunk {i + 1}: Não foi possível entender o áudio.")
        texto = ""
    except sr.RequestError as e:
        print(f"\nChunk {i + 1}: Erro ao solicitar resultados; {e}")
        texto = ""
    os.remove(temp_chunk_path)
    progress_conv = ((i + 1) / total_chunks) * 100
    print(f"Convertendo áudio: {progress_conv:.1f}% concluído.", end="\r")
    return texto

def transcrever_audio(audio_path):
    import concurrent.futures

    SIZE_LIMIT = 9 * 1024 * 1024  # 9MB
    file_size = os.path.getsize(audio_path)
    recognizer = sr.Recognizer()

    # Caso o arquivo esteja dentro do limite, transcreve normalmente
    if file_size <= SIZE_LIMIT:
        with sr.AudioFile(audio_path) as source:
            audio = recognizer.record(source)
        try:
            texto = recognizer.recognize_google(audio, language="pt-BR")
            print("Conversão completa: 100%")
            return texto
        except sr.UnknownValueError:
            print("Não foi possível entender o áudio.")
            return None
        except sr.RequestError as e:
            print(f"Erro ao solicitar resultados do serviço de reconhecimento de fala; {e}")
            return None

    else:
        print("Arquivo excede 9MB, iniciando divisão em partes...")

        # Carrega o áudio completo
        audio_segment = AudioSegment.from_file(audio_path)
        duration_ms = len(audio_segment)
        chunk_duration_ms = int((SIZE_LIMIT * duration_ms) / file_size)
        if chunk_duration_ms <= 0:
            chunk_duration_ms = 10000  # fallback para 10 segundos
        total_chunks = math.ceil(duration_ms / chunk_duration_ms)
        print(f"Áudio dividido em {total_chunks} partes.")

        # Função auxiliar para processar cada chunk
        def process_chunk(i):
            start_ms = i * chunk_duration_ms
            end_ms = min((i + 1) * chunk_duration_ms, duration_ms)
            return transcrever_chunk(audio_segment, start_ms, end_ms, recognizer, i, total_chunks)

        full_text_parts = [None] * total_chunks

        # Processar os chunks em paralelo
        with concurrent.futures.ThreadPoolExecutor(max_workers=min(total_chunks, 4)) as executor:
            future_to_index = {executor.submit(process_chunk, i): i for i in range(total_chunks)}
            for future in concurrent.futures.as_completed(future_to_index):
                i = future_to_index[future]
                try:
                    full_text_parts[i] = future.result()
                except Exception as exc:
                    print(f"\nChunk {i + 1} gerou uma exceção: {exc}")
                    full_text_parts[i] = ""

        print("\nProcessamento concluído.")
        return " ".join(full_text_parts).strip()

def main():
    sample_link = "https://www.youtube.com/watch?v=C1yHhp9-8s4"
    print("Bem-vindo ao programa de transcrição de vídeo!")
    print("Por favor, insira o link do vídeo que deseja transcrição.")
    print(f"Exemplo: {sample_link}\n")
    link = input("Digite o link do vídeo: ")
    print("Digite as iniciais das opções que deseja escolher:")
    print("(v) - vídeo, (a) - áudio, (t) - transcrição, (s) - sair")
    print("Você pode escolher mais de uma opção ou deixar em branco para escolher todas.")
    print("Exemplo: 'vat' para baixar o vídeo, manter o vídeo, audio e transcrever o áudio.")
    input_option = input("Digite as iniciais das opções: ")
    os.system("cls")
    
    if link == "":
        print("Link não fornecido. O programa será encerrado.")
        return
    
    print(f"Baixando o vídeo de {link}...")
    video_path = baixar_video(link)
    if not video_path:
        print("Falha ao baixar o vídeo. O programa será encerrado.")
        return
    nome_video = os.path.splitext(os.path.basename(video_path))[0]
    audio_path = f"{nome_video}.wav"
    temp_audio_path = f"{nome_video}_temp.mp3"

    print("Extraindo áudio do vídeo...")
    extrair_audio(video_path, temp_audio_path)

    print("Convertendo áudio para formato WAV...")
    converter_audio(temp_audio_path, audio_path)

    print("Transcrevendo áudio...")
    texto = transcrever_audio(audio_path)
    
    # Remover arquivos temporários
    os.remove(temp_audio_path)

    if texto:
        print("Transcrição concluída com sucesso!")
        with open(f"{nome_video}.txt", "w", encoding="utf-8") as f:
            f.write(texto)
    else:
        print("Falha na transcrição do áudio.")

    # Criar subpasta dentro da pasta Downloads no diretório atual
    os.makedirs(f"Downloads/{nome_video}", exist_ok=True)

    # Se não foram informadas opções, assume todas (vídeo, áudio e transcrição)
    opcoes = input_option or "vat"

    # Mover ou remover o vídeo com base na opção 'v'
    if "v" in opcoes:
        os.rename(video_path, f"Downloads/{nome_video}/{os.path.basename(video_path)}")
        print(f"Vídeo movido para a pasta Downloads/{nome_video}")
    else:
        os.remove(video_path)
        print("Vídeo removido, conforme opção escolhida.")

    # Mover ou remover o áudio com base na opção 'a'
    if "a" in opcoes:
        os.rename(audio_path, f"Downloads/{nome_video}/{os.path.basename(audio_path)}")
        print(f"Áudio movido para a pasta Downloads/{nome_video}")
    else:
        os.remove(audio_path)
        print("Áudio removido, conforme opção escolhida.")

    # Mover ou remover o arquivo de transcrição com base na opção 't'
    if texto is not None:
        if "t" in opcoes:
            os.rename(f"{nome_video}.txt", f"Downloads/{nome_video}/{nome_video}.txt")
            print(f"Transcrição movida para a pasta Downloads/{nome_video}")
        else:
            os.remove(f"{nome_video}.txt")
            print("Transcrição removida, conforme opção escolhida.")

    print("O programa será encerrado.")

if __name__ == "__main__":
    main()
