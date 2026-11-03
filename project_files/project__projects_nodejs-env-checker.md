Env Checker
beginner

Env Checker
===========

Check required environment variables without leaking values.

Start building, submit solution and get feedback from the community.

Start Working
Env Checker
===========

You are required to build a CLI tool using Node.js that checks whether required environment variables are set.

Real projects use environment variables for values that change between machines, such as API keys, database URLs, and feature flags. Your CLI should accept environment variable names from the terminal and tell the user if any of them are missing.

Here are some example commands you can run to test your CLI:

bash

```
node env-checker.js PATHnode env-checker.js PATH API_KEY DATABASE_URLnode env-checker.js
```

On successful execution, the output should look like this:

txt

```
Set: PATHAll required environment variables are set.
```

If one or more environment variables are missing, print a friendly error:

txt

```
error: missing environment variables: API_KEY, DATABASE_URL
```

If the user does not pass any names, print this error:

txt

```
error: please provide at least one environment variable name
```

Errors should go to `stderr`, and the command should set a non-zero exit code.

Do not print the actual values of environment variables. Some of them may be secrets.

The goal of this project is to practice reading command arguments, using `process.env`, printing helpful errors, and avoiding accidental secret leaks in terminal output.

You will need these Node.js APIs:

* `process.argv` to read the required environment variable names from the terminal.
* `process.env` to check which environment variables are set for the current process.
* `process.exitCode` to mark the command as failed without forcing an early crash.

Solution

Solution:

js

```
const requiredNames = process.argv.slice(2);function printError(message) {  console.error(`error: ${message}`);  process.exitCode = 1;}function getMissingNames(names) {  return names.filter((name) => !process.env[name]);}function printSuccess(names) {  for (const name of names) {    console.log(`Set: ${name}`);  }  console.log('All required environment variables are set.');}function main() {  if (requiredNames.length === 0) {    printError('please provide at least one environment variable name');    return;  }  const missingNames = getMissingNames(requiredNames);  if (missingNames.length > 0) {    printError(`missing environment variables: ${missingNames.join(', ')}`);    return;  }  printSuccess(requiredNames);}main();
```

