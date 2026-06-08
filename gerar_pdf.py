import argparse
import hashlib
import logging
import os
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_SOURCE = os.path.join(SCRIPT_DIR, "templates", "eisvogel-windows-fix.latex")


def _file_hash(path: str) -> str:
    """Calcula hash SHA-256 de um arquivo."""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def garantir_template_eisvogel() -> None:
    """
    Garante que o template Eisvogel esteja instalado e atualizado.

    Copia do repositório para %APPDATA% se ausente ou se o conteúdo divergir.
    """
    template_dir = os.path.join(os.environ["APPDATA"], "pandoc", "templates")
    template_file = os.path.join(template_dir, "eisvogel-windows-fix.latex")

    if not os.path.exists(TEMPLATE_SOURCE):
        logging.error(
            "Arquivo 'eisvogel-windows-fix.latex' não encontrado em templates/."
        )
        sys.exit(1)

    os.makedirs(template_dir, exist_ok=True)

    needs_copy = not os.path.exists(template_file)
    if not needs_copy:
        needs_copy = _file_hash(TEMPLATE_SOURCE) != _file_hash(template_file)

    if needs_copy:
        logging.info("Sincronizando template Eisvogel-windows-fix...")
        shutil.copy(TEMPLATE_SOURCE, template_file)
        logging.info(f"Template instalado em: {template_file}")
    else:
        logging.info("Template Eisvogel-windows-fix atualizado.")


def localizar_executavel(nome: str) -> str | None:
    """
    Tenta localizar um executável no PATH ou em locais padrão do Windows.

    Returns:
        Caminho do executável ou None se não encontrado.
    """
    caminho = shutil.which(nome)
    if caminho:
        return caminho

    caminhos_comuns = [
        fr"C:\Program Files\Pandoc\{nome}.exe",
        fr"C:\Program Files (x86)\Pandoc\{nome}.exe",
        fr"C:\Users\{os.getlogin()}\AppData\Local\Pandoc\{nome}.exe",
        fr"C:\Users\{os.getlogin()}\AppData\Local\Programs\MiKTeX\miktex\bin\x64\{nome}.exe",
    ]

    for c in caminhos_comuns:
        if os.path.exists(c):
            return c

    return None


def gerar_pdf(
    md: str,
    pandoc: str,
    xelatex: str,
    use_css: bool,
) -> tuple[str, bool, str | None]:
    """
    Gera um PDF a partir de um arquivo Markdown.

    Returns:
        Tupla (md, sucesso, mensagem_de_erro).
    """
    pdf = md.replace(".md", ".pdf")
    cmd = [
        pandoc,
        md,
        "--from", "markdown",
        "--template", "eisvogel-windows-fix",
        "--syntax-highlighting=idiomatic",
        "-o", pdf,
        "--pdf-engine", xelatex,
    ]

    if use_css:
        cmd.extend(["--css", "style.css"])

    logging.info(f"Gerando PDF para: {md} -> {pdf}")

    try:
        subprocess.run(cmd, check=True, cwd=SCRIPT_DIR)
        logging.info(f"PDF gerado: {pdf}")
        return md, True, None
    except subprocess.CalledProcessError as e:
        return md, False, str(e)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Gerador de PDFs a partir de arquivos Markdown usando Pandoc."
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--all", action="store_true", help="Gerar PDF para todos os currículos."
    )
    group.add_argument(
        "--file", type=str, help="Gerar PDF apenas para o arquivo especificado (.md)."
    )
    parser.add_argument(
        "--jobs",
        type=int,
        default=None,
        help="Número de compilações paralelas (padrão: min(4, CPUs disponíveis)).",
    )

    args = parser.parse_args()
    logging.info("Preparando o ambiente...")

    os.chdir(SCRIPT_DIR)

    garantir_template_eisvogel()

    logging.info("Localizando Pandoc...")
    pandoc = localizar_executavel("pandoc")
    if not pandoc:
        logging.error("Pandoc não encontrado.")
        logging.info("Baixe em: https://pandoc.org/installing.html")
        sys.exit(1)
    logging.info(f"Pandoc encontrado em: {pandoc}")

    logging.info("Localizando XeLaTeX...")
    xelatex = localizar_executavel("xelatex")
    if not xelatex:
        logging.error("XeLaTeX não encontrado.")
        logging.info("Instale o MiKTeX: https://miktex.org/download")
        sys.exit(1)
    logging.info(f"XeLaTeX encontrado em: {xelatex}")

    arquivos_para_gerar: list[str] = []

    if args.all:
        arquivos_md = [
            f
            for f in os.listdir(".")
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

    use_css = os.path.exists("style.css")
    jobs = args.jobs if args.jobs is not None else min(4, os.cpu_count() or 1)
    jobs = max(1, min(jobs, len(arquivos_para_gerar)))

    if jobs == 1 or len(arquivos_para_gerar) == 1:
        erros = []
        for md in arquivos_para_gerar:
            _, ok, err = gerar_pdf(md, pandoc, xelatex, use_css)
            if not ok:
                erros.append((md, err))
        if erros:
            for md, err in erros:
                logging.error(f"ERRO ao gerar {md}: {err}")
            sys.exit(1)
    else:
        logging.info(f"Gerando {len(arquivos_para_gerar)} PDFs com {jobs} jobs paralelos...")
        erros = []
        with ThreadPoolExecutor(max_workers=jobs) as executor:
            futures = {
                executor.submit(gerar_pdf, md, pandoc, xelatex, use_css): md
                for md in arquivos_para_gerar
            }
            for future in as_completed(futures):
                md, ok, err = future.result()
                if not ok:
                    erros.append((md, err))
        if erros:
            for md, err in erros:
                logging.error(f"ERRO ao gerar {md}: {err}")
            sys.exit(1)

    logging.info("Processo concluído com sucesso!")


if __name__ == "__main__":
    main()
