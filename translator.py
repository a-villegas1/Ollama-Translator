import argparse
import os
from enum import Enum
from llama_index.llms.ollama import Ollama
import ollama
import sys

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
    parser.add_argument('-m', '--model', type=str, default='mixtral:8x22b',
                        help="Ollama model to use for translation (default: mixtral:8x22b)")
    
    args = parser.parse_args()
    
    output_language = args.language
    input_file = args.file
    input_directory = args.directory
    model = args.model
    
    if not check_ollama_model(model):
        pull_ollama_model(model)
    
    if input_file and input_directory:
        parser.error("You must provide either a file OR a directory, not both.")
    elif not input_file and not input_directory:
        parser.error("You must provide either a file or a directory.")

    # Crear el directorio de salida si no existe
    os.makedirs(output_dir, exist_ok=True)
    
    if input_file:
        process_file(input_file, output_language, model)
    elif input_directory:
        process_directory(input_directory, output_language, model)

def process_file(file_path, language, model):
    print(f"Processing file: {file_path}")
    print(f"Output language: {language}")
    
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    translated_content = translate_text(content, language, model)
    
    output_filename = f"{os.path.splitext(os.path.basename(file_path))[0]}_{language.code}.txt"
    output_path = os.path.join(output_dir, output_filename)
    
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(translated_content)
    
    print(f"Translation saved to: {output_path}")

def process_directory(dir_path, language, model):
    print(f"Processing directory: {dir_path}")
    print(f"Output language: {language}")
    
    for filename in os.listdir(dir_path):
        if filename.endswith(".txt") or filename.endswith(".csv"):
            file_path = os.path.join(dir_path, filename)
            process_file(file_path, language, model)

def translate_text(text, language, model):
    prompt = f"Translate the following text to {language.full_name}. It's important you keep the input format and don't add other thing than the translation:\n\n{text}\n\nTranslation:"
    response = ollama.generate(model=model, prompt=prompt)
    return response['response']

if __name__ == "__main__":
    main()