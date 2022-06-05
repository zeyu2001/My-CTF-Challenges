# WeirdMachine™ - Solution

**Author**: zeyu2001

**Category**: Misc

Standard assembly programming with a twist. Multiplication is done by repeated addition, but there are a few caveats.

1. To make this work for negative numbers, we must negate one of the numbers. But in doing so, we create two parallel computers, and we need to figure out which one we're in.
2. Notice that between the two computers, only the one with the positive value will `HALT` (the one with the negative value will count down infinitely).
3. Therefore, by the end of the loop, if we're in the original computer, then the number was positive. If we're in the negated one, then the number was negative. The latter case will return a wrong answer, because we've performed the multiplication on the absolute value of the number instead.
4. We can detect this case by adding the negated value with the original value, and add an additional branch where we negate the final answer before `HALT`-ing. This will give us the correct answer.
5. Note that when doing the second negation above, a similar issue arises - we will therefore only return in the case where we are in the negated machine, and create an infinite loop in the other.

```text
SET 2 -1
JIZ 1 13
ADD 4 1
NEG 1
ADD 4 1
ADD 3 0
ADD 1 2
JNZ 1 5
JNZ 4 13
ADD 5 3
NEG 3
ADD 5 3
JNZ 5 12
HALT 3
```
