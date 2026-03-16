"""
validate_schema.py
Validação automática do schema de anotação bilíngue EN/PT
Projeto: llm-annotation-testset
Autor: Renata Araújo
"""

import pandas as pd
import sys
import os


# ── Configuração do schema ────────────────────────────────────────────────────

REQUIRED_COLUMNS = [
    'id',
    'language',        # EN ou PT
    'category',        # factual | reasoning | adversarial | ambiguous | instructional | conversational
    'prompt',
    'response',
    'faithfulness',    # 1–5
    'relevance',       # 1–5
    'fluency',         # 1–5
    'completeness',    # 1–5
    'safety',          # 1–5
    'hallucination_type',  # intrinsic | extrinsic | none
    'feedback',        # texto livre obrigatório
    'annotator',       # nome ou ID do anotador
]

VALID_LANGUAGES   = ['EN', 'PT']
VALID_CATEGORIES  = ['factual', 'reasoning', 'adversarial',
                     'ambiguous', 'instructional', 'conversational']
VALID_HAL_TYPES   = ['intrinsic', 'extrinsic', 'none']
SCORE_COLUMNS     = ['faithfulness', 'relevance', 'fluency',
                     'completeness', 'safety']
SCORE_RANGE       = (1, 5)


# ── Funções de validação ──────────────────────────────────────────────────────

def check_columns(df):
    """Verifica se todas as colunas obrigatórias existem."""
    errors = []
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        errors.append(f"Colunas ausentes: {missing}")
    return errors


def check_empty_fields(df):
    """Verifica se há campos vazios em colunas obrigatórias."""
    errors = []
    for col in REQUIRED_COLUMNS:
        if col in df.columns:
            empty = df[col].isnull().sum() + (df[col] == '').sum()
            if empty > 0:
                errors.append(f"'{col}' tem {empty} campo(s) vazio(s).")
    return errors


def check_scores(df):
    """Verifica se os scores estão no range 1–5."""
    errors = []
    for col in SCORE_COLUMNS:
        if col in df.columns:
            invalid = df[~df[col].between(
                SCORE_RANGE[0], SCORE_RANGE[1])][col]
            if not invalid.empty:
                errors.append(
                    f"'{col}' tem {len(invalid)} score(s) fora do range "
                    f"{SCORE_RANGE[0]}–{SCORE_RANGE[1]}: "
                    f"linhas {invalid.index.tolist()}"
                )
    return errors


def check_categories(df):
    """Verifica se os valores categóricos são válidos."""
    errors = []

    if 'language' in df.columns:
        invalid = df[~df['language'].isin(VALID_LANGUAGES)]
        if not invalid.empty:
            errors.append(
                f"'language' tem valores inválidos: "
                f"{invalid['language'].unique().tolist()} "
                f"— aceitos: {VALID_LANGUAGES}"
            )

    if 'category' in df.columns:
        invalid = df[~df['category'].isin(VALID_CATEGORIES)]
        if not invalid.empty:
            errors.append(
                f"'category' tem valores inválidos: "
                f"{invalid['category'].unique().tolist()} "
                f"— aceitos: {VALID_CATEGORIES}"
            )

    if 'hallucination_type' in df.columns:
        invalid = df[~df['hallucination_type'].isin(VALID_HAL_TYPES)]
        if not invalid.empty:
            errors.append(
                f"'hallucination_type' tem valores inválidos: "
                f"{invalid['hallucination_type'].unique().tolist()} "
                f"— aceitos: {VALID_HAL_TYPES}"
            )

    return errors


def check_balance(df):
    """Verifica se as categorias e idiomas estão minimamente balanceados."""
    warnings = []

    if 'language' in df.columns:
        counts = df['language'].value_counts()
        for lang in VALID_LANGUAGES:
            n = counts.get(lang, 0)
            if n < 10:
                warnings.append(
                    f"Aviso: apenas {n} exemplos em '{lang}' "
                    f"— recomendado mínimo 10 por idioma."
                )

    if 'category' in df.columns:
        counts = df['category'].value_counts()
        for cat in VALID_CATEGORIES:
            n = counts.get(cat, 0)
            if n < 5:
                warnings.append(
                    f"Aviso: apenas {n} exemplos na categoria '{cat}' "
                    f"— recomendado mínimo 5 por categoria."
                )

    return warnings


def compute_weighted_score(df):
    """Calcula o score ponderado médio do dataset."""
    weights = {
        'faithfulness': 3,
        'relevance':    2,
        'fluency':      1,
        'completeness': 2,
        'safety':       3,
    }
    total_weight = sum(weights.values())  # 11

    if all(col in df.columns for col in weights):
        df['weighted_score'] = sum(
            df[col] * w for col, w in weights.items()
        ) / total_weight
        return df['weighted_score'].mean()
    return None


# ── Função principal ──────────────────────────────────────────────────────────

def validate(filepath):
    print(f"\n{'='*60}")
    print(f"Validando: {filepath}")
    print(f"{'='*60}")

    # Carregar arquivo
    try:
        df = pd.read_csv(filepath)
        print(f"✅ Arquivo carregado: {len(df)} linhas, {len(df.columns)} colunas")
    except Exception as e:
        print(f"❌ Erro ao carregar arquivo: {e}")
        return False

    all_errors   = []
    all_warnings = []

    # Rodar todas as verificações
    all_errors   += check_columns(df)
    all_errors   += check_empty_fields(df)
    all_errors   += check_scores(df)
    all_errors   += check_categories(df)
    all_warnings += check_balance(df)

    # Score ponderado
    avg_score = compute_weighted_score(df)

    # Relatório
    print(f"\n📋 RELATÓRIO DE VALIDAÇÃO")
    print(f"{'─'*40}")

    if all_errors:
        print(f"\n❌ {len(all_errors)} ERRO(S) ENCONTRADO(S):")
        for err in all_errors:
            print(f"   → {err}")
    else:
        print("✅ Nenhum erro encontrado.")

    if all_warnings:
        print(f"\n⚠️  {len(all_warnings)} AVISO(S):")
        for w in all_warnings:
            print(f"   → {w}")

    if avg_score:
        print(f"\n📊 Score ponderado médio do dataset: {avg_score:.2f}/5.00")

    print(f"\n{'─'*40}")
    if all_errors:
        print("❌ VALIDAÇÃO FALHOU — corrige os erros antes do commit.")
        return False
    else:
        print("✅ VALIDAÇÃO PASSOU — dataset pronto para commit.")
        return True


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    # Uso: python src/validate_schema.py data/annotated/dataset.csv
    # Sem argumento: valida todos os CSVs em data/annotated/

    if len(sys.argv) > 1:
        filepath = sys.argv[1]
        success = validate(filepath)
        sys.exit(0 if success else 1)
    else:
        # Valida todos os CSVs em data/annotated/
        annotated_dir = os.path.join(
            os.path.dirname(__file__), '..', 'data', 'annotated'
        )
        csv_files = [
            f for f in os.listdir(annotated_dir) if f.endswith('.csv')
        ]

        if not csv_files:
            print("Nenhum arquivo CSV encontrado em data/annotated/")
            sys.exit(0)

        results = []
        for f in csv_files:
            path = os.path.join(annotated_dir, f)
            results.append(validate(path))

        total   = len(results)
        passed  = sum(results)
        failed  = total - passed

        print(f"\n{'='*60}")
        print(f"RESUMO: {passed}/{total} arquivo(s) válido(s)")
        if failed:
            print(f"         {failed} arquivo(s) com erros — corrige antes do commit.")
        print(f"{'='*60}\n")
        sys.exit(0 if all(results) else 1)