import os
import time
from src.analyzer import analyze_file
from src.test_generator import generate_tests_with_ai

def main():
    samples_dir = "samples"
    target_files = [f for f in os.listdir(samples_dir) if f.endswith('.py') and f != "__init__.py"]
    
    print(f"[*] AI-Powered Test Generation Starting (GROQ FAST MODE)...")
    
    all_tests_content = "import pytest\nimport math\nfrom hypothesis import given, strategies as st\n"
    
    # Importları ekle
    for file_name in target_files:
        module_name = file_name.replace(".py", "")
        all_tests_content += f"from samples.{module_name} import *\n"
    all_tests_content += "\n"

    for file_name in target_files:
        full_path = os.path.join(samples_dir, file_name)
        print(f"\n--- Analyzing File: {file_name} ---")
        
        functions = analyze_file(full_path)
        
        for i, func in enumerate(functions):
            print(f"[+] AI (Groq) is generating tests for: {func['name']}...")
            
            test_code = generate_tests_with_ai(func['name'], func['code'])
            
            if test_code.strip().startswith("# Error"):
                print(f"[!] HATA: {func['name']} için test üretilemedi.")
                print(test_code)
            else:
                all_tests_content += f"# --- Tests for {func['name']} ---\n"
                all_tests_content += test_code + "\n\n"

    # Dosyaya yaz
    os.makedirs("tests", exist_ok=True)
    with open("tests/test_generated.py", "w", encoding="utf-8") as f:
        f.write(all_tests_content)
    
    print("-" * 30)
    print(f"[!] SUCCESS: Tüm testler saniyeler içinde üretildi! 'tests/test_generated.py' dosyasına bak.")

if __name__ == "__main__":
    main()
