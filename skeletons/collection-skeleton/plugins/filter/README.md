# Filter Plugins

Custom Jinja2 filters for use in templates and tasks.

## When to write a filter plugin

When you find yourself writing the same complex Jinja2 expression in multiple templates,
that expression belongs in a filter plugin.

Signals:
- You've copy-pasted the same `| map | select | list` chain three times
- You need a transformation that doesn't exist in `ansible.builtin` or `community.general`
- Your template has Jinja2 logic that a human needs to read and understand

## When NOT to write a filter plugin

- When `community.general` already has it (check first: `ansible-doc -t filter community.general.*`)
- When a simple variable transform would do
- When you'd only use it once

## Structure

```python
# plugins/filter/your_filters.py

class FilterModule:
    def filters(self):
        return {
            'your_filter_name': self.your_filter_name,
        }

    def your_filter_name(self, value, arg=None):
        """
        Transform value in some useful way.
        
        Usage in template: {{ some_list | your_filter_name }}
        Usage with arg:    {{ some_list | your_filter_name('arg') }}
        """
        # implementation
        return transformed_value
```

## Testing filters

Test filter plugins with molecule or directly with Python:

```bash
python3 -c "
from plugins.filter.your_filters import FilterModule
f = FilterModule()
result = f.filters()['your_filter_name'](['a', 'b', 'c'])
print(result)
"
```

## 🐇 Rabbit holes

- `/explore filter-plugins` — writing, testing, and distributing filters
- `/explore lookup-plugins` — when you need to fetch data at task time
- `/explore callback-plugins` — customizing ansible output
