# curriculo-md-pdf-generator
# 📝 Currículo em Markdown + Geração Automática em PDF

Este repositório contém meu currículo em **Markdown** e um pequeno pipeline para gerar um PDF
profissional usando **Pandoc** + **XeLaTeX** + **Eisenvogel Template**.

A ideia é manter um currículo:
-  Simples de editar;
-  Versionado;
-  Facil de atualizar;
-  Com visual profissional;
-  Com geração totalmente automatizada.

---

## Tecnologias utilizadas

- **Markdown** para edição
- **Pandoc** para conversão
- **XeLaTeX** como engine de PDF
- **Template Eisvogel** design elegante
- **CSS customizado** para estilo
- **Python** (com logging e argparse) para automação

---

## 📄 Como gerar o currículo em PDF

### Usando Python

O script Python agora suporta dois modos:

### ✔ Gerar PDF para todos os arquivos .md do diretório
*(ignora automaticamente o arquivo README.md)*

```python
python gerar_pdf.py --all
```
### ✔ Gerar PDF para um arquivo específico

```python
python gerar_pdf.py --file curriculo.md
```

Após a execução, os PDFs serão gerados na raiz do projeto.

## 📁 Estrutura do Projeto

```
curriculo-md-pdf-generator/
│
├── curriculo.md               # Currículo principal
├── curriculo_executivo.md     # Versão alternativa (por exemplo)
├── README.md                  # Arquivo atual
├── style.css                  # Estilos opcionais para o PDF
├── gerar_pdf.py               # Script principal em Python
│
└── exemplos/
    └── curriculo-exemplo.pdf
└── templates/
    └── eisvogel.latex
    └── eisvogel-windows-fix.latex
```

## 🎨 Personalização

Você pode ajustar:
- O conteúdo em **curriculo.md**
- Os estilos em **style.css**
- O template LaTeX (Eisvogel) caso queira personalizações mais profundas

## 📦 Requisitos
- **Pandoc**
- **XeLaTeX** (via MiKTeX, TeXLive ou MacTeX)
- **Template Eisvogel** (instalado automaticamente pelo script)

## 🔧 Instalação

### Linux (Ubuntu/Debian)
```bash
sudo apt install pandoc texlive-full
```

### macOS

```bash
brew install --cask mactex
brew install pandoc
```

### Windows

Baixe e instale:
- Pandoc: https://pandoc.org/installing.html
- MiKTeX: https://miktex.org/download

O script Python irá verificar automaticamente:
- Pandoc
- XeLaTeX
- Template Eisvogel

## 📚 Exemplo de currículo gerado

Você pode visualizar um exemplo em:

exemplos/curriculo-exemplo.pdf

## 🤝 Contribuições

Sugestões, correções ou melhorias são muito bem-vindas!
Sinta-se à vontade para abrir issues ou enviar pull requests.

## 📬 Contato

Caso queira conversar sobre dados, engenharia, triathlon ou tecnologia, estou disponível no LinkedIn!

[Jefferson Silva | Linkedin](https://www.linkedin.com/in/jefferson-silva-78621197/)

Teamwork is the best work.