# Contributing to POS Hide Taxes

Thank you for considering contributing to this module! We welcome contributions from the community.

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue on GitHub with:

1. **Clear title** describing the issue
2. **Steps to reproduce** the problem
3. **Expected behavior** vs **actual behavior**
4. **Odoo version** and module version
5. **Screenshots** if applicable
6. **Error messages** or logs

### Suggesting Enhancements

Enhancement suggestions are welcome! Please include:

1. **Clear description** of the feature
2. **Use case** - why is this needed?
3. **Mockups** or examples if applicable

### Pull Requests

1. **Fork** the repository
2. **Create a branch** from `18.0` (or relevant version)
3. **Make your changes** following the coding standards below
4. **Test thoroughly** - ensure no regressions
5. **Update documentation** if needed
6. **Commit** with clear, descriptive messages
7. **Submit PR** with description of changes

## Coding Standards

### Python
- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use meaningful variable and function names
- Add docstrings to classes and methods
- Keep methods focused and single-purpose

### JavaScript
- Follow [Odoo JavaScript guidelines](https://www.odoo.com/documentation/18.0/contributing/development/coding_guidelines.html#javascript)
- Use ESLint with Odoo configuration
- Add JSDoc comments for functions
- Use modern ES6+ syntax

### XML
- Proper indentation (4 spaces)
- Clear xpath expressions
- Descriptive element IDs

### Commit Messages
```
[TAG] module: Brief description

Longer explanation of the change if needed.
```

**Tags:**
- `[ADD]` - New feature
- `[FIX]` - Bug fix
- `[IMP]` - Improvement
- `[REF]` - Refactoring
- `[REM]` - Removal

## Testing

Before submitting:

1. ✅ Test installation from scratch
2. ✅ Test upgrade from previous version
3. ✅ Test with taxes enabled and disabled
4. ✅ Test in multi-company environment
5. ✅ Test receipt printing
6. ✅ Check for JavaScript console errors
7. ✅ Verify no Python errors in logs

## Questions?

Feel free to open an issue with the question label.

## Code of Conduct

Be respectful, professional, and constructive in all interactions.

Thank you for contributing! 🎉
