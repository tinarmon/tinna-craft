# Testing Patterns Reference (Vitest, Playwright & Pytest)

## 1. TypeScript / React Unit & Integration (Vitest + Testing Library)

```typescript
import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { TaskItem } from './TaskItem';

describe('TaskItem', () => {
  it('toggles completion when checkbox is clicked', () => {
    const onToggle = vi.fn();
    render(
      <TaskItem
        task={{ id: '1', title: 'Write tests', done: false }}
        onToggle={onToggle}
        onDelete={vi.fn()}
      />
    );

    fireEvent.click(screen.getByRole('checkbox'));
    expect(onToggle).toHaveBeenCalledWith('1');
  });
});
```

## 2. End-to-End Browser Testing (Playwright)

```typescript
import { test, expect } from '@playwright/test';

test('user can create and complete a task', async ({ page }) => {
  await page.goto('/tasks');
  await page.getByLabel('New task title').fill('Deploy to production');
  await page.getByRole('button', { name: 'Add Task' }).click();

  const item = page.getByRole('listitem').filter({ hasText: 'Deploy to production' });
  await expect(item).toBeVisible();
});
```

## 3. Python Testing (`pytest`)

```python
import pytest
from pathlib import Path
from my_package.processor import clean_records

def test_clean_records_drops_null_keys():
    raw = [{"id": "1", "val": 10}, {"id": None, "val": 20}]
    result, dropped = clean_records(raw)
    assert len(result) == 1
    assert result[0]["id"] == "1"
    assert dropped == 1

def test_clean_records_raises_on_invalid_schema():
    with pytest.raises(ValueError, match="Missing required field"):
        clean_records([{"wrong_key": 123}])
```
