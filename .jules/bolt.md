## 2024-05-23 - Prevent unbounded memory growth with collections.deque
**Learning:** Using a standard list `[]` to store unbounded chat history or event streams leads to memory leaks and OOM errors as the data grows indefinitely.
**Action:** Use `collections.deque(maxlen=N)` for memory-bound, fast, rolling event logs/chat history instead of plain Python lists, ensuring O(1) space constraints.
