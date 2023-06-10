# Contributing to Shoshin

This document provides guidelines for contributing to project. Before you begin, please follow the
instructions below:

1. Prepare your [development environment](https://github.com/palazzem/shoshin#development).
2. Ensure that you have installed the `pre-commit` hooks.
3. Run `tox` to execute the full test suite.

By following these steps, you can ensure that your contributions are of the highest quality and are properly tested
before they are merged into the project.

## Pull Requests

### PR Title

We follow the [conventional commit convention](https://www.conventionalcommits.org/en/v1.0.0/) for our PR titles.
The title should adhere to the structure below:

```
<type>[optional scope]: <description>
```

The common types are:
- `feat` (enhancements)
- `fix` (bug fixes)
- `docs` (documentation changes)
- `perf` (performance improvements)
- `refactor` (major code refactorings)
- `test` (changes to the tests)
- `tools` (changes to package spec or tools in general)
- `ci` (changes to our CI)
- `deps` (changes to dependencies)

If your change breaks backwards compatibility, indicate so by adding `!` after the type.

Examples:
- `feat[cli]: add Transcribe command`
- `fix: ensure hashing function returns correct value for random input`
- `feat!: remove deprecated API` (a change that breaks backwards compatibility)

### PR Description

Please use the [existing pull request template](https://github.com/palazzem/shoshin/blob/main/.github/pull_request_template.md)
to document and describe your changes.
