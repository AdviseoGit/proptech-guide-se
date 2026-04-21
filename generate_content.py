import os
import json
import urllib.request
from botocore.auth import SigV4Auth
from botocore.awsrequest import AWSRequest
from botocore.credentials import Credentials
from botocore.httpsession import URLLib3Session

def call_claude_bedrock(prompt: str) -> str:
    """
    Invokes the Anthropic Claude 2 model on Amazon Bedrock to generate content.
    """
    # Create a session with your AWS credentials
    access_key = os.environ.get("AWS_ACCESS_KEY_ID")
    secret_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    session_token = os.environ.get("AWS_SESSION_TOKEN")
    
    if not all([access_key, secret_key]):
        raise ValueError("AWS credentials (AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY) must be set as environment variables.")

    creds = Credentials(access_key, secret_key, session_token)
    
    # Create the request
    service = 'bedrock'
    region = 'us-east-1'
    host = f"bedrock-runtime.{region}.amazonaws.com"
    endpoint = f"https://{host}/model/anthropic.claude-v2:1/invoke"

    # Anthropic Claude V2 prompt format
    prompt_data = f"\\n\\nHuman: {prompt}\\n\\nAssistant:"

    request_body = {
        "prompt": prompt_data,
        "max_tokens_to_sample": 8000,
        "temperature": 0.7,
        "top_p": 0.9
    }

    aws_request = AWSRequest(
        method="POST",
        url=endpoint,
        data=json.dumps(request_body),
        headers={'host': host, 'content-type': 'application/json'},
    )
    SigV4Auth(creds, service, region).add_auth(aws_request)
    
    try:
        request = urllib.request.Request(
            endpoint,
            data=aws_request.body,
            headers=aws_request.headers,
            method='POST'
        )
        with urllib.request.urlopen(request) as response:
            response_body = json.loads(response.read())
            return response_body.get('completion', '')
    except Exception as e:
        print(f"Error invoking Bedrock model: {e}")
        return ""

if __name__ == '__main__':
    # Generate the PropTech company directory
    directory_prompt = "Create a markdown table of the top 50 PropTech companies in Sweden. The table should have columns for 'Company', 'Website', and 'Description'. The description should be a short, one-sentence summary of what the company does."
    directory_content = call_claude_bedrock(directory_prompt)

    # Generate the main article
    article_prompt = "Write a long-form article in Swedish titled 'Vad är PropTech? En guide för fastighetsägare i Sverige 2026.' The article should be at least 1000 words long and cover the following topics: what is proptech, why is it important, the different categories of proptech, the benefits of adopting proptech, and the future of proptech in Sweden. The article should be well-structured and easy to read."
    article_content = call_claude_bedrock(article_prompt)
    
    if not article_content or not directory_content:
        print("Failed to generate content from the model. Exiting.")
        exit(1)

    # Create a new HTML file with the generated content
    new_html_content = """
<!DOCTYPE html>
<html lang="sv">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Proptech Guide Sverige | Framtidens Fastighetsförvaltning</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap" rel="stylesheet">
    <style>
        body {{ font-family: 'Plus Jakarta Sans', sans-serif; }}
        .gradient-text {{
            background: linear-gradient(90deg, #0284c7, #06b6d4);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
    </style>
</head>
<body class="bg-slate-50 text-slate-900 flex flex-col min-h-screen">
    <nav class="p-6 max-w-7xl mx-auto w-full flex justify-between items-center">
        <a href="/" class="text-2xl font-extrabold tracking-tight">PROPTECH<span class="text-sky-600">GUIDE</span></a>
        <div class="hidden md:flex space-x-8 font-medium text-slate-600">
            <a href="/kategorier" class="hover:text-sky-600">Kategorier</a>
            <a href="/ai-i-fastigheter" class="hover:text-sky-600">AI i fastigheter</a>
            <a href="/om-oss" class="hover:text-sky-600">Om oss</a>
        </div>
    
        <button id="mobile-menu-btn" class="md:hidden text-slate-600 hover:text-slate-900 focus:outline-none ml-auto" aria-label="Toggle menu" onclick="document.getElementById('mobile-menu').classList.toggle('hidden');">
            <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"></path></svg>
        </button>
</nav>
    <div id="mobile-menu" class="hidden md:hidden bg-white border-b border-slate-200 w-full px-6 py-4 absolute left-0 z-40 shadow-sm" style="top: 80px;">
        <div class="flex flex-col space-y-4 font-medium text-slate-600">
            <a href="/kategorier" class="hover:text-sky-600 block">Kategorier</a>
            <a href="/ai-i-fastigheter" class="hover:text-sky-600 block">AI i fastigheter</a>
            <a href="/om-oss" class="hover:text-sky-600 block">Om oss</a>
        </div>
    </div>


    <header class="py-20 px-6 max-w-7xl mx-auto text-center w-full">
        <h1 class="text-5xl md:text-7xl font-extrabold mb-6 tracking-tight">Digitaliseringen av <span class="gradient-text">svenska fastigheter.</span></h1>
        <p class="text-xl text-slate-600 max-w-2xl mx-auto mb-10">Vi kartlägger de mest innovativa verktygen och plattformarna för fastighetsägare, förvaltare och BRF:er.</p>
        <div class="flex flex-col md:flex-row justify-center gap-4">
            <a href="/kategorier" class="bg-slate-900 text-white px-8 py-4 rounded-xl font-bold hover:bg-slate-800 transition-all text-center">Utforska Verktygen</a>
            <a href="/ai-i-fastigheter" class="bg-white text-slate-900 px-8 py-4 rounded-xl font-bold hover:bg-slate-100 border border-slate-200 transition-all text-center">Läs om AI i Fastigheter</a>
        </div>
    </header>
    <main class="max-w-7xl mx-auto px-6 py-20 flex-grow w-full">
        <article class="prose max-w-none prose-lg">
        {article_content}
        </article>
        <div class="mt-20">
            <h2 class="text-4xl font-extrabold mb-8 tracking-tight text-center">Proptech-bolag i Sverige</h2>
            <div class="overflow-x-auto">
                <table class="w-full text-left border-collapse">
                    <thead>
                        <tr>
                            <th class="py-4 px-6 bg-slate-100 font-bold uppercase text-sm text-slate-600 border-b border-slate-200">Bolag</th>
                            <th class="py-4 px-6 bg-slate-100 font-bold uppercase text-sm text-slate-600 border-b border-slate-200">Hemsida</th>
                            <th class="py-4 px-6 bg-slate-100 font-bold uppercase text-sm text-slate-600 border-b border-slate-200">Beskrivning</th>
                        </tr>
                    </thead>
                    <tbody>
                        <!-- This part will be replaced by the script -->
                        {directory_content}
                    </tbody>
                </table>
            </div>
        </div>
    </main>
    <footer class="py-12 border-t border-slate-200 text-center text-slate-500 mt-auto w-full">
        <p>© 2026 Proptech Guide Sverige | Utvecklad av Adviseo</p>
    </footer>
</body>
</html>
"""

    # A simple way to convert markdown table to HTML rows.
    # This is a bit naive and assumes a simple structure.
    # For a real-world scenario, a proper markdown-to-html library would be better.
    html_table_rows = ""
    for line in directory_content.strip().split('\\n'):
        if '|' in line and '---' not in line: # Basic check for a table row
            cells = [cell.strip() for cell in line.split('|') if cell.strip()]
            if len(cells) == 3:
                html_table_rows += f'<tr class="hover:bg-slate-50"><td class="py-4 px-6 border-b border-slate-200">{cells[0]}</td><td class="py-4 px-6 border-b border-slate-200"><a href="{cells[1]}" target="_blank" class="text-sky-600 hover:underline">{cells[1]}</a></td><td class="py-4 px-6 border-b border-slate-200">{cells[2]}</td></tr>\\n'
    
    final_html = new_html_content.format(article_content=article_content, directory_content=html_table_rows)

    with open("projects/proptech-guide-se/static/index.html", "w") as f:
        f.write(final_html)

    print("Successfully generated new index.html with PropTech content.")
