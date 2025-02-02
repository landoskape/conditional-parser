# Changelog

All notable changes to this project will be documented in this file.
 
The format is based on [Keep a Changelog](http://keepachangelog.com/)
and this project adheres to [Semantic Versioning](http://semver.org/).

## [future development] - Unreleased
As of now, this doesn't work with subparsers. I'm working on it. If you want this
functionality and it isn't there yet, let me know. But - note that you can use 
conditional arguments to completely replace subparsers...

## [0.2.1] - Unreleased

### Added
Tests for more use cases. 
Explanation of how to handle subparser-like functionality. 


## [0.2.0] - 2025-01-11

### Added
- New `_prepare_help` method to show all conditional arguments in help output
- Added conditional argument availability messages in help text
- Added `_callable_representation` method to generate human-readable condition descriptions
- Added comprehensive internal method documentation in API docs
- Added more thorough help text testing

### Changed
- Help system now shows all possible conditional arguments regardless of current state
- Help messages now include information about when conditional arguments become available
- Improved error handling in `add_conditional` method
- Updated documentation to reflect new help system behavior
- Code formatting improvements for better readability
- Added black code formatter to project

### Removed
- Removed behavior where help messages would only show currently available arguments