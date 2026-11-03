Grade Report Generator
beginner

Grade Report Generator
======================

Turn numeric scores into grade report objects.

Start building, submit solution and get feedback from the community.

Start Working
Grade Report Generator
======================

Turn a numeric score into a grade report. The report should include the letter grade, whether the student passed, and a short feedback message.

Write these functions:

* `getLetterGrade(score)` should return `"A"`, `"B"`, `"C"`, `"D"`, or `"F"` based on the score.
* `hasPassed(score)` should return `true` when the score is `60` or higher.
* `getFeedback(grade)` should return a short message for the grade.
* `createGradeReport(name, score)` should return one object with `name`, `score`, `grade`, `passed`, and `feedback`.

Sample checks:

js

```
console.log(createGradeReport('Ava', 92));console.log(createGradeReport('Noah', 48));console.log(createGradeReport('Mina', 75));console.log(createGradeReport('Sam', 60));
```

Expected output:

txt

```
{ name: "Ava", score: 92, grade: "A", passed: true, feedback: "Excellent work" }{ name: "Noah", score: 48, grade: "F", passed: false, feedback: "Keep practicing" }{ name: "Mina", score: 75, grade: "C", passed: true, feedback: "You passed" }{ name: "Sam", score: 60, grade: "D", passed: true, feedback: "You passed" }
```

Use the grade from `getLetterGrade` when choosing the feedback.

Solution

Solution:

js

```
function getLetterGrade(score) {  if (score >= 90) {    return 'A';  }  if (score >= 80) {    return 'B';  }  if (score >= 70) {    return 'C';  }  if (score >= 60) {    return 'D';  }  return 'F';}function hasPassed(score) {  return score >= 60;}function getFeedback(grade) {  if (grade === 'A') {    return 'Excellent work';  }  if (grade === 'B') {    return 'Great job';  }  if (grade === 'C' || grade === 'D') {    return 'You passed';  }  return 'Keep practicing';}function createGradeReport(name, score) {  const grade = getLetterGrade(score);  return {    name,    score,    grade,    passed: hasPassed(score),    feedback: getFeedback(grade),  };}console.log(createGradeReport('Ava', 92));console.log(createGradeReport('Noah', 48));console.log(createGradeReport('Mina', 75));console.log(createGradeReport('Sam', 60));
```

