## 2024-05-12 - Added server-side pagination for tasks and notes
**Learning:** Returning all items dynamically from endpoints can lead to memory or network bottlenecks as the dataset grows. Caching dynamic generative LLMs violates chat usability. Server-side pagination solves large data transfer while retaining accuracy.
**Action:** Always add pagination options to endpoints returning potentially large lists.
