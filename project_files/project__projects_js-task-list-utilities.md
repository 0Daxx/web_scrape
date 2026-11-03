Task List Utilities
beginner

Task List Utilities
===================

Write task list helpers that return updated arrays.

Start building, submit solution and get feedback from the community.

Start Working
Task List Utilities
===================

You are writing helper functions for a task list. Each helper should return a result without mutating the original `tasks` array.

Write these functions:

* `addTask(tasks, title)` should return a new array with a new incomplete task added.
* `completeTask(tasks, taskId)` should return a new array where only the matching task is completed.
* `removeTask(tasks, taskId)` should return a new array without the matching task.
* `countIncompleteTasks(tasks)` should return the number of incomplete tasks.

Sample checks:

js

```
const tasks = [  { id: 1, title: 'Review variables', completed: true },  { id: 2, title: 'Practice functions', completed: false },];const withNewTask = addTask(tasks, 'Build task utilities');console.log(withNewTask.map((task) => task.title));const completed = completeTask(withNewTask, 2);console.log(countIncompleteTasks(completed));console.log(removeTask(completed, 1).map((task) => task.id));console.log(tasks.length);console.log(countIncompleteTasks(tasks));
```

Expected output:

txt

```
["Review variables", "Practice functions", "Build task utilities"]1[2, 3]21
```

The original `tasks` array should still have two items after these helper functions run.

Solution

Solution:

js

```
function addTask(tasks, title) {  const ids = tasks.map((task) => task.id);  const nextId = Math.max(...ids) + 1;  const newTask = { id: nextId, title, completed: false };  return [...tasks, newTask];}function completeTask(tasks, taskId) {  return tasks.map((task) => {    if (task.id !== taskId) {      return task;    }    return { ...task, completed: true };  });}function removeTask(tasks, taskId) {  return tasks.filter((task) => task.id !== taskId);}function countIncompleteTasks(tasks) {  return tasks.filter((task) => task.completed === false).length;}const tasks = [  { id: 1, title: 'Review variables', completed: true },  { id: 2, title: 'Practice functions', completed: false },];const withNewTask = addTask(tasks, 'Build task utilities');console.log(withNewTask.map((task) => task.title));const completed = completeTask(withNewTask, 2);console.log(countIncompleteTasks(completed));console.log(removeTask(completed, 1).map((task) => task.id));console.log(tasks.length);console.log(countIncompleteTasks(tasks));
```

