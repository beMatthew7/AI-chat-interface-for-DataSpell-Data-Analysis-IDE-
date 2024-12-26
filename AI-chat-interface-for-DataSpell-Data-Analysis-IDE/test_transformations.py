import pandas as pd
from Layer1.transformations import select_columns, filter_rows_by_predicate

def test_select_columns():
    """
    Testează funcția select_columns pentru a selecta corect coloanele.
    """
    # Setup DataFrame
    data = {
        'name': ['John', 'Jane', 'Bob', 'Alice'],
        'age': [25, 30, 35, 40],
        'salary': [50000, 60000, 70000, 80000],
        'department': ['HR', 'IT', 'Sales', 'Marketing']
    }
    df = pd.DataFrame(data)

    # Expected Result
    expected_df = pd.DataFrame({
        'name': ['John', 'Jane', 'Bob', 'Alice'],
        'age': [25, 30, 35, 40]
    })

    # Test
    result = select_columns(df, ['name', 'age'])
    assert result.equals(expected_df), "Test failed for select_columns"

test_select_columns()
print("test_select_columns passed.")


def test_filter_rows_by_predicate():
    """
    Testează funcția filter_rows_by_predicate pentru filtrarea rândurilor.
    """
    # Setup DataFrame
    data = {
        'name': ['John', 'Jane', 'Bob', 'Alice'],
        'age': [25, 30, 35, 40],
        'salary': [50000, 60000, 70000, 80000],
        'department': ['HR', 'IT', 'Sales', 'Marketing']
    }
    df = pd.DataFrame(data)

    # Expected Result
    expected_df = pd.DataFrame({
        'name': ['Bob', 'Alice'],
        'age': [35, 40],
        'salary': [70000, 80000],
        'department': ['Sales', 'Marketing']
    }).reset_index(drop=True)

    # Test
    predicates = [
        lambda row: row['age'] > 30,
        lambda row: row['salary'] > 60000
    ]
    result = filter_rows_by_predicate(df, predicates)
    assert result.equals(expected_df), "Test failed for filter_rows_by_predicate"

test_filter_rows_by_predicate()
print("test_filter_rows_by_predicate passed.")

