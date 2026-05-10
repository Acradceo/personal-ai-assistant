
## 2024-05-10 - [Stateful Caching Side Effects in Pytest]
**Learning:** Adding `@lru_cache` to functions wrapping stateful or external API calls (like LangChain's LLM `.predict()`) creates test pollution if not cleared between tests. A mock might appear to not be called or be called too many times depending on execution order.
**Action:** When adding caching to any stateful function, always explicitly add `.cache_clear()` to the global `setup_and_teardown` autouse pytest fixture to ensure full test isolation.
