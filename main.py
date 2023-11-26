import re
import tkinter as tk
from tkinter import ttk, filedialog
import whisper
import os





reference_words = [
    'лис', 'жук', 'мир', 'мощь', 'бич', 'зять', 'шах', 'царь', 'фон', 'суп', 'любимый', 'обязательно',
    'хорошо', 'женщина', 'помогать', 'офицер', 'химический', 'наблюдать', 'девушка', 'составлять',
    'голосистыйскворец', 'бабушкинаматрёшка', 'месторождениезолота', 'коричневаяциновка',
    'пуховыйплаток', 'серебристаяящерица', 'милыйбегемотик', 'быстроходныйкатерперевозилпассажировчерезозеро',
    'лидаподсказаладашедомашнеезадание', 'апельсиновыйлимонадналиливхрустальныйграфин',
    'вэтомпомещенииработаютучёные', 'усофиинасарафаненовыепуговицы'
]


save_folder_path = ''

def select_audio_folder():
    global folder_path
    folder_path = filedialog.askdirectory()
    entry.delete(0, tk.END)
    entry.insert(0, folder_path)


def select_save_folder():
    global save_folder_path
    save_folder_path = filedialog.askdirectory()
    save_entry.delete(0, tk.END)
    save_entry.insert(0, save_folder_path)


def save_to_file(text, save_folder):
    folder_name = os.path.basename(folder_path)
    save_path = os.path.join(save_folder, f"{folder_name}.txt")
    with open(save_path, "w", encoding="utf-8") as file:
        file.write(text)
    return save_folder

root = tk.Tk()
root.title("Audio Transcriber")

frame = ttk.Frame(root, padding="20")
frame.grid(row=0, column=0, sticky="nsew")

transcription_label = ttk.Label(frame, text="", wraplength=400)
transcription_label.grid(row=5, column=0, padx=5, pady=5)

def transcribe_audio():
    global all_transcriptions

    folder_path = entry.get()
    save_folder_path = save_entry.get()

    if folder_path and save_folder_path and os.path.isdir(folder_path) and os.path.isdir(save_folder_path):
        model = whisper.load_model("medium")
        all_transcriptions = ""
        for file_name in os.listdir(folder_path):
            if file_name.endswith(".mp3") or file_name.endswith(".wav") or file_name.endswith(".ogg"):
                audio_path = os.path.join(folder_path, file_name)
                result = model.transcribe(audio_path, language='ru')
                word = result['text']
                word = word.lower()
                word = re.sub(r'[^\w\s]', '', word)

                all_transcriptions += f"Транскрибированное слово из {file_name}:\n{word}\n\n"

        if all_transcriptions:
            transcription_label.config(text="Все файлы прошли транскрибацию")
            save_to_file(all_transcriptions, save_folder_path)
        else:
            transcription_label.config(text="No audio files found in the selected folder.")
    else:
        transcription_label.config(text="Please select valid folders!")




def evaluate_transcribed_words(transcribed_text):
    transcribed_text = load_transcribed_text(os.path.join(save_folder_path, "transcriptions.txt"))
    if transcribed_text:
        result_text = ""
        transcribed_words = re.findall(r'\b\w+\b', transcribed_text)
        for transcribed_word in transcribed_words:
            transcribed_word = transcribed_word.lower()
            for reference_word in reference_words:
                reference_word = reference_word.lower()
                matching_characters = sum(a == b for a, b in zip(transcribed_word, reference_word))
                percentage = (matching_characters / len(reference_word)) * 100
                result_text += (
                    f"Транскрибированное слово: {transcribed_word}\n"
                    f"Эталонное слово: \"{reference_word}\"\n"
                    f"Слово произнесено правильно на {percentage:.2f}%\n\n"
                )
        save_path = os.path.join(save_folder_path, "transcriptions_result.txt")
        save_evaluation_result(result_text, save_path)
        transcription_label.config(text="Результат оценки сохранен в файле 'transcriptions_result.txt'")
    else:
        transcription_label.config(text="Файл с транскрибированными словами не найден.")



def load_transcribed_text(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        return None



def save_evaluation_result(result_text, file_path):
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(result_text)
        return True
    except Exception as e:
        print(f"Ошибка сохранения результата: {e}")
        return False

transcribed_text = load_transcribed_text("transcriptions.txt")
result_text = evaluate_transcribed_words(transcribed_text)









label = ttk.Label(frame, text="Выберите папку с аудиофайлами:")
label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

entry = ttk.Entry(frame, width=40)
entry.grid(row=1, column=0, padx=5, pady=5)

select_folder_button = ttk.Button(frame, text="Выбрать папку", command=select_audio_folder)
select_folder_button.grid(row=1, column=1, padx=5, pady=5)

save_label = ttk.Label(frame, text="Выберите папку для сохранения:")
save_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")

save_entry = ttk.Entry(frame, width=40)
save_entry.grid(row=3, column=0, padx=5, pady=5)

select_save_button = ttk.Button(frame, text="Выбрать папку", command=select_save_folder)
select_save_button.grid(row=3, column=1, padx=5, pady=5)

transcribe_button = ttk.Button(frame, text="Транскрибировать", command=transcribe_audio)
transcribe_button.grid(row=4, column=0, padx=5, pady=5)

evaluate_button = ttk.Button(frame, text="Провести оценку", command=evaluate_transcribed_words)
evaluate_button.grid(row=6, column=0, padx=5, pady=5)



root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
frame.columnconfigure(0, weight=1)

root.mainloop()
