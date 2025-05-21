# Ticket generator.
Generator of tickets for Oral Test in Linear Algebra and Geometry course on DSBA HSE.

Randomly mixes given questions into tickets so that no ticket contains too much questions on the same topic.

## How to use
To use the script for your own type of test one shall:
1. Divide your question into separate *topics*. Describe the topic in the variable `topic_code` in the file generate.py. The topic code should start with %#
    * For example, our test in autumn has topics 'matrices', 'systems', 'permutations', 'determinants', 'complex numbers', 'polynomials'.
2. Define the types of questions there are going to be in the test. 
    * For example, our test has 2 questions that are definitions, 1 question to formulate a theorem given its name, 1 interesting question on general understanding of the course, 1 question to prove a theorem.
3. For each type of question prepare an input file in plain text format. Each question should consist of 2 lines: first line should describe the topic through its topic code starting with %#, the second line should be the question itself. Any line starting with % (comment in tex) without # afterwards will be ignored.
4. Configure the names of input files in the variable *input_filenames* in the file generate.py. Configure `auxillary_filenames`.
5. Function `create_tickets` is configured at the moment to select two definitions from the same file and sort them. If your types of questions are different, change this place.
6. Change the function `check_l` as fit for your test.
7. In `main()` function change the seed used for generation and the required number of tickets.


## Version

This is version 1.0 from Fall 2022.

## License

[MIT](https://choosealicense.com/licenses/mit/)