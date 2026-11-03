JSON Response Normalizer
beginner

JSON Response Normalizer
========================

Normalize API-shaped JSON data into article summaries.

Start building, submit solution and get feedback from the community.

Start Working
JSON Response Normalizer
========================

An API response often contains more data than your program needs. Normalize the response into a smaller list of published article summaries.

Write these functions:

* `getPublishedArticles(response)` should return only articles where `status` is `"published"`.
* `toArticleSummary(article)` should return an object with `id`, `title`, `authorName`, and `views`.
* `normalizeArticles(response)` should return summaries for published articles only.

Sample checks:

js

```
const apiResponse = {  data: [    {      id: 'a1',      title: 'Learning JavaScript',      status: 'published',      author: { name: 'Ava Stone' },      stats: { views: 1200 },    },    {      id: 'a2',      title: 'Draft Notes',      status: 'draft',      author: { name: 'Noah Kim' },      stats: { views: 50 },    },    {      id: 'a3',      title: 'Async Basics',      status: 'published',      author: { name: 'Mina Patel' },      stats: { views: 900 },    },  ],  meta: {    total: 3,  },};console.log(normalizeArticles(apiResponse));console.log(getPublishedArticles(apiResponse).length);console.log(toArticleSummary(apiResponse.data[0]));
```

Expected output:

txt

```
[  { id: "a1", title: "Learning JavaScript", authorName: "Ava Stone", views: 1200 },  { id: "a3", title: "Async Basics", authorName: "Mina Patel", views: 900 }]2{ id: "a1", title: "Learning JavaScript", authorName: "Ava Stone", views: 1200 }
```

Do not change the original `apiResponse` object.

Solution

Solution:

js

```
function getPublishedArticles(response) {  return response.data.filter((article) => article.status === 'published');}function toArticleSummary(article) {  return {    id: article.id,    title: article.title,    authorName: article.author.name,    views: article.stats.views,  };}function normalizeArticles(response) {  const publishedArticles = getPublishedArticles(response);  return publishedArticles.map((article) => toArticleSummary(article));}const apiResponse = {  data: [    {      id: 'a1',      title: 'Learning JavaScript',      status: 'published',      author: { name: 'Ava Stone' },      stats: { views: 1200 },    },    {      id: 'a2',      title: 'Draft Notes',      status: 'draft',      author: { name: 'Noah Kim' },      stats: { views: 50 },    },    {      id: 'a3',      title: 'Async Basics',      status: 'published',      author: { name: 'Mina Patel' },      stats: { views: 900 },    },  ],  meta: {    total: 3,  },};console.log(normalizeArticles(apiResponse));console.log(getPublishedArticles(apiResponse).length);console.log(toArticleSummary(apiResponse.data[0]));
```

