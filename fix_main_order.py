def patch_main():
    with open('/data/workspace/projects/proptech-guide-se/main.py', 'r') as f:
        content = f.read()
        
    main_block = 'if __name__ == "__main__":\n    port = int(os.environ.get("PORT", 8080))\n    uvicorn.run(app, host="0.0.0.0", port=port)'
    
    if main_block in content:
        # Remove it from wherever it is
        content = content.replace(main_block, '')
        # Add it to the end
        content += '\n\n' + main_block + '\n'
        
        with open('/data/workspace/projects/proptech-guide-se/main.py', 'w') as f:
            f.write(content)
        print("Patched main.py order")

patch_main()
