Greeting Builder
beginner

Greeting Builder
================

Build a small greeting helper from reusable string functions.

Start building, submit solution and get feedback from the community.

Start Working
Greeting Builder
================

Build a small greeting helper. The main function, `createGreeting`, should take a person's first name, last name, and time of day, then return one greeting string.

Write these functions:

* `formatName(firstName, lastName)` should return the first and last name as one string.
* `getGreeting(timeOfDay)` should return `"Good morning"`, `"Good afternoon"`, or `"Good evening"`.
* `createGreeting(firstName, lastName, timeOfDay)` should use the other two functions and return the final greeting.

Sample checks:

js

```
console.log(createGreeting('Ava', 'Stone', 'morning'));console.log(createGreeting('Noah', 'Kim', 'evening'));console.log(createGreeting('Mina', 'Patel', 'afternoon'));
```

Expected output:

txt

```
Good morning, Ava StoneGood evening, Noah KimGood afternoon, Mina Patel
```

Your functions should return strings. Use `console.log` only to test your answer.

Solution

Solution:

js

```
function formatName(firstName, lastName) {  return `${firstName} ${lastName}`;}function getGreeting(timeOfDay) {  if (timeOfDay === 'morning') {    return 'Good morning';  }  if (timeOfDay === 'afternoon') {    return 'Good afternoon';  }  return 'Good evening';}function createGreeting(firstName, lastName, timeOfDay) {  const greeting = getGreeting(timeOfDay);  const name = formatName(firstName, lastName);  return `${greeting}, ${name}`;}console.log(createGreeting('Ava', 'Stone', 'morning'));console.log(createGreeting('Noah', 'Kim', 'evening'));console.log(createGreeting('Mina', 'Patel', 'afternoon'));
```

