GitHub Profile Details
beginner

GitHub Profile Details
======================

Fetch and print public details for a GitHub user.

Start building, submit solution and get feedback from the community.

Start Working
GitHub Profile Details
======================

You are required to build a CLI tool using Node.js that prints public profile details for a GitHub user.

The tool should accept a GitHub username from the terminal. If the user does not pass a username, it should print a friendly error.

Here are some example commands you can run to test your CLI:

bash

```
node github-profile.js octocatnode github-profile.js missing-user-name-examplenode github-profile.js
```

On successful execution, the output should look like this:

txt

```
Name: The OctocatUsername: octocatProfile: https://github.com/octocatPublic repos: 8Followers: 20000
```

The exact follower count can be different when you run the command.

If the GitHub user does not exist, print a friendly error:

txt

```
error: GitHub user not found: missing-user-name-example
```

If the user does not pass a username, print this error:

txt

```
error: please provide a GitHub username
```

Errors should go to `stderr`, and the command should set a non-zero exit code.

The goal of this project is to practice reading command arguments, calling an API from Node.js, handling failed responses, and printing useful data in the terminal.

You will need these Node.js APIs:

* `process.argv` to read the username from the terminal.
* `fetch` to call the GitHub API.
* `encodeURIComponent()` to safely place the username in the URL.

Solution

Solution:

js

```
const username = process.argv[2];function printError(message) {  console.error(`error: ${message}`);  process.exitCode = 1;}function printProfile(profile) {  console.log(`Name: ${profile.name || 'not set'}`);  console.log(`Username: ${profile.login}`);  console.log(`Profile: ${profile.html_url}`);  console.log(`Public repos: ${profile.public_repos}`);  console.log(`Followers: ${profile.followers}`);}async function fetchGitHubProfile(username) {  const url = `https://api.github.com/users/${encodeURIComponent(username)}`;  let response;  try {    response = await fetch(url, {      headers: {        Accept: 'application/vnd.github+json',        'User-Agent': 'github-profile-cli',      },    });  } catch {    printError('could not reach GitHub');    return null;  }  const data = await response.json().catch(() => null);  if (response.status === 404) {    printError(`GitHub user not found: ${username}`);    return null;  }  if (!response.ok) {    printError(data?.message || `GitHub request failed with status ${response.status}`);    return null;  }  return data;}async function main() {  if (!username) {    printError('please provide a GitHub username');    return;  }  const profile = await fetchGitHubProfile(username);  if (!profile) {    return;  }  printProfile(profile);}await main();
```

