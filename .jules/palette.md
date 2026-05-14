## 2024-05-14 - Textarea Focus Outlines

**Learning:** When using standard HTML `<textarea>` elements without global CSS resets, adding custom `:focus-visible` outlines helps ensure keyboard accessibility visibility, but the outline might interact poorly with default sizing unless `box-sizing: border-box` is explicitly applied.
**Action:** Always verify focus rings and box-sizing properties on raw HTML form inputs when enhancing accessibility in vanilla setups.
