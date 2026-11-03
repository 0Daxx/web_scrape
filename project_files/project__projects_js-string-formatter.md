String Formatter
beginner

String Formatter
================

Normalize names with string cleanup and formatting functions.

Start building, submit solution and get feedback from the community.

Start Working
String Formatter
================

A signup form is receiving names with inconsistent spacing and casing. Normalize the names before showing them back to the user.

Write these functions:

* `cleanText(text)` should remove spaces from the start and end of a string.
* `capitalize(text)` should uppercase the first character and lowercase the rest.
* `formatDisplayName(firstName, lastName)` should clean and capitalize both names, then return the full display name.

Sample checks:

js

```
console.log(formatDisplayName('  ava', 'STONE  '));console.log(formatDisplayName('nOAh', '  kim'));console.log(formatDisplayName('  mINA  ', 'pATEL'));
```

Expected output:

txt

```
Ava StoneNoah KimMina Patel
```

`formatDisplayName` should reuse the smaller helpers instead of repeating all the string cleanup work.

Solution

Solution:

js

```
function cleanText(text) {  return text.trim();}function capitalize(text) {  const cleaned = cleanText(text).toLowerCase();  if (cleaned.length === 0) {    return '';  }  return cleaned[0].toUpperCase() + cleaned.slice(1);}function formatDisplayName(firstName, lastName) {  const cleanFirstName = capitalize(firstName);  const cleanLastName = capitalize(lastName);  return `${cleanFirstName} ${cleanLastName}`;}console.log(formatDisplayName('  ava', 'STONE  '));console.log(formatDisplayName('nOAh', '  kim'));console.log(formatDisplayName('  mINA  ', 'pATEL'));
```

