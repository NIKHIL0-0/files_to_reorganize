import os
import json
import re

def get_file_content(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"

def generate():
    workspace = r'C:\Users\ambat\Downloads\files_to_reorganize'
    categories = [
        'archives', 'café', 'configs', 'data', 'documentation', 
        'münchen', 'naïve-bayes', 'notes', 'reports', 'resources', 
        'résumé', 'scripts', 'templates', '日本語'
    ]
    
    file_data = []
    for cat in categories:
        cat_dir = os.path.join(workspace, cat)
        if not os.path.exists(cat_dir):
            continue
        for file in os.listdir(cat_dir):
            if file.endswith('.txt'):
                filepath = os.path.join(cat_dir, file)
                content = get_file_content(filepath)
                file_data.append({
                    "category": cat,
                    "filename": file,
                    "content": content,
                    "size": os.path.getsize(filepath)
                })
                
    # Read the reorganize.sh file to display it on the page
    script_content = ""
    script_path = os.path.join(workspace, 'reorganize.sh')
    if os.path.exists(script_path):
        script_content = get_file_content(script_path)
    
    # Read README.md
    readme_content = ""
    readme_path = os.path.join(workspace, 'README.md')
    if os.path.exists(readme_path):
        readme_content = get_file_content(readme_path)

    # Let's create the html template
    html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CMS Reorganization Showcase</title>
    <!-- Outfit Font -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=Fira+Code:wght@400;500&display=swap" rel="stylesheet">
    <!-- FontAwesome for Premium Icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {
            --bg-primary: #0b0f19;
            --bg-secondary: #131a2e;
            --bg-tertiary: #1b2542;
            --accent-primary: #6366f1;
            --accent-secondary: #06b6d4;
            --accent-gradient: linear-gradient(135deg, #6366f1 0%, #06b6d4 100%);
            --text-main: #f3f4f6;
            --text-muted: #9ca3af;
            --glass-bg: rgba(19, 26, 46, 0.6);
            --glass-border: rgba(255, 255, 255, 0.08);
            --glass-highlight: rgba(255, 255, 255, 0.03);
            --shadow-premium: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Outfit', sans-serif;
            background-color: var(--bg-primary);
            color: var(--text-main);
            line-height: 1.6;
            overflow-x: hidden;
            background-image: 
                radial-gradient(at 0% 0%, rgba(99, 102, 241, 0.15) 0px, transparent 50%),
                radial-gradient(at 100% 100%, rgba(6, 182, 212, 0.15) 0px, transparent 50%);
            background-attachment: fixed;
        }

        header {
            padding: 4rem 2rem 2rem 2rem;
            text-align: center;
            position: relative;
        }

        .header-badge {
            background: var(--accent-gradient);
            padding: 0.5rem 1.5rem;
            border-radius: 50px;
            font-size: 0.85rem;
            font-weight: 600;
            letter-spacing: 0.05em;
            text-transform: uppercase;
            display: inline-block;
            margin-bottom: 1.5rem;
            box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4);
        }

        h1 {
            font-size: 3.5rem;
            font-weight: 800;
            background: linear-gradient(to right, #ffffff, #9ca3af);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 1rem;
            letter-spacing: -0.02em;
        }

        .subtitle {
            font-size: 1.2rem;
            color: var(--text-muted);
            max-width: 600px;
            margin: 0 auto;
            font-weight: 300;
        }

        main {
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
            display: grid;
            grid-template-columns: 1fr;
            gap: 3rem;
        }

        .hash-card {
            background: var(--glass-bg);
            backdrop-filter: blur(12px);
            border: 1px solid var(--glass-border);
            border-radius: 20px;
            padding: 2rem;
            box-shadow: var(--shadow-premium);
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-wrap: wrap;
            gap: 1.5rem;
            background-image: linear-gradient(180deg, var(--glass-highlight), transparent);
            position: relative;
            overflow: hidden;
        }

        .hash-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 4px;
            height: 100%;
            background: var(--accent-gradient);
        }

        .hash-info h3 {
            font-size: 1.1rem;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 0.5rem;
        }

        .hash-value {
            font-family: 'Fira Code', monospace;
            font-size: 1.25rem;
            color: #34d399;
            background: rgba(52, 211, 153, 0.1);
            padding: 0.75rem 1.25rem;
            border-radius: 10px;
            border: 1px solid rgba(52, 211, 153, 0.2);
            word-break: break-all;
            display: flex;
            align-items: center;
            gap: 1rem;
        }

        .btn-copy {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid var(--glass-border);
            color: var(--text-main);
            padding: 0.75rem 1.25rem;
            border-radius: 10px;
            cursor: pointer;
            font-family: 'Outfit', sans-serif;
            font-weight: 500;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .btn-copy:hover {
            background: var(--accent-primary);
            border-color: var(--accent-primary);
            box-shadow: 0 0 15px rgba(99, 102, 241, 0.4);
            transform: translateY(-2px);
        }

        .section-title {
            font-size: 1.75rem;
            font-weight: 700;
            margin-bottom: 1.5rem;
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }

        .section-title i {
            background: var(--accent-gradient);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .dashboard-grid {
            display: grid;
            grid-template-columns: 280px 1fr;
            gap: 2rem;
        }

        @media (max-width: 900px) {
            .dashboard-grid {
                grid-template-columns: 1fr;
            }
        }

        .sidebar-card {
            background: var(--glass-bg);
            backdrop-filter: blur(12px);
            border: 1px solid var(--glass-border);
            border-radius: 20px;
            padding: 1.5rem;
            box-shadow: var(--shadow-premium);
            height: fit-content;
        }

        .category-list {
            list-style: none;
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
        }

        .category-item {
            padding: 0.75rem 1rem;
            border-radius: 10px;
            cursor: pointer;
            transition: all 0.2s ease;
            display: flex;
            align-items: center;
            justify-content: space-between;
            color: var(--text-muted);
            font-weight: 500;
            background: rgba(255, 255, 255, 0.01);
        }

        .category-item:hover {
            background: rgba(255, 255, 255, 0.04);
            color: var(--text-main);
            transform: translateX(4px);
        }

        .category-item.active {
            background: var(--accent-gradient);
            color: white;
            box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
        }

        .category-count {
            background: rgba(255, 255, 255, 0.1);
            padding: 0.2rem 0.6rem;
            border-radius: 20px;
            font-size: 0.75rem;
        }

        .explorer-container {
            display: flex;
            flex-direction: column;
            gap: 1.5rem;
        }

        .explorer-card {
            background: var(--glass-bg);
            backdrop-filter: blur(12px);
            border: 1px solid var(--glass-border);
            border-radius: 20px;
            padding: 2rem;
            box-shadow: var(--shadow-premium);
            min-height: 400px;
            display: flex;
            flex-direction: column;
        }

        .files-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
            gap: 1rem;
            margin-bottom: 2rem;
        }

        .file-item-card {
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 12px;
            padding: 1.25rem;
            cursor: pointer;
            transition: all 0.2s ease;
            position: relative;
            overflow: hidden;
        }

        .file-item-card:hover {
            background: rgba(255, 255, 255, 0.05);
            border-color: var(--accent-secondary);
            transform: translateY(-2px);
        }

        .file-icon {
            font-size: 2rem;
            margin-bottom: 0.75rem;
            color: var(--accent-secondary);
        }

        .file-name {
            font-weight: 600;
            font-size: 0.95rem;
            word-break: break-all;
            margin-bottom: 0.25rem;
        }

        .file-size {
            font-size: 0.8rem;
            color: var(--text-muted);
        }

        .file-details-modal {
            background: rgba(11, 15, 25, 0.8);
            border: 1px solid var(--glass-border);
            border-radius: 15px;
            padding: 1.5rem;
            margin-top: auto;
        }

        .code-section {
            background: var(--glass-bg);
            backdrop-filter: blur(12px);
            border: 1px solid var(--glass-border);
            border-radius: 20px;
            padding: 2rem;
            box-shadow: var(--shadow-premium);
        }

        .code-container {
            position: relative;
            margin-top: 1rem;
            border-radius: 12px;
            overflow: hidden;
            border: 1px solid rgba(255, 255, 255, 0.05);
        }

        .code-header {
            background: var(--bg-tertiary);
            padding: 0.75rem 1.5rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        }

        pre {
            background: #080c14;
            padding: 1.5rem;
            overflow-x: auto;
            font-family: 'Fira Code', monospace;
            font-size: 0.9rem;
            color: #e5e7eb;
        }

        footer {
            text-align: center;
            padding: 5rem 2rem;
            margin-top: 5rem;
            border-top: 1px solid var(--glass-border);
            background: rgba(11, 15, 25, 0.4);
            color: var(--text-muted);
        }

        .footer-logo {
            font-weight: 800;
            font-size: 1.25rem;
            margin-bottom: 1rem;
            background: var(--accent-gradient);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .email-link {
            color: var(--accent-secondary);
            text-decoration: none;
            font-weight: 500;
            transition: color 0.3s;
        }

        .email-link:hover {
            color: var(--accent-primary);
        }

        .toast {
            position: fixed;
            bottom: 2rem;
            right: 2rem;
            background: #10b981;
            color: white;
            padding: 1rem 2rem;
            border-radius: 10px;
            box-shadow: 0 10px 25px rgba(16, 185, 129, 0.3);
            display: flex;
            align-items: center;
            gap: 0.5rem;
            transform: translateY(100px);
            opacity: 0;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            z-index: 1000;
        }

        .toast.show {
            transform: translateY(0);
            opacity: 1;
        }

        /* Detail display styling */
        .preview-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            padding-bottom: 0.75rem;
            margin-bottom: 1rem;
        }
        .preview-title {
            font-weight: 700;
            font-size: 1.1rem;
        }
        .preview-content {
            font-family: 'Fira Code', monospace;
            background: rgba(0, 0, 0, 0.2);
            padding: 1rem;
            border-radius: 8px;
            white-space: pre-wrap;
            font-size: 0.85rem;
            max-height: 200px;
            overflow-y: auto;
        }
    </style>
</head>
<body>

    <header>
        <span class="header-badge">Verification Dashboard</span>
        <h1>CMS Reorganization</h1>
        <p class="subtitle">An automated pipeline that refactors flat/nested structures into clean, category-based organizations.</p>
    </header>

    <main>
        <!-- Verification Hash -->
        <section class="hash-card">
            <div class="hash-info">
                <h3>Verification Hash (SHA-256)</h3>
                <div class="hash-value" id="hash-text">3a803fdd979c3ec8941a5e5eb7f889d6ac6661c8b7413472c70a52bc52004203</div>
            </div>
            <button class="btn-copy" onclick="copyHash()">
                <i class="fa-regular fa-copy"></i> Copy Hash
            </button>
        </section>

        <!-- Live File Explorer Dashboard -->
        <section>
            <div class="section-title">
                <i class="fa-solid fa-folder-tree"></i>
                <h2>Interactive File Explorer</h2>
            </div>
            
            <div class="dashboard-grid">
                <!-- Sidebar (Categories) -->
                <div class="sidebar-card">
                    <ul class="category-list" id="category-list-ul">
                        <!-- Categories will be injected here -->
                    </ul>
                </div>

                <!-- Explorer Main -->
                <div class="explorer-container">
                    <div class="explorer-card">
                        <div class="files-grid" id="files-grid-div">
                            <!-- Files will be injected here -->
                        </div>
                        
                        <!-- File Preview Modal/Details -->
                        <div class="file-details-modal" id="preview-section" style="display: none;">
                            <div class="preview-header">
                                <span class="preview-title" id="preview-filename">Select a file to preview</span>
                                <span class="file-size" id="preview-filesize"></span>
                            </div>
                            <div class="preview-content" id="preview-body"></div>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- Reorganization Script -->
        <section class="code-section">
            <div class="section-title">
                <i class="fa-solid fa-terminal"></i>
                <h2>The Reorganization Script</h2>
            </div>
            <p style="color: var(--text-muted); margin-bottom: 1rem;">This Bash script extracts the target category from each document's first line, normalizes relative paths, places them in corresponding directories, and generates the verification signature.</p>
            <div class="code-container">
                <div class="code-header">
                    <span>reorganize.sh</span>
                    <button class="btn-copy" onclick="copyScript()">
                        <i class="fa-regular fa-copy"></i> Copy Script
                    </button>
                </div>
                <pre><code id="script-code"># script content here</code></pre>
            </div>
        </section>
    </main>

    <footer>
        <div class="footer-logo">CMS Refactoring Portfolio</div>
        <p style="margin-bottom: 0.5rem;">Created as part of the Content Management System Refactoring Challenge.</p>
        <p>Contact Developer: <!--email_off-->23f3001617@ds.study.iitm.ac.in<!--/email_off--></p>
    </footer>

    <div class="toast" id="toast-el">
        <i class="fa-solid fa-circle-check"></i>
        <span id="toast-message">Copied to clipboard!</span>
    </div>

    <script>
        // Data injected from Python generator
        const fileData = """ + json.dumps(file_data) + """;
        const scriptCodeContent = """ + json.dumps(script_content) + """;

        document.getElementById('script-code').textContent = scriptCodeContent;

        // Group files by category
        const categories = {};
        fileData.forEach(item => {
            if (!categories[item.category]) {
                categories[item.category] = [];
            }
            categories[item.category].push(item);
        });

        // Initialize sidebar
        const catUl = document.getElementById('category-list-ul');
        const sortedCats = Object.keys(categories).sort();
        
        sortedCats.forEach((cat, index) => {
            const li = document.createElement('li');
            li.className = 'category-item' + (index === 0 ? ' active' : '');
            li.setAttribute('data-category', cat);
            li.innerHTML = `
                <span><i class="fa-regular fa-folder-open" style="margin-right: 8px;"></i> ${cat}</span>
                <span class="category-count">${categories[cat].length}</span>
            `;
            li.onclick = () => selectCategory(cat, li);
            catUl.appendChild(li);
        });

        // Select initial category
        if (sortedCats.length > 0) {
            renderFiles(sortedCats[0]);
        }

        function selectCategory(cat, element) {
            document.querySelectorAll('.category-item').forEach(el => el.classList.remove('active'));
            element.classList.add('active');
            renderFiles(cat);
            document.getElementById('preview-section').style.display = 'none';
        }

        function renderFiles(category) {
            const grid = document.getElementById('files-grid-div');
            grid.innerHTML = '';
            
            categories[category].forEach(file => {
                const card = document.createElement('div');
                card.className = 'file-item-card';
                card.innerHTML = `
                    <div class="file-icon"><i class="fa-regular fa-file-lines"></i></div>
                    <div class="file-name">${file.filename}</div>
                    <div class="file-size">${(file.size / 1024).toFixed(2)} KB</div>
                `;
                card.onclick = () => showPreview(file);
                grid.appendChild(card);
            });
        }

        function showPreview(file) {
            document.getElementById('preview-section').style.display = 'block';
            document.getElementById('preview-filename').textContent = file.filename;
            document.getElementById('preview-filesize').textContent = (file.size / 1024).toFixed(2) + " KB";
            document.getElementById('preview-body').textContent = file.content;
        }

        function copyHash() {
            const hash = document.getElementById('hash-text').textContent;
            navigator.clipboard.writeText(hash).then(() => {
                showToast("Verification hash copied!");
            });
        }

        function copyScript() {
            navigator.clipboard.writeText(scriptCodeContent).then(() => {
                showToast("Shell script copied!");
            });
        }

        function showToast(message) {
            const toast = document.getElementById('toast-el');
            document.getElementById('toast-message').textContent = message;
            toast.classList.add('show');
            setTimeout(() => {
                toast.classList.remove('show');
            }, 2500);
        }
    </script>
</body>
</html>
"""
    
    output_html_path = os.path.join(workspace, 'index.html')
    with open(output_html_path, 'w', encoding='utf-8') as f:
        f.write(html_template)
        
    print(f"Generated index.html successfully at {output_html_path}")

if __name__ == "__main__":
    generate()
