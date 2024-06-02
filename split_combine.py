import os
import argparse

def split_html(html_file):
    with open(html_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    html_content = []
    css_content = []
    js_content = []

    inside_style = False
    inside_script = False

    for line in lines:
        if '<style' in line:
            inside_style = True
            continue
        if '</style>' in line:
            inside_style = False
            continue
        if '<script' in line:
            inside_script = True
            continue
        if '</script>' in line:
            inside_script = False
            continue

        if inside_style:
            css_content.append(line)
        elif inside_script:
            js_content.append(line)
        else:
            html_content.append(line)

    base_filename = os.path.splitext(html_file)[0]

    html_output_file = base_filename + '_split.html'

    if css_content:
        css_output_file = base_filename + '.css'
        with open(css_output_file, 'w', encoding='utf-8') as file:
            file.writelines(css_content)
        html_content.insert(-1, f'<link rel="stylesheet" type="text/css" href="{os.path.basename(css_output_file)}">\n')
        print(f'CSS content split into {css_output_file}')

    if js_content:
        js_output_file = base_filename + '.js'
        with open(js_output_file, 'w', encoding='utf-8') as file:
            file.writelines(js_content)
        html_content.insert(-1, f'<script src="{os.path.basename(js_output_file)}"></script>\n')
        print(f'JavaScript content split into {js_output_file}')

    with open(html_output_file, 'w', encoding='utf-8') as file:
        file.writelines(html_content)
    print(f'HTML content split into {html_output_file}')

def combine_html(html_file, css_file, js_file, output_file):
    if not os.path.exists(html_file):
        print(f"HTML file '{html_file}' is missing.")
        return
    if css_file and not os.path.exists(css_file):
        print(f"CSS file '{css_file}' is missing.")
        return
    if js_file and not os.path.exists(js_file):
        print(f"JavaScript file '{js_file}' is missing.")
        return

    with open(html_file, 'r', encoding='utf-8') as file:
        html_lines = file.readlines()

    # Remove the existing link to the CSS file and script tags for JS if present
    if css_file:
        css_file_basename = os.path.basename(css_file)
        html_lines = [line for line in html_lines if css_file_basename not in line]

    if js_file:
        js_file_basename = os.path.basename(js_file)
        html_lines = [line for line in html_lines if js_file_basename not in line]

    # Joining lines and removing root html and body tags to prevent duplication
    html_content = ''.join(html_lines).replace('<html>', '').replace('</html>', '').replace('<body>', '').replace('</body>', '')

    css_content = ""
    css_tag = ""
    if css_file:
        with open(css_file, 'r', encoding='utf-8') as file:
            css_content = file.read()
        css_tag = f"<style>{css_content}</style>"

    js_content = ""
    js_tag = ""
    if js_file:
        with open(js_file, 'r', encoding='utf-8') as file:
            js_content = file.read()
        js_tag = f"<script>{js_content}</script>"

    combined_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Combined Document</title>
    {css_tag}
</head>
<body>
    {html_content}
    {js_tag}
</body>
</html>
"""

    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(combined_content)

    print(f'Combined files into {output_file}')

def main():
    parser = argparse.ArgumentParser(description='Split or combine HTML, CSS, and JavaScript files.')
    subparsers = parser.add_subparsers(dest='command')

    split_parser = subparsers.add_parser('split', help='Split an HTML file into separate HTML, CSS, and JavaScript files.')
    split_parser.add_argument('--html', required=True, help='Path to the HTML file to split.')

    combine_parser = subparsers.add_parser('combine', help='Combine separate HTML, CSS, and JavaScript files into a single HTML file.')
    combine_parser.add_argument('--html', required=True, help='Path to the HTML file.')
    combine_parser.add_argument('--css', help='Path to the CSS file.')
    combine_parser.add_argument('--js', help='Path to the JavaScript file.')

    args = parser.parse_args()

    if args.command == 'split':
        split_html(args.html)
    elif args.command == 'combine':
        combine_html(args.html, args.css, args.js)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
