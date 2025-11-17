import subprocess
import shutil
import os
import sys
import argparse

import logging

# Configuração básica do logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# ==========================
# 1. Instalação automática do template Eisvogel
# ==========================

def garantir_template_eisvogel():
    """
        Garante que o template Eisvogel esteja instalado no diretório correto.
        O projeto utiliza uma versão corrigida do template para Windows.
    """
    template_dir = os.path.join(os.environ["APPDATA"], "pandoc", "templates")
    template_file = os.path.join(template_dir, "eisvogel-windows-fix.latex")

    # Cria a pasta se não existir
    if not os.path.exists(template_dir):
        os.makedirs(template_dir)

    # Copia o template apenas se necessário
    if not os.path.exists(template_file):
        if not os.path.exists(r".\templates\eisvogel-windows-fix.latex"):
            logging.error("Arquivo 'eisvogel-windows-fix.latex' não encontrado no diretório atual.")
            sys.exit(1)

        logging.info("Template Eisvogel-windows-fix não encontrado. Copiando para o local adequado...")
        shutil.copy(r".\templates\eisvogel-windows-fix.latex", template_file)
        logging.info(f"Template instalado em: {template_file}")
    else:
        logging.info("Template Eisvogel-windows-fix encontrado.")


# ==========================
# 2. Localização de Executáveis
# ==========================

def localizar_executavel(nome):
    """
    Tenta localizar um executável no PATH ou em locais padrão do Windows.
    Retorna None se não encontrado.
    """
    caminho = shutil.which(nome)
    if caminho:
        return caminho

    # Locais comuns no Windows
    caminhos_comuns = [
        fr"C:\Program Files\Pandoc\{nome}.exe",
        fr"C:\Program Files (x86)\Pandoc\{nome}.exe",
        fr"C:\Users\{os.getlogin()}\AppData\Local\Pandoc\{nome}.exe",
        fr"C:\Users\{os.getlogin()}\AppData\Local\Programs\MiKTeX\miktex\bin\x64\{nome}.exe"
    ]

    for c in caminhos_comuns:
        if os.path.exists(c):
            return c

    return None


# ==========================
# 3. Execução principal
# ==========================

def main():

    parser = argparse.ArgumentParser(
        description="Gerador de PDFs a partir de arquivos Markdown usando Pandoc."
    )
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--all", action="store_true", help="Gerar PDF para todos os currículos.")
    group.add_argument("--file", type=str, help="Gerar PDF apenas para o arquivo especificado (.md).")

    args = parser.parse_args()
    logging.info("Preparando o ambiente...")

    # Garante que o template esteja instalado
    garantir_template_eisvogel()

    # Localiza Pandoc
    logging.info("Localizando Pandoc...")
    pandoc = localizar_executavel("pandoc")

    if not pandoc:
        logging.error("Pandoc não encontrado.")
        logging.info("Baixe em: https://pandoc.org/installing.html")
        sys.exit(1)

    logging.info(f"Pandoc encontrado em: {pandoc}")

    # Localiza XeLaTeX
    logging.info("Localizando XeLaTeX...")
    xelatex = localizar_executavel("xelatex")

    if not xelatex:
        logging.error("XeLaTeX não encontrado.")
        logging.info("Instale o MiKTeX: https://miktex.org/download")
        sys.exit(1)

    logging.info(f"XeLaTeX encontrado em: {xelatex}")

    # --- Lógica Principal ---
    arquivos_para_gerar = []

    if args.all:
        # Busca todos os arquivos .md no diretório
        arquivos_md = [
            f for f in os.listdir(".") if f.lower().endswith(".md")
            if f.lower().endswith(".md") and f.lower() != "readme.md"
            ]

        if not arquivos_md:
            logging.error("Nenhum arquivo .md encontrado no diretório.")
            sys.exit(1)

        arquivos_para_gerar.extend(arquivos_md)

    elif args.file:
        if not os.path.exists(args.file):
            logging.error(f"Arquivo '{args.file}' não encontrado.")
            sys.exit(1)
        arquivos_para_gerar.append(args.file)

    # Gerar PDFs
    for md in arquivos_para_gerar:
        pdf = md.replace(".md", ".pdf")

        cmd = [
            pandoc,
            md,
            "--from", "markdown",
            "--template", "eisvogel-windows-fix",
            "--syntax-highlighting=idiomatic",
            "-o", pdf,
            "--pdf-engine=xelatex"
        ]

        if os.path.exists("style.css"):
            cmd.extend(["--css", "style.css"])

        logging.info(f"Gerando PDF para: {md} -> {pdf}")

        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError as e:
            logging.error(f"ERRO ao gerar {pdf}: {e}")
            sys.exit(1)

        logging.info(f"PDF gerado: {pdf}")

    logging.info("Processo concluído com sucesso!")

if __name__ == "__main__":
    main()
