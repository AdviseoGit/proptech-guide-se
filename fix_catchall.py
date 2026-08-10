def patch_main():
    with open('/data/workspace/projects/proptech-guide-se/main.py', 'r') as f:
        content = f.read()
        
    import re
    # We need to move the catchall to the end, just before the if __name__ block
    
    # Extract the catchall block
    catchall_pattern = re.compile(r'@app\.get\("/\{filename:path\}", response_class=HTMLResponse\)\nasync def serve_html\(filename: str\):\n.*?return FileResponse\(\)\n', re.DOTALL)
    
    catchall_match = catchall_pattern.search(content)
    if catchall_match:
        catchall_text = catchall_match.group(0)
        # Remove it from its current position
        content = content.replace(catchall_text, '')
        
        # Add it right before the if __name__ block
        main_block = 'if __name__ == "__main__":'
        content = content.replace(main_block, catchall_text + '\n' + main_block)
        
        with open('/data/workspace/projects/proptech-guide-se/main.py', 'w') as f:
            f.write(content)
        print("Patched catchall route order")
    else:
        # Let's try a simpler regex just matching up to next @app or if __name__
        lines = content.split('\n')
        new_lines = []
        catchall_lines = []
        in_catchall = False
        
        for line in lines:
            if line.startswith('@app.get("/{filename:path}"'):
                in_catchall = True
                catchall_lines.append(line)
            elif in_catchall and (line.startswith('@app') or line.startswith('if __name__')):
                in_catchall = False
                new_lines.append(line)
            elif in_catchall:
                catchall_lines.append(line)
            else:
                new_lines.append(line)
                
        # Insert catchall lines before if __name__
        final_lines = []
        for line in new_lines:
            if line.startswith('if __name__'):
                final_lines.extend(catchall_lines)
                final_lines.append(line)
            else:
                final_lines.append(line)
                
        with open('/data/workspace/projects/proptech-guide-se/main.py', 'w') as f:
            f.write('\n'.join(final_lines))
        print("Patched catchall route order (fallback method)")

patch_main()
