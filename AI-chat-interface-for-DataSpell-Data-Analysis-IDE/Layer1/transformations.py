import pandas as pd
from typing import List, Callable, Dict

def filter_rows_by_predicate(df: pd.DataFrame, predicates: List[Callable]) -> pd.DataFrame:
    """
    Filter rows from a DataFrame based on a list of predicates.
    """
    if df.empty:
        raise ValueError("Input DataFrame is empty")
    
    if not predicates:
        raise ValueError("No predicates provided")

    filtered_df = df.copy()
    for predicate in predicates:
        filtered_df = filtered_df[filtered_df.apply(predicate, axis=1)]

    return filtered_df.reset_index(drop=True)

def select_columns(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
    """
    Select specific columns from a DataFrame.
    """
    if df.empty:
        raise ValueError("Input DataFrame is empty")

    if not columns:
        raise ValueError("No columns provided")

    return df[columns]

def apply_transformations(df: pd.DataFrame, transformations: List[dict]) -> pd.DataFrame:
    """
    Apply a list of transformations to a DataFrame.

    Args:
        df (pd.DataFrame): The input DataFrame.
        transformations (List[dict]): A list of transformation dictionaries.

    Returns:
        pd.DataFrame: The transformed DataFrame.

    Raises:
        ValueError: If any transformation is invalid.
    """
    if df.empty:
        raise ValueError("Input DataFrame is empty")

    if not transformations:
        raise ValueError("No transformations provided")

    transformed_df = df.copy()

    for transformation in transformations:
        validate_transformation(transformation)
        if transformation["operation"] == "filter":
            predicates = transformation.get("predicates", [])
            if not predicates:
                raise ValueError(f"Filter operation missing predicates: {transformation}")

            # Convert predicates to lambdas
            lambda_predicates = []
            for predicate in predicates:
                try:
                    # Înlocuim operatorii specifici limbajului natural cu funcții Python valide
                    if "contains" in predicate:
                        column, value = predicate.split(" contains ")
                        column = column.strip()
                        value = value.strip().strip("'")
                        lambda_predicates.append(lambda row, col=column, val=value: val in str(row[col]))

                    elif "starts with" in predicate:
                        column, value = predicate.split(" starts with ")
                        column = column.strip()
                        value = value.strip().strip("'")
                        lambda_predicates.append(lambda row, col=column, val=value: str(row[col]).startswith(val))

                    elif "ends with" in predicate:
                        column, value = predicate.split(" ends with ")
                        column = column.strip()
                        value = value.strip().strip("'")
                        lambda_predicates.append(lambda row, col=column, val=value: str(row[col]).endswith(val))

                    else:
                        # Tratarea cazurilor normale (cum ar fi ==, >, <, etc.)
                        column, operator, value = predicate.split(' ', 2)
                        value = eval(value)  # Convertim valoarea în Python (ex: '10' -> 10)
                        if operator == "==":
                            lambda_predicates.append(lambda row, col=column, val=value: row[col] == val)
                        elif operator == "!=":
                            lambda_predicates.append(lambda row, col=column, val=value: row[col] != val)
                        elif operator == ">":
                            lambda_predicates.append(lambda row, col=column, val=value: row[col] > val)
                        elif operator == "<":
                            lambda_predicates.append(lambda row, col=column, val=value: row[col] < val)
                        elif operator == ">=":
                            lambda_predicates.append(lambda row, col=column, val=value: row[col] >= val)
                        elif operator == "<=":
                            lambda_predicates.append(lambda row, col=column, val=value: row[col] <= val)
                        else:
                            raise ValueError(f"Unsupported operator: {operator}")

                except Exception as e:
                    raise ValueError(f"Invalid predicate format: {predicate}. Error: {e}")


            transformed_df = filter_rows_by_predicate(transformed_df, lambda_predicates)

        elif transformation["operation"] == "select":
            columns = transformation.get("columns", [])
            if not columns:
                raise ValueError(f"Select operation missing columns: {transformation}")
            transformed_df = select_columns(transformed_df, columns)
        else:
            raise ValueError(f"Unsupported operation: {transformation['operation']}")
    return transformed_df

def validate_transformation(transformation: dict):
    """
    Validate a single transformation dictionary.
    """
    if "operation" not in transformation:
        raise ValueError(f"Transformation missing 'operation': {transformation}")
    if transformation["operation"] == "filter":
        if "predicates" not in transformation or not isinstance(transformation["predicates"], list):
            raise ValueError(f"Filter operation requires 'predicates': {transformation}")
    elif transformation["operation"] == "select":
        if "columns" not in transformation or not isinstance(transformation["columns"], list):
            raise ValueError(f"Select operation requires 'columns': {transformation}")
    else:
        raise ValueError(f"Unknown operation: {transformation['operation']}")
