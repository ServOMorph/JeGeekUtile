# Session JeGeekUtile 2026-04-27
## Technical Insights

### 1. Flask & Markdown Integration
Issue: Hardcoding HTML in JavaScript strings for modal content is hard to maintain.
Solution: Used the `markdown` library in a Flask context processor to inject rendered HTML from `.md` files into templates via hidden source divs.
Code Pattern:
```python
@app.context_processor
def inject_content():
    import markdown
    # read .md, render to html, return in dict
```

### 2. UI/UX: Modal Customization
Insight: Standard scrollbars break the neon/dark aesthetic.
Solution: Applied custom CSS scrollbar styling to the modal content container:
```css
.modal-content-html::-webkit-scrollbar { width: 4px; }
.modal-content-html::-webkit-scrollbar-thumb { background: var(--neon); box-shadow: 0 0 10px var(--neon); }
```

### 3. JavaScript Bug: Nested Functions
Error: Accidental nesting of functions during `replace_file_content` edits.
Prevention: Always verify function closing braces `}` when adding new logic to existing scripts in templates.

### 4. Layout: Hero Section Alignment
Problem: Using `position: absolute` for user info made it difficult to stack elements vertically when the user requested the name be "above" the title.
Resolution: Reverted to `display: flex; flex-direction: column` for the hero content while keeping a `min-height` to maintain the visual weight.
