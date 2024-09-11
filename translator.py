import argparse
import os
from enum import Enum
from llama_index.llms.ollama import Ollama
import ollama
import sys
import chardet

output_dir = 'output/'

class Language(Enum):
    ENGLISH = ('en', 'English')
    SPANISH = ('es', 'Spanish')
    FRENCH = ('fr', 'French')
    GERMAN = ('de', 'German')
    ITALIAN = ('it', 'Italian')
    PORTUGUESE = ('pt', 'Portuguese')
    RUSSIAN = ('ru', 'Russian')
    CHINESE = ('zh', 'Chinese')
    JAPANESE = ('ja', 'Japanese')
    KOREAN = ('ko', 'Korean')

    def __init__(self, code, full_name):
        self.code = code
        self.full_name = full_name

    def __str__(self):
        return f"{self.full_name}"

    @classmethod
    def from_code(cls, code):
        for lang in cls:
            if lang.code == code.lower():
                return lang
        raise ValueError(f"No se encontró un idioma con el código '{code}'")

def detect_encoding(file_path):
    with open(file_path, 'rb') as file:
        raw_data = file.read()
    result = chardet.detect(raw_data)
    return result['encoding']

def language_choice(value):
    try:
        return Language.from_code(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"'{value}' no es un código de idioma válido. Opciones válidas: {', '.join([lang.code for lang in Language])}")

def check_ollama_model(model_name):
    try:
        #Check if model name have the structure of ollama models
        if ':' in model_name:
            model_ollama = model_name
        else:
            model_ollama = model_name + ':latest'

        models = ollama.list()
        return any(model['name'] == model_ollama for model in models['models'])
    except Exception as e:
        print(f"Error al verificar el modelo de Ollama: {e}")
        return False

def pull_ollama_model(model_name):
    print(f"El modelo '{model_name}' no está disponible localmente. Descargando...")
    try:
        ollama.pull(model_name)
        print(f"Modelo '{model_name}' descargado exitosamente.")
    except Exception as e:
        print(f"Error al descargar el modelo '{model_name}': {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description="Script to process files and translate them into a specified language using Ollama models.",
        epilog="Examples of use:\n"
               "  python script.py -l es -f input.txt\n"
               "  python script.py -l en -d /path/to/directory",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument('-l', '--language', type=language_choice, required=True, 
                        help="Output language (for example: 'es' for Spanish, 'en' for English)")
    parser.add_argument('-f', '--file', type=str, 
                        help="Path to the input file")
    parser.add_argument('-d', '--directory', type=str, 
                        help="Path to the input directory")
    parser.add_argument('-m', '--model', type=str, default='llama3.1:latest',
                        help="Ollama model to use for translation (default: llama3.1)")
    
    args = parser.parse_args()
    
    output_language = args.language
    input_file = args.file
    input_directory = args.directory
    model = args.model

    #Check if the model is arleady pulled else, is pulled
    if not check_ollama_model(model):
        pull_ollama_model(model)
    
    if input_file and input_directory:
        parser.error("You must provide either a file OR a directory, not both.")
    elif not input_file and not input_directory:
        parser.error("You must provide either a file or a directory.")

    # Creating the output directory if it isn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    if input_file:
        if os.path.isfile(input_file):
            process_file(input_file, output_language, model)
        else:
            parser.error("The path you provide isn't a file")
    elif input_directory:
        if os.path.isdir(input_directory):
            process_directory(input_directory, output_language, model)
        else:
            parser.error("The path you provide isn't a directory")

def chunk_content(content, chunk_size=1000):
    """Split the content into chunks of approximately chunk_size characters."""
    chunks = []
    current_chunk = []
    current_size = 0
    
    for line in content.split('\n'):
        if current_size + len(line) > chunk_size and current_chunk:
            chunks.append('\n'.join(current_chunk))
            current_chunk = []
            current_size = 0
        current_chunk.append(line)
        current_size += len(line) + 1  # +1 for the newline character
    
    if current_chunk:
        chunks.append('\n'.join(current_chunk))
    
    return chunks

def process_file(file_path, language, model):
    print(f"Processing file: {file_path}")
    print(f"Output language: {language}")
    
    # Detect the file encoding
    file_encoding = detect_encoding(file_path)
    print(f"Detected file encoding: {file_encoding}")
    
    # Open the file with the detected encoding
    with open(file_path, 'r', encoding=file_encoding) as file:
        content = file.read()
    
    # Split the content into chunks
    chunks = chunk_content(content)
    print(f"Split content into {len(chunks)} chunks")
    
    # Translate each chunk
    translated_chunks = []
    for i, chunk in enumerate(chunks):
        print(f"Translating chunk {i+1}/{len(chunks)}...")
        translated_chunk = translate_text(chunk, language, model)
        translated_chunks.append(translated_chunk)
    
    # Join the translated chunks
    translated_content = '\n'.join(translated_chunks)
    
    # Generate the output file path
    output_path = os.path.join(output_dir, file_path)
    
    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Save the file (using UTF-8 encoding for the output)
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(translated_content)
    
    print(f"Translation saved to: {output_path}")

def process_directory(dir_path, language, model):
    print(f"Processing directory: {dir_path}")

    #Create the directory in the output directory
    os.makedirs(output_dir + dir_path, exist_ok=True)
    
    for filename in os.listdir(dir_path):
        if filename.endswith(".txt") or filename.endswith(".csv"):
            file_path = os.path.join(dir_path, filename)
            if os.path.isdir(file_path):
                process_directory(file_path,language, model)
            else:
                process_file(file_path, language, model)

def translate_text(text, language, model):
    prompt = f"""You are a profesional dataset traductor. Translate the following dataset text to {language.full_name}. Follow these instructions carefully:
First, only keep the translation in the result.
Second as the text is a dataset, please, maintain the exact input format in your translation. This includes preserving all line breaks, spacing, and punctuation.
Third, do not add any explanations, notes, or content other than the direct translation and do not include any text outside of the translation itself - no introductions, conclusions, or meta-commentary.
Fourth, if a single term in the source language translates to multiple words in the target language, join these words with underscores. For example, 'smartphone' in English might become 'teléfono_inteligente' in Spanish.
Fifth, preserve any special characters, numbers, or untranslatable elements exactly as they appear in the original text.
Sixth, if there are any ambiguous terms or phrases, choose the most appropriate translation based on the context.


Here is the text to translate:

{text}

Translation:"""
    response = ollama.generate(model=model, prompt=prompt)
    return response['response']

if __name__ == "__main__":
    main()