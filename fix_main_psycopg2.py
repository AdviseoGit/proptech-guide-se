def patch_main():
    with open('/data/workspace/projects/proptech-guide-se/main.py', 'r') as f:
        content = f.readlines()
        
    for i, line in enumerate(content):
        if line.startswith('import psycopg2') and i < 20:
            content[i] = 'try:\n    import psycopg2\nexcept ImportError:\n    pass\n'
            break
            
    with open('/data/workspace/projects/proptech-guide-se/main.py', 'w') as f:
        f.writelines(content)
    print("Patched main.py")

patch_main()
