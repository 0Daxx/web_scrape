User Profile Formatter
beginner

User Profile Formatter
======================

Format nested user data into a smaller profile summary.

Start building, submit solution and get feedback from the community.

Start Working
User Profile Formatter
======================

Format a nested user object into values that are easier to show in an interface or return from an API. The final summary should collect the smaller pieces.

Write these functions:

* `getDisplayName(user)` should return the first and last name as one string.
* `getLocation(user)` should return `"City, Country"`.
* `getContactSummary(user)` should return an object with `email` and `phone`.
* `isAccountActive(user)` should return `true` when `account.status` is `"active"`.
* `createProfileSummary(user)` should return `displayName`, `location`, `contact`, `active`, and `plan`.

Sample checks:

js

```
const user = {  id: 42,  firstName: 'Ava',  lastName: 'Stone',  email: 'ava@example.com',  phone: null,  address: {    city: 'London',    country: 'UK',  },  account: {    status: 'active',    plan: 'pro',  },};console.log(createProfileSummary(user));console.log(getDisplayName(user));console.log(isAccountActive(user));console.log(getContactSummary(user));
```

Expected output:

txt

```
{ displayName: "Ava Stone", location: "London, UK", contact: { email: "ava@example.com", phone: null }, active: true, plan: "pro" }Ava Stonetrue{ email: "ava@example.com", phone: null }
```

Keep `phone` as `null` when the user has no phone number.

Solution

Solution:

js

```
function getDisplayName(user) {  return `${user.firstName} ${user.lastName}`;}function getLocation(user) {  return `${user.address.city}, ${user.address.country}`;}function getContactSummary(user) {  return {    email: user.email,    phone: user.phone,  };}function isAccountActive(user) {  return user.account.status === 'active';}function createProfileSummary(user) {  return {    displayName: getDisplayName(user),    location: getLocation(user),    contact: getContactSummary(user),    active: isAccountActive(user),    plan: user.account.plan,  };}const user = {  id: 42,  firstName: 'Ava',  lastName: 'Stone',  email: 'ava@example.com',  phone: null,  address: {    city: 'London',    country: 'UK',  },  account: {    status: 'active',    plan: 'pro',  },};console.log(createProfileSummary(user));console.log(getDisplayName(user));console.log(isAccountActive(user));console.log(getContactSummary(user));
```

