import numpy as np
import pandas as pd

students = pd.read_csv("Students_Performance.csv")
print(students.head(5))
print(students.columns)
print(students['math score'])
print(students[0][3])