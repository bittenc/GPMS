"""
utils/io_helpers.py

Módulo de utilitários para operações de leitura de arquivos.
Encapsula padrões comuns de I/O, mantendo o código organizado e testável.
"""

import os
import glob
import pandas as pd
from typing import Dict


def read_all_csvs(folder_path: str) -> Dict[str, pd.DataFrame]:
    """
    Lê todos os arquivos CSV presentes em uma pasta e retorna um dicionário de DataFrames.

    Cada CSV será carregado em um pandas.DataFrame. A chave do dicionário
    é o nome do arquivo (sem extensão) e o valor é o próprio DataFrame.

    Args:
        folder_path (str): Caminho absoluto ou relativo para a pasta de CSVs.

    Returns:
        Dict[str, pd.DataFrame]: Mapeamento de nome_de_arquivo → DataFrame.

    Raises:
        FileNotFoundError: Se a pasta informada não existir.
        ValueError: Se não houver arquivos .csv na pasta.
    """
    # Verifica se a pasta existe no sistema de arquivos
    if not os.path.isdir(folder_path):
        raise FileNotFoundError(f"Pasta não encontrada: '{folder_path}'")

    # Gera o padrão de busca para todos os arquivos CSV
    csv_pattern = os.path.join(folder_path, "*.csv")
    csv_paths = glob.glob(csv_pattern)

    # Se não houver arquivos CSV, informa ao usuário
    if not csv_paths:
        raise ValueError(f"Nenhum arquivo .csv encontrado em: '{folder_path}'")

    dataframes: Dict[str, pd.DataFrame] = {}

    # Itera sobre cada caminho de CSV encontrado
    for path in csv_paths:
        # Extrai o nome do arquivo (ex: "vendas.csv" → "vendas")
        filename = os.path.basename(path)
        key, _ext = os.path.splitext(filename)

        # Lê o CSV usando pandas
        try:
            df = pd.read_csv(path)
        except Exception as e:
            # Se ocorrer erro na leitura, inclui mais contexto na exceção
            raise RuntimeError(f"Erro ao ler '{path}': {e}") from e

        # Armazena o DataFrame no dicionário com a chave adequada
        dataframes[key] = df

    return dataframes
