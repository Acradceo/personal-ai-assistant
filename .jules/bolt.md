## 2024-05-15 - [Backend Pagination]
**Learning:** Returning large lists by casting `dict.values()` to a list `list(dict.values())` can cause large O(N) memory spikes as the dataset grows.
**Action:** Implementing server-side pagination with `limit` and `offset` using `itertools.islice` creates memory-efficient lazy evaluation for slices. Default `limit` to `None` so legacy clients still work correctly, but with improved potential to limit requests.
