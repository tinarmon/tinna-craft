# WCAG 2.1 AA Accessibility Checklist

## 1. Semantic HTML & Landmarks
- Use native interactive elements (`<button>`, `<a href="...">`, `<input>`, `<select>`, `<dialog>`) instead of `<div onClick={...}>`.
- Provide page landmarks: `<header>`, `<nav>`, `<main>`, `<aside>`, `<footer>`.
- Maintain strict heading hierarchy (`<h1>` once per page, followed by `<h2>`, `<h3>` without skipping levels).

## 2. Keyboard Navigation & Focus
- Every interactive control must be reachable via `Tab` and `Shift+Tab` in a logical visual order.
- Never remove focus outlines (`outline: none`) without replacing them with a high-contrast `:focus-visible` ring.
- Modal dialogs must trap focus while open, focus the first interactive element (or close button) on open, restore focus to the trigger element on close, and close on `Escape`.

## 3. ARIA & Labeling
- Every `<input>`, `<textarea>`, and `<select>` must have an associated `<label htmlFor="...">` or `aria-label` / `aria-labelledby`.
- Icon-only buttons (`<button><TrashIcon /></button>`) must have `aria-label="Delete item"`, and decorative SVG icons should have `aria-hidden="true"`.
- Dynamic status updates (toasts, empty states, form errors, loading skeletons) should use `role="status"`, `role="alert"`, or `aria-live="polite"`.
- Form inputs with validation errors must set `aria-invalid="true"` and link to the error text via `aria-describedby`.

## 4. Visual Contrast & Motion
- Normal text (< 18pt, or < 14pt bold): minimum **4.5:1** contrast ratio against background.
- Large text (>= 18pt, or >= 14pt bold) & UI component borders/icons: minimum **3:1** contrast ratio.
- Never use color alone to convey status (pair red/green indicators with icons or text labels).
- Respect `prefers-reduced-motion: reduce` for animations and transitions.
