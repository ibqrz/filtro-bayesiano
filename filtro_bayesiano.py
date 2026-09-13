import re

# 1. BASE DE CONHECIMENTO (DICIONÁRIO DE PESOS)
PALAVRAS_CHAVE = {
    "pix": 0.9,
    "grátis": 0.8,
    "urgente": 0.7,
    "reunião": 0.1,
    "aula": 0.05,
}


def classificar_email(texto_email: str) -> dict:
    """Classifica um e-mail em 'SPAM' ou 'E-MAIL NORMAL (HAM)' com base na média dos

    pesos das palavras-chave encontradas no texto.
    """
    # Converter para minúsculas e extrair palavras
    palavras_email = re.findall(r"\w+", texto_email.lower())

    # Identificar quais palavras do e-mail estão na base de conhecimento
    palavras_encontradas = {}
    for palavra in palavras_email:
        if palavra in PALAVRAS_CHAVE:
            palavras_encontradas[palavra] = PALAVRAS_CHAVE[palavra]

    # Calcular a média dos pesos
    pesos = list(palavras_encontradas.values())
    if pesos:
        media_pesos = sum(pesos) / len(pesos)
    else:
        media_pesos = 0.0

    # Regra de Decisão
    if media_pesos >= 0.50:
        classificacao = "SPAM"
    else:
        classificacao = "E-MAIL NORMAL (HAM)"

    return {
        "texto_original": texto_email,
        "palavras_detectadas": palavras_encontradas,
        "media_pesos": media_pesos,
        "classificacao": classificacao,
    }


def exibir_relatorio(resultado: dict) -> None:
    """Imprime um relatório formatado no terminal."""
    print("\n" + "=" * 60)
    print("RELATÓRIO DE ANÁLISE DE E-MAIL")
    print("=" * 60)
    print(f'E-mail Analisado: "{resultado["texto_original"]}"\n')

    detectadas = resultado["palavras_detectadas"]
    if detectadas:
        print("Palavras da base detectadas:")
        for palavra, peso in detectadas.items():
            print(f"  - '{palavra}': peso {peso}")

        pesos_str = " + ".join(str(p) for p in detectadas.values())
        print(
            f"\nCálculo da Média: ({pesos_str}) / {len(detectadas)} = {resultado['media_pesos']:.3f}"
        )
    else:
        print("Nenhuma palavra-chave da base foi detectada.")
        print("\nCálculo da Média: 0.0")

    print(f"\nResultado Final: {resultado['classificacao']}")
    print("=" * 60 + "\n")


def menu_interativo():
    """Menu para permitir ao usuário testar os e-mails pré-definidos

    ou digitar um novo e-mail para análise.
    """
    emails_padrao = [
        "Urgente receba seu pix grátis agora",
        "Confirmação de reunião para a aula de amanhã",
    ]

    while True:
        print("--- MENU DE CLASSIFICAÇÃO DE E-MAILS ---")
        print("1. Executar Cenários Pré-definidos (E-mails Padrão)")
        print("2. Digitar um Novo E-mail")
        print("3. Sair")

        opcao = input("Escolha uma opção (1, 2 ou 3): ").strip()

        if opcao == "1":
            for email in emails_padrao:
                resultado = classificar_email(email)
                exibir_relatorio(resultado)
        elif opcao == "2":
            novo_email = input("\nDigite o texto do e-mail para análise: ")
            if novo_email.strip():
                resultado = classificar_email(novo_email)
                exibir_relatorio(resultado)
            else:
                print("\n[Aviso] O texto do e-mail não pode estar vazio.\n")
        elif opcao == "3":
            print("\nEncerrando o programa... Até logo!")
            break
        else:
            print("\n[Erro] Opção inválida! Tente novamente.\n")


if __name__ == "__main__":
    menu_interativo()