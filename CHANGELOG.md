# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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

