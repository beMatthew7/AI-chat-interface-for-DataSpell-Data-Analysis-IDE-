import pandas as pd
from Task1.Layer1.transformations import select_columns, filter_rows_by_predicate, apply_transformations


#create a simple DataFrame for testing
data = {
    'name': ['John', 'Jane', 'Bob', 'Alice'],
    'age': [25, 30, 35, 40],
    'salary': [50000, 60000, 70000, 80000],
    'department': ['HR', 'IT', 'Sales', 'Marketing']
}

df = pd.DataFrame(data)

#test the select_colums function
selected_columns = select_columns(df, ['name', 'age'])
print(selected_columns)

#test the filter_rows_by_predicate function
filtered_df = filter_rows_by_predicate(df, [lambda row: row['age'] > 30, lambda row: row['salary'] > 60000])
print(filtered_df)

# Test DataFrame
data = {
    'name': ['John', 'Jane', 'Bob', 'Alice'],
    'age': [25, 30, 35, 40],
    'salary': [50000, 60000, 70000, 80000],
    'department': ['HR', 'IT', 'Sales', 'Marketing']
}

df = pd.DataFrame(data)

# Test filter_rows_by_predicate
predicates = [lambda row: row['age'] > 30, lambda row: row['salary'] > 60000]
filtered_df = filter_rows_by_predicate(df, predicates)
print(filtered_df)

# Test select_columns
selected_df = select_columns(df, ['name', 'age'])
print(selected_df)

# Test apply_transformations
transformations = [
    {"operation": "filter", "predicates": ["lambda row: row['age'] > 30", "lambda row: row['salary'] > 60000"]},
    {"operation": "select", "columns": ["name", "age"]}
]
transformed_df = apply_transformations(df, transformations)
print(transformed_df)
