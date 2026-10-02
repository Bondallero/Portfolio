*This project was created as part of 42 curriculum by wgulinsk*

push_swap

*Description:*

push_swap is a sorting algorithm project in which a stack of integers must be sorted in ascending order using a limited set of stack operations. The challenge is not only to sort the data correctly but also to minimize the number of operations performed.

The program accepts a list of integers as command-line arguments, validates the input, stores the numbers in a stack, and outputs the sequence of operations required to sort the stack. Invalid input, duplicate numbers, and integer overflows are detected and reported with an "Error" message.

The project focuses on algorithmic thinking, efficient data structures, memory management, and writing clean, modular C code.

Features:

Input parsing and validation
Detection of invalid integers and integer overflows
Detection of duplicate values
Linked-list implementation of stacks
Implementation of all mandatory stack operations:
sa, sb, ss - swap operations 
pa, pb - push operations
ra, rb, rr - rotate operations 
rra, rrb, rrr - reverse rotate operations
Optimized sorting for small stacks
Efficient sorting algorithm for larger inputs
Memory leak-free implementation

*Instructions:*

Compilation:

Program should compile with make command. Makefile also allows following commands:
make clean - cleans object files, but leaves output file
make fclean - cleans all the both object and output file
make re - recreates

Execution:

To execute the program you should use:
./push_swap *random numbers of int or str type separated with space*

The program, in turn, must give you the set of operations (sa, sb, ss, pb, etc.) that you
need to sort the list of numbers in ascending order. Each operation should be written on a newline

*Resourses:*
Some of the websites (w3school.com, www.geeksforgeeks.org, medium.com etc), that explain, how structs work and all the other theoretic info were used.

AI was used to choose the sorting algorithm I can implement and to give me needed info on how hard it will be and, how should I split the work on the project (operations first, input checking then, later parsing and the sorting algorithm). AI was also used to write part of this README xd
