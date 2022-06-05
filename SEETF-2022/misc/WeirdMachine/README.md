# WeirdMachine™

**Author**: zeyu2001

**Category**: Misc

[Solution](./solve.md)

## Description

You're interviewing for a CS major at Hogwarts.

"Here at Hogwarts, our computers are a bit... different. Can you help us write a few programs on our WeirdMachine™?"

Architecture:

- The WeirdMachine is a collection of up to 10 smaller computers, each with 10 registers storing values from -1000 to 1000.
- At the beginning of the program, we start off with only 1 computer, and its first two registers R0 and R1 are loaded with the program inputs.

Instructions:

- `SET x, y`: Set `Rx` to the value `y`.
- `ADD x, y`: Set `Rx` to the value of `Rx + Ry`.
- `NEG x`: Clone the current computer, and add this clone to the collection of computers within the WeirdMachine. In the cloned computer, `Rx` is multiplied by -1.
- `JIZ x, y`: If `Rx` == 0, jump to instruction `y`. Instructions start from index 0.
- `JNZ x, y`: If `Rx` != 0, jump to instruction `y`. Instructions start from index 0.
- `HALT x`: Stop the program. The output of the program is the value of `Rx`.

All cloned computers as a result of `NEG` will run in parallel (i.e. run one instruction per tick). The first computer that `HALT`s will return the answer to the entire program, regardless of whether other computers are still running.

The challenge: Write a script that performs `R0 * R1`.

## Difficulty

Medium

## Deployment

`docker-compose up -d`
