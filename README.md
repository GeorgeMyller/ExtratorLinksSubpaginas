
# Extrator de Links de Subpáginas

Ferramenta Python para extrair todos os links de subpáginas de um site, com:
- Interface web via Streamlit
- Suporte a internacionalização (i18n)
- API opcional com FastAPI
- Gerenciamento moderno de dependências com [UV](https://docs.astral.sh/uv/)

> **Destaques:**
> - Rápido, fácil de usar e multiplataforma
> - Exporta links para arquivos `.txt` na pasta `output/`
> - Pronto para deploy local ou integração em outros sistemas



## Gerenciamento de Dependências com UV

Este projeto recomenda o uso do [UV](https://docs.astral.sh/uv/) para gerenciar ambientes, dependências e scripts Python de forma rápida e eficiente.

### Requisitos

- Python >= 3.12 (pode ser instalado e gerenciado pelo UV)
- [uv](https://docs.astral.sh/uv/) (gerenciador de dependências)

### Instalação do UV

No macOS e Linux:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Ou, se preferir, via pip:

```bash
pip install uv
```

### Instalando as dependências do projeto

Com UV, basta rodar:

```bash
uv pip install -r requirements.txt
# ou, se usar pyproject.toml:
uv pip install .
```

Você também pode usar o lockfile universal do UV:

```bash
uv pip compile requirements.in --universal --output-file requirements.txt
uv pip sync requirements.txt
```

**Vantagens do UV:**
- Muito mais rápido que pip tradicional (10-100x)
- Gerencia ambientes virtuais, dependências, scripts e versões do Python
- Compatível com pip, poetry, pipx, virtualenv, etc.
- Cache global eficiente
- Suporte a lockfile universal

Para mais detalhes, consulte a [documentação oficial do UV](https://docs.astral.sh/uv/).

---

## Estrutura do Projeto

```
extrator.py           # Função principal de extração de links (CLI e importável)
main.py               # Exemplo de entrypoint simples
pyproject.toml        # Configuração do projeto Python (recomendado para UV)
README.md             # Este arquivo
output/               # Saída dos arquivos de links extraídos
web/app_streamlit.py  # Interface web (Streamlit)
web/output/           # Saída da interface web
```

---


## Como usar

### 1. Linha de Comando (CLI)

Execute diretamente para testar extração de links:

```bash
python extrator.py
# Edite o arquivo para testar com outras URLs.
```

### 2. Interface Web (Streamlit)

Interface amigável para uso no navegador:

```bash
streamlit run web/app_streamlit.py
```
Depois, acesse o endereço exibido no terminal (geralmente http://localhost:8501).

Digite a URL desejada e clique em "Extrair". Os links encontrados podem ser baixados em um arquivo `.txt`.



## Internacionalização (i18n)

O sistema suporta internacionalização das mensagens. Por padrão, o idioma é português (`pt_BR`).
Para adicionar outros idiomas, crie arquivos de tradução `.po`/`.mo` em `web/locales/<idioma>/LC_MESSAGES/messages.po`.
Defina a variável de ambiente `LOCALE` para alterar o idioma:

```bash
export LOCALE=en_US
streamlit run web/app_streamlit.py
```


## Exemplo de uso como biblioteca

```python
from extrator import get_subpage_links
links = get_subpage_links("https://exemplo.com")
print(links)
```


## Observações e Dicas

- O extrator funciona melhor em sites com HTML tradicional. Para páginas muito dinâmicas (JavaScript), pode ser necessário Selenium.
- Os arquivos de saída são salvos na pasta `output/`.
- O projeto já inclui `.python-version` para facilitar o uso de múltiplas versões com UV ou pyenv.
- Para dúvidas ou sugestões, abra uma issue.

---

Desenvolvido com ❤️ por [George Myller](https://github.com/GeorgeMyller).
