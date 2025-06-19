import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def get_subpage_links(base_url):
    """
    Extrai todos os links de subpáginas de uma URL base.

    Args:
        base_url (str): A URL principal do site de documentação (ex: "www.exemplo.com.br").

    Returns:
        list: Uma lista de URLs de subpáginas únicas.
    """
    print(f"Buscando links em: {base_url}")
    try:
        # Faz a requisição HTTP para obter o conteúdo da página
        response = requests.get(base_url)
        response.raise_for_status()  # Lança uma exceção para códigos de status HTTP de erro (4xx ou 5xx)
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar a URL {base_url}: {e}")
        return []

    # Cria um objeto BeautifulSoup para analisar o HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    subpage_links = set()  # Usamos um conjunto para armazenar links únicos
    base_netloc = urlparse(base_url).netloc # Domínio da URL base

    # Encontra todas as tags <a> (âncoras/links)
    for link_tag in soup.find_all('a', href=True):
        href = link_tag['href']

        # Converte o link para uma URL absoluta
        full_url = urljoin(base_url, href)

        # Analisa a URL completa para verificar o domínio e o fragmento (âncora)
        parsed_full_url = urlparse(full_url)

        # Filtra links que são:
        # 1. Âncoras internas na mesma página (ex: #section-id)
        # 2. Links que não pertencem ao mesmo domínio (opcional, dependendo da necessidade)
        # 3. Links para arquivos (ex: .pdf, .zip - você pode adicionar mais extensões)
        # 4. Links de e-mail (mailto:)
        if parsed_full_url.fragment:  # Ignora âncoras internas
            continue
        if parsed_full_url.netloc != base_netloc: # Garante que o link é do mesmo domínio
            continue
        if any(full_url.endswith(ext) for ext in ['.pdf', '.zip', '.tar.gz', '.rar']): # Ignora arquivos
            continue
        if full_url.startswith('mailto:'): # Ignora links de e-mail
            continue

        # Adiciona o link ao conjunto se passar pelos filtros
        # Remove o fragmento para evitar duplicatas para a mesma página com âncoras diferentes
        clean_url = urljoin(full_url, parsed_full_url.path) # Garante que o path seja o "limpo" sem fragmento
        subpage_links.add(clean_url)

    return sorted(list(subpage_links)) # Retorna a lista de links únicos e ordenados

if __name__ == "__main__":
    # Exemplo de uso com a URL da CrewAI
    # Observe que para sites com conteúdo muito dinâmico (JavaScript),
    # pode ser necessário usar bibliotecas como Selenium para simular um navegador.
    # No entanto, este script deve funcionar para a maioria dos sites com links HTML tradicionais.
    url_exemplo = "https://docs.crewai.com/introduction"
    links_encontrados = get_subpage_links(url_exemplo)


    if links_encontrados:
        print("\nLinks de subpáginas encontrados:")
        for link in links_encontrados:
            print(link)
        # Exporta os links para um arquivo txt na pasta output, nomeado pelo domínio do site
        from urllib.parse import urlparse
        import os
        dominio = urlparse(url_exemplo).netloc.replace('.', '_')
        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, f"links_{dominio}.txt")
        with open(output_path, "w", encoding="utf-8") as f:
            for link in links_encontrados:
                f.write(link + "\n")
        print(f"\n{len(links_encontrados)} links exportados para {output_path}")
    else:
        print("\nNenhum link de subpágina encontrado ou erro ao processar a página.")

    # Você pode testar com outras URLs aqui
    # url_outra = "https://www.python.org/doc/"
    # links_outra = get_subpage_links(url_outra)
    # if links_outra:
    #     print("\nLinks de subpáginas em outro site:")
    #     for link in links_outra:
    #         print(link)
