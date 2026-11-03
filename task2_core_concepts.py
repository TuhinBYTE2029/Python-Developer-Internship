
# Python Developer Internship - Task 2
# Core Concepts and Skills

print("=" * 50)
print("       PYTHON CORE CONCEPTS AND SKILLS")
print("=" * 50)

# 1. Variables and Data Types
name = "Tuhin"
age = 21
height = 168.0
is_student = True

print("\n1. VARIABLES AND DATA TYPES")
print("Name:", name)
print("Age:", age)
print("Height:", height)
print("Student:", is_student)

# 2. Operators
print("\n2. OPERATORS")
a = 20
b = 10
print("Addition:", a + b)
print("Subtraction:", a - b)
print("Multiplication:", a * b)
print("Division:", a / b)

# 3. Conditional Statements
print("\n3. CONDITIONAL STATEMENTS")
marks = 85

if marks >= 80:
    print("Grade: A")
elif marks >= 60:
    print("Grade: B")
else:
    print("Grade: C")

# 4. Loops
print("\n4. LOOPS")
for i in range(1, 6):
    print("Number:", i)

# 5. Lists, Tuples, Dictionaries and Sets
print("\n5. COLLECTIONS")
fruits = ["Apple", "Banana", "Mango"]
coordinates = (10, 20)
student = {"name": name, "age": age}
unique_numbers = {1, 2, 2, 3, 4}

print("List:", fruits)
print("Tuple:", coordinates)
print("Dictionary:", student)
print("Set:", unique_numbers)

# 6. Functions
print("\n6. FUNCTIONS")

def calculate_sum(x, y):
    return x + y

print("Sum:", calculate_sum(15, 25))

# 7. Exception Handling
print("\n7. EXCEPTION HANDLING")

try:
    number = int("100")
    print("Converted number:", number)
except ValueError:
    print("Invalid input!")

# 8. File Handling
print("\n8. FILE HANDLING")

with open("sample.txt", "w") as file:
    file.write("Python Developer Internship - Task 2")

with open("sample.txt", "r") as file:
    print("File content:", file.read())

print("\n" + "=" * 50)
print("TASK 2 COMPLETED SUCCESSFULLY!")
print("=" * 50)
