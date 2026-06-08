# curriculo-md-pdf-generator
# 📝 Currículo em Markdown + Geração Automática em PDF

Este repositório contém meu currículo em **Markdown** e um pequeno pipeline para gerar um PDF
profissional usando **Pandoc** + **XeLaTeX** + **Eisvogel Template**.

A ideia é manter um currículo:
-  Simples de editar;
-  Versionado;
-  Facil de atualizar;
-  Com visual profissional;
-  Com geração totalmente automatizada.

## Tecnologias utilizadas

- **Markdown** para edição
- **Pandoc** para conversão
- **XeLaTeX** como engine de PDF
- **Template Eisvogel** design elegante
- **CSS customizado** para estilo (não afeta PDF via LaTeX; reservado para uso futuro)
- **Python** (com logging e argparse) para automação

---

## Arquivos de currículo

O projeto mantém **4 variantes** que devem permanecer sincronizadas:

| Arquivo | Descrição |
|---------|-----------|
| `curriculo.md` | Fonte base — português, versão completa |
| `curriculo_enus.md` | Mesmo conteúdo traduzido para inglês |
| `curriculo_executivo.md` | Versão resumida em português |
| `curriculo_executivo_enus.md` | Versão resumida em inglês |

**Regra:** toda alteração em um arquivo deve ser refletida nos demais. A pasta `.cursor/` contém rules e skills que orientam o agente nesse fluxo de sincronização.

---

## 📄 Como gerar o currículo em PDF

### Usando Python

O script Python suporta três modos:

### ✔ Gerar PDF para todos os arquivos .md do diretório
*(ignora automaticamente o arquivo README.md)*

```bash
python gerar_pdf.py --all
```

### ✔ Gerar PDF para um arquivo específico

```bash
python gerar_pdf.py --file curriculo.md
```

### ✔ Geração paralela (mais rápido com múltiplos currículos)

```bash
python gerar_pdf.py --all --jobs 4
```

O padrão é `min(4, CPUs disponíveis)`. Cada job executa uma compilação XeLaTeX independente.

Após a execução, os PDFs serão gerados na raiz do projeto.

### Usando PowerShell

```powershell
.\generate_all.ps1
```

## 📁 Estrutura do Projeto

```
curriculo-md-pdf-generator/
│
├── .cursor/
│   ├── rules/                 # Regras para sincronização dos currículos
│   └── skills/                # Skills do agente (sync-curriculo)
│
├── curriculo.md               # Currículo completo (PT) — fonte base
├── curriculo_enus.md          # Currículo completo (EN)
├── curriculo_executivo.md     # Versão resumida (PT)
├── curriculo_executivo_enus.md # Versão resumida (EN)
├── README.md
├── style.css                  # Estilos opcionais (não afeta PDF LaTeX)
├── gerar_pdf.py               # Script principal em Python
├── generate_all.ps1           # Atalho para gerar todos os PDFs
│
└── templates/
    ├── eisvogel.latex
    └── eisvogel-windows-fix.latex
```

## 🎨 Personalização

Você pode ajustar:
- O conteúdo em **curriculo.md** (e propagar para os demais)
- Os estilos em **style.css**
- O template LaTeX (Eisvogel) caso queira personalizações mais profundas

## 📦 Requisitos
- **Pandoc**
- **XeLaTeX** (via MiKTeX, TeXLive ou MacTeX)
- **Template Eisvogel** (instalado/sincronizado automaticamente pelo script)

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
- Template Eisvogel (com sincronização por hash)

## 🤝 Contribuições

Sugestões, correções ou melhorias são muito bem-vindas!
Sinta-se à vontade para abrir issues ou enviar pull requests.

## 📬 Contato

Caso queira conversar sobre dados, engenharia, triathlon ou tecnologia, estou disponível no LinkedIn!

[Jefferson Silva | Linkedin](https://www.linkedin.com/in/jefferson-silva-78621197/)

Teamwork is the best work.
