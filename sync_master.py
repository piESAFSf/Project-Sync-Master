import os
import sys

# Optimized for Commercial Release (Weiyang Technology)

IGNORE_DIRS = {'.git', 'node_modules', '__pycache__', 'venv', '.openclaw', '.vscode', 'dist', 'build'}
EXTENSIONS = {'.md', '.py', '.js', '.ts', '.txt', '.json'}

def get_project_sync_data(root_dir):
    print(f"[*] Analyzing project at: {root_dir}")
    sync_block = "### [PROJECT SYNC BLOCK - CONTEXT INJECTION] ###\n"
    sync_block += "Goal: Synchronize project state with AI Assistant.\n\n"
    
    files_processed = 0
    
    for root, dirs, files in os.walk(root_dir):
        # Prune ignored directories
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext in EXTENSIONS or file in ['Dockerfile', 'docker-compose.yml', 'package.json', 'requirements.txt']:
                path = os.path.join(root, file)
                rel_path = os.path.relpath(path, root_dir)
                
                try:
                    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                        
                    # Heuristic: only include full content if file is small (< 5KB), otherwise summarize
                    if len(content) < 5000:
                        sync_block += f"--- File: {rel_path} ---\n{content}\n\n"
                    else:
                        sync_block += f"--- File: {rel_path} (Truncated) ---\n{content[:2000]}\n[... truncated for context efficiency ...]\n\n"
                    
                    files_processed += 1
                except Exception:
                    continue

    sync_block += "### [END OF SYNC BLOCK] ###"
    return sync_block, files_processed

if __name__ == "__main__":
    target_path = os.getcwd()
    if len(sys.argv) > 1:
        target_path = sys.argv[1]
        
    data, count = get_project_sync_data(target_path)
    
    print("-" * 30)
    print(f"Sync complete. Processed {count} files.")
    print("COPY THE CONTENT BELOW TO YOUR AI ASSISTANT:")
    print("-" * 30)
    print(data)
    print("-" * 30)

