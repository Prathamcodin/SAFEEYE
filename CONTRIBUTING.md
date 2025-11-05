# Contributing to SafeEye

Thank you for your interest in contributing to SafeEye! This document provides guidelines and instructions for contributing.

## 🚀 Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/yourusername/safeye.git
   cd safeye
   ```
3. **Add upstream remote**:
   ```bash
   git remote add upstream https://github.com/originalowner/safeye.git
   ```

## 📝 Development Setup

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Frontend

```bash
cd frontend
npm install
```

## 🔀 Workflow

1. **Create a branch** for your feature/fix:
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/bug-description
   ```

2. **Make your changes** following our coding standards

3. **Test your changes**:
   - Backend: Ensure all endpoints work correctly
   - Frontend: Test in browser, check for console errors
   - Run linters if available

4. **Commit your changes**:
   ```bash
   git add .
   git commit -m "feat: Add new feature description"
   ```
   
   Use conventional commit messages:
   - `feat:` for new features
   - `fix:` for bug fixes
   - `docs:` for documentation changes
   - `style:` for formatting changes
   - `refactor:` for code refactoring
   - `test:` for adding tests
   - `chore:` for maintenance tasks

5. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request** on GitHub

## 📋 Pull Request Guidelines

- **Title**: Clear and descriptive
- **Description**: Explain what changes you made and why
- **Issue**: Link to related issues if applicable
- **Testing**: Describe how you tested your changes
- **Screenshots**: Include screenshots for UI changes

## 🎨 Code Style

### Python (Backend)

- Follow PEP 8 style guide
- Use type hints where possible
- Write docstrings for functions and classes
- Maximum line length: 100 characters

### TypeScript/React (Frontend)

- Use TypeScript for type safety
- Follow React best practices
- Use functional components and hooks
- Format with Prettier (if configured)

## 🧪 Testing

- Test your changes thoroughly
- Test edge cases
- Ensure backward compatibility
- Update tests if needed

## 📚 Documentation

- Update README.md if needed
- Add comments to complex code
- Update API documentation if endpoints change
- Update CHANGELOG.md for significant changes

## 🐛 Reporting Bugs

Create an issue with:
- Clear title and description
- Steps to reproduce
- Expected vs actual behavior
- Environment details (OS, Python/Node versions)
- Screenshots if applicable

## 💡 Feature Requests

Open an issue with:
- Clear description of the feature
- Use case and benefits
- Possible implementation approach

## 📞 Questions?

- Open a discussion on GitHub
- Check existing issues and discussions
- Review the documentation

## 🎯 Areas for Contribution

- **AI Models**: Improve tracking accuracy, add new models
- **Performance**: Optimize video processing
- **UI/UX**: Improve user interface and experience
- **Documentation**: Improve docs and add examples
- **Testing**: Add unit and integration tests
- **Localization**: Add translations
- **Security**: Security improvements and audits

## 📜 Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Focus on constructive feedback
- Respect differing viewpoints

Thank you for contributing to SafeEye! 🎉

