# AGENTS.md

Guidelines, architectural rules, and conventions for AI agents operating in the `pyaidoc` codebase.

---

## 1. Git & Commit Guidelines

- **Staged Changes Focus**: Commit messages must always accurately describe the changes currently staged in `git diff --cached` / `git status`.
- **Conventional Commits v1.0.0 Compliance**:
  - Format: `<type>[optional scope]: <description>`
  - Language: Commit messages must **always** be written in **English**.
  - Types:
    - `feat`: New feature or capability
    - `fix`: Bug fix
    - `docs`: Documentation changes
    - `style`: Formatting, missing semicolons, etc. (no functional code changes)
    - `refactor`: Refactoring code without adding features or fixing bugs
    - `perf`: Performance improvements
    - `test`: Adding or updating tests
    - `build`: Build system or dependency updates
    - `ci`: CI configuration and script updates
    - `chore`: Maintenance tasks
  - Breaking Changes: Use `!` before `:` or `BREAKING CHANGE: <description>` in the footer.

- **`create git message` Workflow & Pre-Commit Protocol**:
  - When the user prompts `create git message` (or asks to generate/prepare a commit message):
    1. **Type Checking (`pyright`)**: Run `pyright` strictly from the project's virtual environment (`.venv/bin/pyright <modified_python_files>`) on the modified/staged Python files only. Never use a global or external instance.
    2. **Fix Type Errors**: Resolve all errors identified by `pyright` immediately.
    3. **Run Tests**: Execute `pytest` (`.venv/bin/pytest`) to guarantee all tests pass.
    4. **Bump Version**: Increment the version number according to Semantic Versioning (`MAJOR.MINOR.PATCH`) across:
       - `pyproject.toml` (`version = "..."`)
       - `src/pyaidoc/__init__.py` (`__version__ = "..."`)
       - `tests/test_tools.py` (`assert pyaidoc.__version__ == "..."`)
       - `CHANGELOG.md` (add `## [x.y.z] - YYYY-MM-DD` section following Keep a Changelog)
    5. **Generate Commit Message**: Propose or generate the Conventional Commit message reflecting the staged changes.

---

## 2. Core Architecture & Philosophy (Elegant Objects / Pure OOP)

`pyaidoc` follows strict **Elegant Objects** (Yegor Bugayenko) and pure Object-Oriented Programming principles:

1. **100% Code-Free Constructors**:
   - `__init__` methods must strictly only perform attribute assignments (`self._param = param`).
   - No validation, conditionals, type conversions, side effects, or business logic inside `__init__`.

2. **No `isinstance` Checks (Polymorphism via Candidates)**:
   - Never use `isinstance(...)` checks or procedural type branching.
   - Decompose behavior into polymorphic candidate classes (e.g. `AdaptedToolCandidates`, `TypeNameCandidates`, `DefaultValueCandidates`).

3. **Never Return `None` (Null Object Pattern & Fail Fast)**:
   - Never return `None` or use `None` checks for missing values.
   - Use explicit Null Objects (`EmptyDocstring`, `NoDefault`, `EmptyTableContent`, `EmptySectionCards`).

4. **Composition over Inheritance & Autonomous Domain Objects**:
   - Build documents and presentations by composing cohesive domain objects and decorators (`Card`, `Document`, `Page`, `Table`, `Badge`, `Terminal`).
   - Encapsulate styles and templates as domain objects (e.g. `DefaultCss`) instead of procedural global variables.

5. **Eliminate Imperative Branching in Domain Logic**:
   - Favor declarative flow and objects like `Ternary` (`pyaidoc.ternary`) over procedural `if/return` branches.

6. **No Getters / Setters / Anemic DTOs**:
   - Encapsulate data and behavior together within cohesive, living domain objects.
   - Query methods returning values should be nouns/adjectives, not JavaBean-style `get_...`.

7. **No Static Methods & No Global Singletons**:
   - Avoid global mutable state, singleton containers, and `@staticmethod` utility dumps.
   - Pure instance-based composition roots.

---

## 3. Technology Stack & Standards

- **Language**: Python >= 3.10
- **Virtual Environment**: `.venv` with `pytest` and `pyright`
- **Testing**: `pytest` (`testpaths = ["tests"]`, `pythonpath = ["src"]`)
- **Type Checking**: `pyright` configured via `pyrightconfig.json`
- **Changelog**: English, Keep a Changelog standard in `CHANGELOG.md`
