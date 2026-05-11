## 2026-05-11 - Stateful Cache Test Contamination
**Learning:** When using `functools.lru_cache` to optimize expensive external calls (like LLM predictions) in this Flask app, the cache persists across pytest runs because the app module remains in memory. This leads to subtle test contamination where mocks aren't called or previous state leaks.
**Action:** Always call `.cache_clear()` on cached functions within a `pytest` autouse=True setup/teardown fixture to ensure test isolation.
