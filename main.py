import argparse
import os
import openai
import re
openai.organization = os.getenv("OPENAI_API_ORG")
openai.api_key = os.getenv("OPENAI_API_KEY")
import base64
import zlib
import requests


code_directory_path="./code_files/"
# Define a dictionary to map code types to file extensions
code_type_extensions = {
    'plantuml': 'puml',
    'graphviz': 'dot',
    'digraph': 'dot',
    'mermaid': 'mermaid',
    'blockdiag': 'diag',
    # Add more mappings as needed
}
# Define a dictionary to map code types to file extensions
extensions_to_type = {
    'puml': 'plantuml',
    'dot': 'graphviz',
    'mermaid': 'mermaid',
    'diag':'blockdiag',
}
code_files_dir='code_files/'

def get_diagram_encoding(file_path):
    
    try:
        # Read the contents of the  file
        with open(file_path, 'rb') as file:
            file_contents = file.read()

        # Compress the file contents using zlib with compression level 9
        compressed_data = zlib.compress(file_contents, level=9)

        # Encode the compressed data as URL-safe base64
        encoded_data = base64.urlsafe_b64encode(compressed_data).decode('ascii')

        # Print or use the encoded data as needed
        return encoded_data

    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


def format_response(api_data, i=0):
    code_blocks_with_type = re.findall(r'```(.*?)```', api_data, re.DOTALL)

    # Create a directory to store code files
    if not os.path.exists('code_files'):
        os.mkdir('code_files')

    # Save code blocks to files based on type
    for block_with_type in code_blocks_with_type:
        i=i+1
        lines = block_with_type.strip().split('\n')
        
        if len(lines) < 2:
            continue
        
        code_type = lines[0].strip().lower()
        code_content = '\n'.join(lines[1:])
        
        if code_type in code_type_extensions:
            file_extension = code_type_extensions[code_type]
            with open(f'code_files/code_{i}.{file_extension}', 'w') as file:
                file.write(code_content)
        
    return i


def call_model(model_version, instruction, text):
    response = openai.ChatCompletion.create(
        model=model_version,
        messages=[
            {"role": "system", "content": "You are a helpful assistant. Generate only code"},
            {"role": "user", "content": f"${instruction}, Text: ${text}"},
        ]
    )
    return response['choices'][0]['message']['content']

def convert_code(file):
    file_path = os.path.join(code_directory_path, file)

    encoding=get_diagram_encoding(file_path)

    # Get the file extension
    file_extension = os.path.splitext(file_path)[1]

    # Remove the dot (.) from the extension
    file_extension = file_extension.lstrip('.')

    if file_extension not in extensions_to_type:
        return ''
    url = 'https://kroki.io/'+extensions_to_type[file_extension]+'/svg/'+encoding

    return url

def generate_diagrams(model_version, text_file, output_dir, num_diagrams):
    print(f"Generating {num_diagrams} diagrams using model {model_version}...")
    print(f"Input text file: {text_file}")
    print(f"Output directory: {output_dir}")
    diagrams_generated=0

    instruction=f"Generate code in Kroki to create exactly ${num_diagrams} informative diagrams. "

    with open(text_file, 'r') as file:
        m=0
        text = file.read()
        
        while(diagrams_generated<num_diagrams):
            print(f"{diagrams_generated}/{num_diagrams} generated ...")
            api_data=call_model(model_version, instruction, text)
            m=format_response(api_data, m)
            m=+1
            file_list = os.listdir(code_directory_path)
            for m in range(len(file_list)):
                
                if num_diagrams== diagrams_generated:
                    break
                
                url = convert_code(file_list[m])

                if url=='':
                    continue

                # Send the GET request
                response = requests.get(url)

                if response.status_code == 200:
                    svg_text = response.text

                    file_name = f'output_{diagrams_generated}.svg'
                    file_path = os.path.join(output_dir, file_name)

                    try:
                        with open(file_path, 'w') as file:
                            file.write(svg_text)

                        print(f"SVG file '{file_path}' has been created.")
                        diagrams_generated+=1
                        
                    except Exception as e:
                        print(f"An error occurred: {str(e)}")

                    
                else:
                    print(f"Request failed with status code {response.status_code}")
                try:
                    
                    file_path = os.path.join(code_files_dir, file_list[m])
                    os.remove(file_path)
                    print(f"File '{file_path}' deleted successfully.")
                except OSError as e:
                    # Handle any errors that occur during deletion
                    print(f"Error deleting file '{file_path}': {e}") 

    


    print(f'Done... You can find your diagram in {output_dir}')

    # Cleanup
    try:
        for item in os.listdir(code_files_dir):
            item_path = os.path.join(code_files_dir, item)
            if os.path.isfile(item_path):
                os.remove(item_path)
        os.rmdir(code_files_dir)
        print(f"Directory '{code_files_dir}' deleted successfully.")
    except OSError as e:
        # Handle any errors that occur during deletion
        print(f"Error deleting directory '{code_files_dir}': {e}")







        

def main():
    # Create an argument parser
    parser = argparse.ArgumentParser(description="Generate diagrams from text using a specified model.")

    # Define valid model choices
    valid_models = ["gpt-4", "gpt-4-32k", "gpt-3.5-turbo", "gpt-3.5-turbo-16k"]

    # Define command-line arguments
    parser.add_argument("-m", "--model", choices=valid_models, default="gpt-4", help="Model version (default: gpt-4)")
    parser.add_argument("text_file", help="Input text file (required)")
    parser.add_argument("-o", "--output", default="diagrams/", help="Output directory (default: diagrams/)")
    parser.add_argument("-n", "--num_diagrams", type=int, default=3, help="Number of diagrams to generate (default: 3)")

    # Parse the command-line arguments
    args = parser.parse_args()

    # Check if the input text file exists
    if not os.path.isfile(args.text_file):
        print(f"Error: The specified text file '{args.text_file}' does not exist.")
        return

    # Create the output directory if it doesn't exist
    os.makedirs(args.output, exist_ok=True)

    # Call the function to generate diagrams
    generate_diagrams(args.model, args.text_file, args.output, args.num_diagrams)

if __name__ == "__main__":
    main()
