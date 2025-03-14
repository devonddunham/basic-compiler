# BASIC Compiler

## Overview
This project is a compiler for a simple interpreted language inspired by BASIC. The compiler reads a source file written in this language and generates equivalent C++ code.

## Features
- Lexical analysis using a custom lexer (`Lexer` class).
- Parsing with a recursive descent parser (`Parser` class).
- Code emission to generate valid C++ output (`Emitter` class).
- Supports basic arithmetic operations, variable assignments, conditional statements, loops, and input/output operations.
- Error handling for invalid syntax and undeclared labels.

## Supported Language Constructs
- **Variable Declaration and Assignment**:
  ```
  LET a = 10
  ````
- **Input and Output**:
  ```
  PRINT "Hello, world!"
  INPUT x
  ```
- **Conditional Statements**:
  ```
  IF x > 10 THEN
      PRINT "X is greater than 10"
  ENDIF
  ```
- **Loops**:
  ```
  WHILE x < 5 REPEAT
      PRINT x
      LET x = x + 1
  ENDWHILE
  ```
- **Goto and Labels**:
  ```
  LABEL start
  PRINT "Looping"
  GOTO start
  ```

## Project Structure
```
.
├── basic.py        # Main compiler driver
├── lex.py          # Lexer implementation
├── parse.py        # Parser implementation
├── emit.py         # Code emitter for generating C++ output
└── README.md       # Project documentation
```

## Installation & Usage
### Prerequisites
- Python 3.x
- C++ compiler (e.g., g++)

### Running the Compiler
```sh
python basic.py <sourcefile>
```
This generates an `out.cpp` file containing the compiled C++ code.

### Compiling the Generated Code
```sh
g++ out.cpp -o output
./output
```

## Example Program
### BASIC Source Code
```
# Computer average of numbers
LET a = 0
WHILE a < 1 REPEAT
    PRINT "Enter number of scores: "
    INPUT a
ENDWHILE

LET b = 0
LET s = 0
PRINT "Enter one value at a time: "
WHILE b < a REPEAT
    INPUT c
    LET s = s + c
    LET b = b + 1
ENDWHILE

PRINT "Average: "
PRINT s / a
```
### Generated C++ Code
```cpp
#include <iostream>
using namespace std;

int main() {
    double a = 0;
    while (a < 1) {
        cout << "Enter number of scores: " << endl;
        cin >> a;
    }

    double b = 0;
    double s = 0;
    cout << "Enter one value at a time: " << endl;
    while (b < a) {
        double c;
        cin >> c;
        s = s + c;
        b = b + 1;
    }
    cout << "Average: " << endl;
    cout << s / a << endl;
    return 0;
}
```

