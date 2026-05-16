## 2024-05-16 - Textarea without labels
**Learning:** The chat input `textarea` was lacking an explicit label, making it difficult for screen readers to identify its purpose. Since adding a visible label might affect the visual design, an `aria-label` provides the necessary context for accessibility without changing the layout.
**Action:** Always add an `aria-label` to form inputs like `textarea` when there is no visual `<label>` tag.
