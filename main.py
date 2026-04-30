"""
Sistema de Automacao Digital - Gestao de Pecas, Qualidade e Armazenamento
=========================================================================

Prototipo desenvolvido em Python para auxiliar uma industria no controle
de producao e qualidade das pecas fabricadas em sua linha de montagem.

Criterios de qualidade:
  - Peso entre 95g e 105g
  - Cor azul ou verde
  - Comprimento entre 10cm e 20cm

Trabalho de Algoritmos e Logica de Programacao - UniFECAF
"""

import sys
import io

# Garante saida UTF-8 no Windows (para acentos e emojis no terminal).
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


# ========================================================================
# CONSTANTES (regras de negocio centralizadas)
# ========================================================================
PESO_MIN = 95.0
PESO_MAX = 105.0
COMPRIMENTO_MIN = 10.0
COMPRIMENTO_MAX = 20.0
CORES_PERMITIDAS = ("azul", "verde")
CAPACIDADE_CAIXA = 10


# ========================================================================
# ESTRUTURAS DE DADOS GLOBAIS
# ========================================================================
pecas = []              # Lista com todas as pecas (cada peca e um dict).
caixas_fechadas = []    # Lista de caixas fechadas (cada caixa e uma lista).
caixa_atual = []        # Caixa em montagem.


# ========================================================================
# FUNCOES DE LEITURA / VALIDACAO DE ENTRADA
# ========================================================================
def ler_float(mensagem):
    """Le um numero decimal, repetindo ate receber valor valido."""
    while True:
        entrada = input(mensagem).strip().replace(",", ".")
        try:
            return float(entrada)
        except ValueError:
            print("  ⚠ Valor invalido. Digite um numero (ex: 100.5).")


def ler_texto(mensagem):
    """Le um texto nao vazio."""
    while True:
        entrada = input(mensagem).strip()
        if entrada:
            return entrada
        print("  ⚠ O campo nao pode ficar vazio.")


# ========================================================================
# REGRA DE QUALIDADE
# ========================================================================
def avaliar_peca(peso, cor, comprimento):
    """
    Avalia uma peca segundo os criterios.
    Retorna (aprovada: bool, motivos: list[str]).
    """
    motivos = []

    if not (PESO_MIN <= peso <= PESO_MAX):
        motivos.append(
            f"peso fora do intervalo ({peso}g, esperado {PESO_MIN}-{PESO_MAX}g)"
        )

    if cor.lower() not in CORES_PERMITIDAS:
        motivos.append(
            f"cor nao permitida ('{cor}', esperado {' ou '.join(CORES_PERMITIDAS)})"
        )

    if not (COMPRIMENTO_MIN <= comprimento <= COMPRIMENTO_MAX):
        motivos.append(
            f"comprimento fora do intervalo ({comprimento}cm, "
            f"esperado {COMPRIMENTO_MIN}-{COMPRIMENTO_MAX}cm)"
        )

    return len(motivos) == 0, motivos


# ========================================================================
# ARMAZENAMENTO EM CAIXAS
# ========================================================================
def armazenar_em_caixa(peca):
    """Coloca peca aprovada na caixa atual; fecha e abre nova se encher."""
    global caixa_atual

    caixa_atual.append(peca)
    if len(caixa_atual) >= CAPACIDADE_CAIXA:
        caixas_fechadas.append(caixa_atual)
        print(
            f"  📦 Caixa #{len(caixas_fechadas)} fechada com "
            f"{CAPACIDADE_CAIXA} pecas. Iniciando nova caixa."
        )
        caixa_atual = []


def reorganizar_caixas():
    """Reagrupa todas as pecas aprovadas em caixas (usado apos remocao)."""
    global caixa_atual, caixas_fechadas

    aprovadas = [p for p in pecas if p["aprovada"]]
    caixas_fechadas = []
    caixa_atual = []

    for peca in aprovadas:
        caixa_atual.append(peca)
        if len(caixa_atual) >= CAPACIDADE_CAIXA:
            caixas_fechadas.append(caixa_atual)
            caixa_atual = []


# ========================================================================
# OPCAO 1 - CADASTRAR NOVA PECA
# ========================================================================
def cadastrar_peca():
    """Cadastra uma nova peca e a avalia automaticamente."""
    print("\n--- Cadastro de Nova Peca ---")

    id_peca = ler_texto("ID da peca: ")

    if any(p["id"] == id_peca for p in pecas):
        print(f"  ⚠ Ja existe uma peca com o ID '{id_peca}'. Cadastro cancelado.")
        return

    peso = ler_float("Peso (g): ")
    cor = ler_texto("Cor: ").lower()
    comprimento = ler_float("Comprimento (cm): ")

    aprovada, motivos = avaliar_peca(peso, cor, comprimento)

    peca = {
        "id": id_peca,
        "peso": peso,
        "cor": cor,
        "comprimento": comprimento,
        "aprovada": aprovada,
        "motivos": motivos,
    }
    pecas.append(peca)

    if aprovada:
        print(f"  ✅ Peca '{id_peca}' APROVADA.")
        armazenar_em_caixa(peca)
    else:
        print(f"  ❌ Peca '{id_peca}' REPROVADA. Motivos:")
        for m in motivos:
            print(f"     - {m}")


# ========================================================================
# OPCAO 2 - LISTAR PECAS APROVADAS / REPROVADAS
# ========================================================================
def listar_pecas():
    """Lista as pecas separadas por status."""
    print("\n--- Listagem de Pecas ---")

    if not pecas:
        print("  Nenhuma peca cadastrada ainda.")
        return

    aprovadas = [p for p in pecas if p["aprovada"]]
    reprovadas = [p for p in pecas if not p["aprovada"]]

    print(f"\n✅ APROVADAS ({len(aprovadas)}):")
    if aprovadas:
        for p in aprovadas:
            print(
                f"  - ID: {p['id']:<10} | peso: {p['peso']}g | "
                f"cor: {p['cor']:<6} | comprimento: {p['comprimento']}cm"
            )
    else:
        print("  (nenhuma)")

    print(f"\n❌ REPROVADAS ({len(reprovadas)}):")
    if reprovadas:
        for p in reprovadas:
            print(
                f"  - ID: {p['id']:<10} | peso: {p['peso']}g | "
                f"cor: {p['cor']:<6} | comprimento: {p['comprimento']}cm"
            )
            for m in p["motivos"]:
                print(f"      · {m}")
    else:
        print("  (nenhuma)")


# ========================================================================
# OPCAO 3 - REMOVER PECA
# ========================================================================
def remover_peca():
    """Remove uma peca pelo ID (e reorganiza caixas se necessario)."""
    print("\n--- Remocao de Peca ---")

    if not pecas:
        print("  Nenhuma peca cadastrada para remover.")
        return

    id_peca = ler_texto("ID da peca a remover: ")

    for i, p in enumerate(pecas):
        if p["id"] == id_peca:
            era_aprovada = p["aprovada"]
            pecas.pop(i)
            print(f"  🗑 Peca '{id_peca}' removida.")
            if era_aprovada:
                reorganizar_caixas()
                print("  ♻ Caixas reorganizadas.")
            return

    print(f"  ⚠ Nenhuma peca encontrada com o ID '{id_peca}'.")


# ========================================================================
# OPCAO 4 - LISTAR CAIXAS FECHADAS
# ========================================================================
def listar_caixas_fechadas():
    """Lista todas as caixas que ja foram fechadas."""
    print("\n--- Caixas Fechadas ---")

    if not caixas_fechadas:
        print("  Nenhuma caixa fechada ate o momento.")
    else:
        for i, caixa in enumerate(caixas_fechadas, start=1):
            print(f"\n📦 Caixa #{i} ({len(caixa)} pecas):")
            for p in caixa:
                print(
                    f"  - ID: {p['id']:<10} | peso: {p['peso']}g | "
                    f"cor: {p['cor']:<6} | comprimento: {p['comprimento']}cm"
                )

    if caixa_atual:
        print(
            f"\n📋 Caixa em montagem: {len(caixa_atual)}/"
            f"{CAPACIDADE_CAIXA} pecas (ainda nao fechada)."
        )


# ========================================================================
# OPCAO 5 - RELATORIO FINAL
# ========================================================================
def gerar_relatorio():
    """Gera um relatorio consolidado da operacao."""
    print("\n" + "=" * 55)
    print("           RELATORIO CONSOLIDADO DE PRODUCAO")
    print("=" * 55)

    total = len(pecas)
    aprovadas = [p for p in pecas if p["aprovada"]]
    reprovadas = [p for p in pecas if not p["aprovada"]]

    print(f"\nTotal de pecas processadas: {total}")
    print(f"  ✅ Aprovadas: {len(aprovadas)}")
    print(f"  ❌ Reprovadas: {len(reprovadas)}")

    if reprovadas:
        contagem_motivos = {}
        for p in reprovadas:
            for m in p["motivos"]:
                tipo = m.split("(")[0].strip()
                contagem_motivos[tipo] = contagem_motivos.get(tipo, 0) + 1

        print("\nDetalhamento das reprovacoes:")
        for p in reprovadas:
            print(f"  - Peca '{p['id']}':")
            for m in p["motivos"]:
                print(f"      · {m}")

        print("\nResumo por tipo de falha:")
        for tipo, qtd in contagem_motivos.items():
            print(f"  · {tipo}: {qtd} ocorrencia(s)")

    print(f"\nArmazenamento:")
    print(f"  📦 Caixas fechadas: {len(caixas_fechadas)}")
    print(
        f"  📋 Pecas na caixa atual (nao fechada): "
        f"{len(caixa_atual)}/{CAPACIDADE_CAIXA}"
    )

    total_caixas_usadas = len(caixas_fechadas) + (1 if caixa_atual else 0)
    print(f"  Total de caixas utilizadas: {total_caixas_usadas}")

    if total > 0:
        taxa = (len(aprovadas) / total) * 100
        print(f"\nTaxa de aprovacao: {taxa:.1f}%")

    print("=" * 55)


# ========================================================================
# MENU PRINCIPAL
# ========================================================================
def exibir_menu():
    print("\n" + "=" * 55)
    print("  SISTEMA DE GESTAO DE PECAS - LINHA DE MONTAGEM")
    print("=" * 55)
    print("  1 - Cadastrar nova peca")
    print("  2 - Listar pecas aprovadas/reprovadas")
    print("  3 - Remover peca cadastrada")
    print("  4 - Listar caixas fechadas")
    print("  5 - Gerar relatorio final")
    print("  0 - Sair")
    print("=" * 55)


def main():
    print("\n🏭 Bem-vindo ao Sistema de Automacao Industrial!")

    while True:
        exibir_menu()
        opcao = input("Escolha uma opcao: ").strip()

        if opcao == "1":
            cadastrar_peca()
        elif opcao == "2":
            listar_pecas()
        elif opcao == "3":
            remover_peca()
        elif opcao == "4":
            listar_caixas_fechadas()
        elif opcao == "5":
            gerar_relatorio()
        elif opcao == "0":
            print("\nEncerrando o sistema. Ate logo! 👋\n")
            break
        else:
            print("  ⚠ Opcao invalida. Tente novamente.")


if __name__ == "__main__":
    main()
