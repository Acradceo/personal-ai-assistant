## 2024-05-16 - LLM Prediction Caching
**Learning:** Caching generative AI chat models using `functools.lru_cache` degrades usability as chatbots are expected to be non-deterministic, however caching repetitive queries can reduce expensive, redundant computations in performance-sensitive contexts when appropriate.
**Action:** When caching stateful or external calls (like LLM predictions) using `functools.lru_cache`, always call `.cache_clear()` in a pytest autouse=True setup/teardown fixture to ensure clean state and avoid test contamination.
