# Ollama-based Translation Tool

This Python script provides a command-line interface for translating text files or entire directories of files using Ollama language models. It supports multiple languages and allows you to specify the Ollama model to use for translation.

## Features

- Translate individual text files or entire directories
- Support for multiple languages (English, Spanish, French, German, Italian, Portuguese, Russian, Chinese, Japanese, Korean)
- Customizable Ollama model selection
- Automatic model download if not available locally
- Preserves input format in the translated output

## Prerequisites

Before you can use this tool, make sure you have the following installed:

- Python 3.6 or higher
- Ollama (follow the installation instructions at [https://ollama.ai/](https://ollama.ai/))

## Installation

1. Clone this repository or download the script file.

2. Install the required Python packages:

   ```
   pip install llama-index-llm-ollama ollama argparse chardet
   ```

3. Make sure Ollama is running on your system.

## Usage

The basic syntax for using the script is:

```
python translator.py -l <language_code> [-f <file_path> | -d <directory_path>] [-m <model_name>]
```

### Arguments:

- `-l, --language`: (Required) Output language code (e.g., 'es' for Spanish, 'en' for English)
- `-f, --file`: Path to the input file (use this OR -d)
- `-d, --directory`: Path to the input directory (use this OR -f)
- `-m, --model`: Ollama model to use for translation (default: llama3.1:latest)

### Examples:

1. Translate a single file to Spanish using the default model:
   ```
   python script.py -l es -f input.txt
   ```

2. Translate all files in a directory to English using a specific model:
   ```
   python script.py -l en -d /path/to/directory -m mistral:latest
   ```

## Output

Translated files will be saved in an `output/` directory in the same location as the script. The output files will have the same name as the input files, with the language code appended (e.g., `input_es.txt` for a Spanish translation of `input.txt`).

## Supported Languages

- English (en)
- Spanish (es)
- French (fr)
- German (de)
- Italian (it)
- Portuguese (pt)
- Russian (ru)
- Chinese (zh)
- Japanese (ja)
- Korean (ko)

## Notes

- The script will automatically download the specified Ollama model if it's not already available locally.
- Make sure you have sufficient disk space and a stable internet connection when using models that aren't locally available.
- The quality of the translation depends on the Ollama model used. Experiment with different models to find the best results for your specific use case.

## License

MIT License

Copyright (c) [year] [fullname]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Contributing

If you'd like to contribute to this project, please follow these steps:

1. Fork the repository
2. Create a new branch for your feature or bug fix
3. Make your changes and commit them with a clear commit message
4. Push your changes to your fork
5. Create a pull request to the main repository

Please ensure that your code follows the existing style and includes appropriate tests and documentation.

## Support

If you encounter any issues or have questions about using this tool, please open an issue on the GitHub repository. We'll do our best to assist you and improve the tool based on your feedback.