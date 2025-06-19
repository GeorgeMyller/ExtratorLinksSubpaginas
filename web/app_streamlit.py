
import streamlit as st
from urllib.parse import urlparse
from pathlib import Path
import sys
import os

# Garante que o diretório principal está no sys.path para importar extrator.py
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))
from extrator import get_subpage_links

# Configuração da página
st.set_page_config(page_title="Extrator de Links de Subpáginas", layout="centered")

st.title("Extrator de Links de Subpáginas")
st.write("Insira a URL para extrair links de subpáginas:")

# Formulário para entrada de URL
import gettext

# Internacionalização (i18n)
LOCALE = os.getenv("LOCALE", "pt_BR")
localedir = Path(__file__).parent / "locales"
try:
    t = gettext.translation("messages", localedir=localedir, languages=[LOCALE])
    _ = t.gettext
except Exception:
    _ = lambda s: s

url = st.text_input(_("URL"), placeholder="https://exemplo.com.br")

if st.button(_("Extrair")):
    if url:
        try:
            links = get_subpage_links(url)
            if links:
                st.success(_(f"{len(links)} links encontrados!"))

                # Exibir links
                for link in links:
                    st.write(link)

                # Salvar links em arquivo
                dominio = urlparse(url).netloc.replace('.', '_')
                output_dir = Path("output")
                output_dir.mkdir(exist_ok=True)
                output_path = output_dir / f"links_{dominio}.txt"
                with open(output_path, "w", encoding="utf-8") as f:
                    for link in links:
                        f.write(link + "\n")

                st.download_button(
                    label=_("Baixar arquivo de links"),
                    data=open(output_path, "r", encoding="utf-8").read(),
                    file_name=f"links_{dominio}.txt",
                    mime="text/plain"
                )
            else:
                st.error(_("Nenhum link encontrado ou erro ao processar a página."))
        except Exception as e:
            st.error(_("Erro ao extrair links: ") + str(e))
    else:
        st.warning(_("Por favor, insira uma URL válida."))
