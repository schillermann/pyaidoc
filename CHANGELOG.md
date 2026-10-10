# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.4.1] - 2026-10-10

### Added
- Added `AGENTS.md` specifying agent conventions, pure OOP guidelines, and pre-commit workflow.

### Changed
- Configured local virtual environment `.venv` with `pytest` and `pyright` in `pyrightconfig.json`.

## [0.4.0] - 2026-10-10

### Changed
- Radical Pure OOP refactoring adhering strictly to Yegor Bugayenko's *Elegant Objects* philosophy:
  - 100% Code-free constructors across all classes (assignments only).
  - Total eradication of `isinstance` checks using candidate polymorphism (`AdaptedToolCandidates`, `TypeNameCandidates`, `DefaultValueCandidates`).
  - Replaced stateless fake objects with stateful Null Objects (`EmptyDocstring`, `NoDefault`, `EmptyTableContent`, `EmptySectionCards`).
  - Replaced module-level variables with autonomous domain objects (introduced `DefaultCss`).
  - Introduced `Ternary` conditional object in `pyaidoc.ternary` eliminating imperative `if/return` in domain objects.
  - Extracted `SchemaFunction` and candidate-based `SchemaParameterType` to cleanly encapsulate OpenAI/JSON tool schemas.
  - Refactored badges into polymorphic objects (`RequiredBadge`, `OptionalBadge`, `Badge`).
  - Implemented Dependency Inversion on UI elements (`Card`, `Document`, `Page`, `Table`).
  - CLI architecture refactored to pure objects: `ExitCode`, `Output` (`Stdout`, `MemoryOutput`), `FileDestination` (`LocalFile`, `MemoryFile`), and immutable `Arguments`.
  - Documentation in `README.md` completely translated to English.

## [0.3.0] - 2026-10-10

### Added
- Standalone CLI executable `pyaidoc` with commands `tools`, `docs`, and `help`.
- Terminal ANSI cards presentation engine in `pyaidoc.terminal` for rich CLI display with parameter types, defaults, and requirement status.
- Entry-point integration for `pyresponse` CLI (`ai_tools` and `ai_docs` commands).
- Pure OOP dynamic target resolver (`TargetTools`) discovering tool collections from module attributes or current working directory.
- CLI usage guide and optional `pyresponse` integration documentation in `README.md`.

## [0.2.0] - 2026-10-09

### Added
- Native support for OpenAI/JSON AI function calling schemas via `SchemaTool`, `SchemaParameter`, and `SchemaParameters`.
- Automatic schema ingestion in `Tools` collection without external dependencies or data conversion.
- Quickstart guide and file export instructions in `README.md`.

## [0.1.0] - 2026-10-09

### Added
- Zero-annotation, living HTML documentation engine for Python AI function calls and agent tools.
- Pure OOP domain objects adhering strictly to Yegor Bugayenko's *Elegant Objects* (`Tool`, `Tools`, `Parameter`, `Parameters`, `TypeName`, `Docstring`, `EmptyDocstring`, `Default`, `NoDefault`, `PresentDefault`).
- Composable HTML presentation components (`Page`, `Section`, `Card`, `Table`, `Row`, `Badge`, `Document`, `Style`).
- Responsive modern dark/light mode stylesheet with minimum 14px font size.
- Comprehensive test suite covering domain introspection, collections, and HTML generation.

