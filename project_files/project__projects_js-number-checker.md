Number Checker
beginner

Number Checker
==============

Create boolean helper functions that describe a number.

Start building, submit solution and get feedback from the community.

Start Working
Number Checker
==============

Given a number, return a small report describing what kind of number it is. Use simple boolean helper functions, then combine their results in `describeNumber`.

Write these functions:

* `isPositive(number)` should return `true` when the number is greater than `0`.
* `isNegative(number)` should return `true` when the number is less than `0`.
* `isZero(number)` should return `true` when the number is exactly `0`.
* `isEven(number)` should return `true` when the number is even.
* `describeNumber(number)` should return an object with `positive`, `negative`, `zero`, `even`, and `odd` properties.

Sample checks:

js

```
console.log(describeNumber(8));console.log(describeNumber(-3));console.log(describeNumber(0));console.log(describeNumber(7));
```

Expected output:

txt

```
{ positive: true, negative: false, zero: false, even: true, odd: false }{ positive: false, negative: true, zero: false, even: false, odd: true }{ positive: false, negative: false, zero: true, even: true, odd: false }{ positive: true, negative: false, zero: false, even: false, odd: true }
```

Each checker function should return a boolean. The summary function should return a new object.

Solution

Solution:

js

```
function isPositive(number) {  return number > 0;}function isNegative(number) {  return number < 0;}function isZero(number) {  return number === 0;}function isEven(number) {  return number % 2 === 0;}function describeNumber(number) {  return {    positive: isPositive(number),    negative: isNegative(number),    zero: isZero(number),    even: isEven(number),    odd: !isEven(number),  };}console.log(describeNumber(8));console.log(describeNumber(-3));console.log(describeNumber(0));console.log(describeNumber(7));
```

