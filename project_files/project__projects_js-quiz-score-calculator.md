Quiz Score Calculator
beginner

Quiz Score Calculator
=====================

Score quiz answers and return a result summary.

Start building, submit solution and get feedback from the community.

Start Working
Quiz Score Calculator
=====================

Score a quiz by matching each question with the answer the user gave. The final result should include the count, total, percentage, and a simple message.

Write these functions:

* `isAnswerCorrect(question, userAnswer)` should return `true` when the user's answer matches the correct answer.
* `countCorrectAnswers(questions, userAnswers)` should match each question with its user answer and return the number correct.
* `calculatePercentage(correctCount, totalQuestions)` should return the percentage score.
* `getResultMessage(percentage)` should return a short message based on the percentage.
* `createQuizResult(questions, userAnswers)` should return `correctCount`, `totalQuestions`, `percentage`, and `message`.

Sample checks:

js

```
const questions = [  { id: 1, correctAnswer: 'B' },  { id: 2, correctAnswer: 'A' },  { id: 3, correctAnswer: 'D' },  { id: 4, correctAnswer: 'C' },];const userAnswers = [  { questionId: 1, answer: 'B' },  { questionId: 2, answer: 'C' },  { questionId: 3, answer: 'D' },  { questionId: 4, answer: 'C' },];console.log(createQuizResult(questions, userAnswers));console.log(countCorrectAnswers(questions, userAnswers));console.log(calculatePercentage(3, questions.length));const partialAnswers = [{ questionId: 1, answer: 'B' }];console.log(createQuizResult(questions, partialAnswers));
```

Expected output:

txt

```
{ correctCount: 3, totalQuestions: 4, percentage: 75, message: "You passed" }375{ correctCount: 1, totalQuestions: 4, percentage: 25, message: "Keep practicing" }
```

If a user answer is missing, count that question as incorrect.

Solution

Solution:

js

```
function isAnswerCorrect(question, userAnswer) {  if (!userAnswer) {    return false;  }  return question.correctAnswer === userAnswer.answer;}function countCorrectAnswers(questions, userAnswers) {  let correctCount = 0;  for (const question of questions) {    const userAnswer = userAnswers.find((answer) => {      return answer.questionId === question.id;    });    if (isAnswerCorrect(question, userAnswer)) {      correctCount += 1;    }  }  return correctCount;}function calculatePercentage(correctCount, totalQuestions) {  if (totalQuestions === 0) {    return 0;  }  return (correctCount / totalQuestions) * 100;}function getResultMessage(percentage) {  if (percentage >= 80) {    return 'Great work';  }  if (percentage >= 60) {    return 'You passed';  }  return 'Keep practicing';}function createQuizResult(questions, userAnswers) {  const correctCount = countCorrectAnswers(questions, userAnswers);  const totalQuestions = questions.length;  const percentage = calculatePercentage(correctCount, totalQuestions);  return {    correctCount,    totalQuestions,    percentage,    message: getResultMessage(percentage),  };}const questions = [  { id: 1, correctAnswer: 'B' },  { id: 2, correctAnswer: 'A' },  { id: 3, correctAnswer: 'D' },  { id: 4, correctAnswer: 'C' },];const userAnswers = [  { questionId: 1, answer: 'B' },  { questionId: 2, answer: 'C' },  { questionId: 3, answer: 'D' },  { questionId: 4, answer: 'C' },];console.log(createQuizResult(questions, userAnswers));console.log(countCorrectAnswers(questions, userAnswers));console.log(calculatePercentage(3, questions.length));const partialAnswers = [{ questionId: 1, answer: 'B' }];console.log(createQuizResult(questions, partialAnswers));
```

