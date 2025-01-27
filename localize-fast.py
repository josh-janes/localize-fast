import argparse
import os
import re
import sys
import requests
import colorama
from colorama import Fore, Style

colorama.init()

class ProgressUI:
    def __init__(self, total_files):
        self.total_files = total_files
        self.translated_count = 0
    
    def update(self):
        self.translated_count += 1
        self._update_progress()
    
    def _update_progress(self):
        bar_width = 20
        progress = self.translated_count / self.total_files
        filled = int(bar_width * progress)
        bar = '[' + '#' * filled + '-' * (bar_width - filled) + ']'
        sys.stdout.write(f"\r{Fore.YELLOW}Progress: {bar} {self.translated_count}/{self.total_files} files{Style.RESET_ALL}")
        sys.stdout.flush()

def main():
    parser = argparse.ArgumentParser(description='Translate text files in a directory.')
    parser.add_argument('source_dir', help='Source directory containing files to translate')
    parser.add_argument('input_lang', help='Input language code (e.g., en)')
    parser.add_argument('output_lang', help='Output language code (e.g., es)')
    parser.add_argument('output_base', help='Base directory where translated files will be saved')
    parser.add_argument('--model', default='llama2', help='Ollama model to use (default: llama2)')
    parser.add_argument('--chunk-size', type=int, default=4000, help='Maximum chunk size for translation (default: 4000)')
    args = parser.parse_args()

    # First pass to count files
    file_paths = []
    for root, dirs, files in os.walk(args.source_dir):
        for file in files:
            if file.endswith(('.txt')):
                file_paths.append(os.path.join(root, file))

    if not file_paths:
        print(f"{Fore.RED}No translatable files found in {args.source_dir}{Style.RESET_ALL}")
        return

    ui = ProgressUI(len(file_paths))
    print(f"\n{Fore.CYAN}Starting translation ({len(file_paths)} files){Style.RESET_ALL}\n")

    output_dir = os.path.join(args.output_base, args.output_lang)
    os.makedirs(output_dir, exist_ok=True)

    for src_path in file_paths:
        file = os.path.basename(src_path)
        rel_path = os.path.relpath(src_path, args.source_dir)
        dest_path = os.path.join(output_dir, rel_path)
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)

        print(f"{Fore.GREEN}Translating:{Style.RESET_ALL} {os.path.relpath(src_path)}")

        try:
            with open(src_path, 'r', encoding='utf-8') as f:
                content = f.read()
                translated = translate_text(content, args.input_lang, args.output_lang, args.model, args.chunk_size)

            with open(dest_path, 'w', encoding='utf-8') as f:
                f.write(translated)

        except Exception as e:
            print(f"\n{Fore.RED}Error processing {src_path}: {e}{Style.RESET_ALL}")

        ui.update()

    print(f"\n\n{Fore.CYAN}Translation complete!{Style.RESET_ALL}")

def translate_text(text, input_lang, output_lang, model, chunk_size):
    chunks = split_into_chunks(str(text), chunk_size)
    translated = []
    for chunk in chunks:
        translated_chunk = send_ollama_request(chunk, input_lang, output_lang, model)
        translated.append(translated_chunk)
    return ''.join(translated)

def split_into_chunks(text, max_size):
    if len(text) <= max_size:
        return [text]
    chunks = []
    current = []
    current_len = 0
    sentences = re.split(r'(?<=[.!?]) +', text)
    for sentence in sentences:
        sentence_len = len(sentence)
        if current_len + sentence_len > max_size:
            if current:
                chunks.append(' '.join(current))
                current = []
                current_len = 0
            while sentence_len > max_size:
                split_pos = sentence.rfind(' ', 0, max_size)
                if split_pos == -1:
                    split_pos = max_size
                chunks.append(sentence[:split_pos])
                sentence = sentence[split_pos:].lstrip()
                sentence_len = len(sentence)
        if sentence:
            current.append(sentence)
            current_len += sentence_len
    if current:
        chunks.append(' '.join(current))
    return chunks

def send_ollama_request(text, input_lang, output_lang, model):
    prompt = f"Translate the following text from {input_lang} to {output_lang}. Preserve formatting and structure. Do not add any comments or notes, only the translated text. Preserve the original tone where possible, but also try to adapt untranslatable concepts in a way that will sound natural to native speakers of the target language. Include only the translated text in your response. If the text is empty or you can't complete the request just return an empty response. Text: {text}"
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": model, "prompt": prompt, "stream": False}
        )
        response.raise_for_status()
        return response.json()["response"].strip()
    except requests.RequestException as e:
        print(f"{Fore.RED}Translation error: {e}{Style.RESET_ALL}")
        return text

if __name__ == '__main__':
    main()