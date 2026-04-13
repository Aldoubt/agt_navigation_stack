# Development Standards (开发规范)

## Code Style (代码风格)

### Python
- Follow PEP 8
- Use 4 spaces for indentation
- Maximum line length: 100 characters
- Use type hints where possible

Example:
```python
def process_data(input_data: dict) -> bool:
    """Process input data."""
    # Implementation
    return True
```

### C++
- Use Google C++ Style Guide
- 2 spaces for indentation
- Use const references where applicable

## File Naming Convention (文件命名规范)

- Python files: `snake_case.py`
- C++ files: `snake_case.cpp`/`snake_case.hpp`
- Messages: `CamelCase.msg`
- Services: `CamelCase.srv`
- Launch files: `snake_case.launch.xml` or `.py`

## Package Structure (包结构)

```
package_name/
├── CMakeLists.txt
├── package.xml
├── src/
│   ├── package_name/
│   │   ├── __init__.py
│   │   ├── node.py
│   │   └── utils.py
│   └── cpp_sources/
├── launch/
├── config/
├── test/
└── README.md
```

## Git Workflow (Git工作流)

1. Create feature branch: `git checkout -b feature/feature-name`
2. Make changes and commit: `git commit -m "feat: description"`
3. Push and create pull request
4. Code review and merge

## Testing (测试)

- Write unit tests for new features
- Run tests before submitting PR
- Use pytest for Python tests

```bash
pytest test/
```

## Documentation (文档)

- Document public APIs
- Add docstrings to functions
- Keep README.md updated
- Update CHANGELOG.md for releases

## Commit Message Format (提交信息格式)

```
<type>(<scope>): <subject>

<body>

<footer>
```

Types: feat, fix, docs, style, refactor, test, chore

Example:
```
feat(odometry): add UKF filter support

Implement UKF-based odometry filtering for improved accuracy.
Tested with benchmark dataset.

Closes #123
```
