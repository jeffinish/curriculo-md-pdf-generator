---
name: sync-curriculo
description: >-
  Sincroniza alterações entre os 4 arquivos de currículo (curriculo.md,
  curriculo_enus.md, curriculo_executivo.md, curriculo_executivo_enus.md).
  Use ao editar, traduzir ou resumir qualquer arquivo curriculo*.md.
---

# Sincronização de currículos

## Arquivos e papéis

| Arquivo | Papel |
|---------|-------|
| `curriculo.md` | Fonte base — PT, completo |
| `curriculo_enus.md` | Tradução EN do completo |
| `curriculo_executivo.md` | Resumo PT |
| `curriculo_executivo_enus.md` | Resumo EN |

## Workflow

### 1. Identificar origem da mudança

Determine qual arquivo foi editado e o tipo de alteração:
- Conteúdo (experiência, projeto, competência)
- Metadados (date, title no front matter)
- Correção (typo, formatação)
- Nova seção

### 2. Propagar na ordem correta

**Mudança em `curriculo.md`:**
1. Traduzir para `curriculo_enus.md`
2. Resumir em `curriculo_executivo.md`
3. Traduzir resumo para `curriculo_executivo_enus.md`

**Mudança em `curriculo_enus.md`:**
1. Refletir em `curriculo.md` (PT)
2. Atualizar `curriculo_executivo.md` e `curriculo_executivo_enus.md`

**Mudança em `curriculo_executivo.md`:**
1. Traduzir para `curriculo_executivo_enus.md`
2. Verificar consistência com `curriculo.md` (fatos não podem contradizer)

**Mudança em `curriculo_executivo_enus.md`:**
1. Refletir em `curriculo_executivo.md` (PT)
2. Verificar consistência com `curriculo_enus.md`

### 3. Regras de tradução EN

- Tom profissional, direto
- Manter títulos de cargo já usados no repositório
- Datas: formato EN (May/2025, Mar/2020 – Dec/2021)
- Localização: "Brazil" (não "Brasil")

### 4. Regras de resumo executivo

- Bullets curtos (1–3 por experiência)
- Incluir todos os projetos relevantes do completo (versão condensada)
- Omitir seção Interesses (decisão do projeto)
- Manter `header-includes` com enumitem para consistência visual no PDF

### 5. Front matter YAML

Preservar em todos os arquivos:

```yaml
geometry: margin=1.8cm
fontsize: 11pt
colorlinks: true
header-includes:
  - \usepackage{enumitem}
  - \setlist{itemsep=1pt, topsep=2pt}
```

Versões executivas usam título com "Currículo Técnico" / "Technical Resume".

### 6. Checklist final

- [ ] Contato idêntico nos 4 arquivos
- [ ] `date` alinhado entre pares completo/executivo
- [ ] `scikit-learn` (não `sckit-learn`)
- [ ] Status do doutorado consistente
- [ ] Nenhum artefato de edição (ex.: `n+` em títulos)
- [ ] PDFs não commitados
