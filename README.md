# 🔐 Lockmind - Intelligent Authentication System

An advanced AI-powered authentication and password management system that uses personal security questions for secure user verification and password recovery.

## 🎯 Project Overview

**Lockmind** is an intelligent authentication system built with Google's Agent Development Kit (ADK) that provides:

- **Smart Account Creation**: Automated user onboarding with comprehensive personal security questions
- **Intelligent Password Recovery**: AI-powered verification through personal questions with fuzzy matching
- **Secure Authentication**: Multi-layered security with encrypted password storage
- **Personal Verification**: Uses personal details (age, favorite color, sports team, etc.) as backup authentication
- **Audit Logging**: Complete authentication history and security event tracking

## 🏗️ Architecture

The system consists of two main AI agents working together:

### 🛡️ AuthManager Agent

- **Account Creation**: Guides new users through complete profile setup
- **User Authentication**: Verifies credentials and manages login sessions
- **Password Recovery**: Conducts intelligent personal verification when passwords are forgotten
- **Security Monitoring**: Tracks failed attempts and implements security protocols

### 🔑 PasswordsManager Agent

- **Password Storage**: Manages encrypted password storage
- **Security Questions**: Handles personal security question management
- **Data Persistence**: Maintains user profiles and authentication history

## 🚀 Key Features

### ✨ Intelligent Account Creation

- Collects username, password, and email
- Asks 10+ personal security questions:
  - Age, favorite color, favorite sports team
  - Birthplace, first pet's name, mother's maiden name
  - Favorite food, elementary school, favorite movie
  - Dream vacation destination, and more
- Validates username uniqueness
- Encrypts passwords before storage

### 🧠 Smart Password Recovery

- **Fuzzy Matching**: Handles typos and variations in answers
- **Confidence Scoring**: Calculates verification confidence (80%+ = allow, 60-79% = additional questions, <60% = deny)
- **Random Question Selection**: Prevents pattern recognition attacks
- **Security Protocols**: Rate limiting and audit trails

### 🔒 Security Features

- Password encryption using SHA-256 hashing
- Account lockout after failed attempts
- Comprehensive audit logging
- Session management with SQLite database
- Protection against brute force attacks

## 📋 Prerequisites

- Python 3.8+
- Google Agent Development Kit (ADK)
- SQLite database
- Required Python packages (see installation)

## 🛠️ Installation & Setup

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd passwordsAgent
   ```

2. **Install dependencies**

   ```bash
   pip install google-adk python-dotenv
   ```

3. **Set up environment variables**
   Create a `.env` file in the project root:

   ```env
   # Add your Google API credentials and other environment variables
   GOOGLE_API_KEY=your_api_key_here
   ```

4. **Initialize the database**
   The SQLite database will be automatically created on first run.

## 🏃‍♂️ Running the Application

1. **Start the application**

   ```bash
   cd passwordsAgent
   python main.py
   ```

2. **Interact with the system**
   - Type your messages to interact with the authentication system
   - For new users: The system will guide you through account creation
   - For existing users: Login with your credentials
   - For password recovery: The system will ask personal verification questions
   - Type `exit` or `quit` to end the session

## 💡 Usage Examples

### Creating a New Account

```
You: I want to create an account
AI: I'll help you create a new account. Let's start with some basic information...
```

### Password Recovery

```
You: I forgot my password for username "john_doe"
AI: I'll help you recover your password through personal verification...
```

## 🗂️ Project Structure

```
passwordsAgent/
├── README.md                          # This file
├── main.py                           # Application entry point
├── my_agent_data.db                  # SQLite database (auto-generated)
├── .env                              # Environment variables
└── Agency/
    ├── __init__.py
    ├── agent.py                      # Main manager agent
    └── workers/
        ├── auth_manager/
        │   ├── __init__.py
        │   └── agent.py              # Authentication agent
        └── passwords_manager/
            ├── __init__.py
            └── agent.py              # Password management agent
```

## 🤝 Contributing

We welcome contributions to improve **Lockmind**! Here's how you can help:

### 📝 Pull Request Process

1. **Fork the repository**

   ```bash
   git fork <repository-url>
   ```

2. **Create a feature branch**

   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**

   - Follow the existing code style
   - Add appropriate comments and documentation
   - Test your changes thoroughly

4. **Commit your changes**

   ```bash
   git commit -m "Add: Description of your feature"
   ```

5. **Push to your fork**

   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request**
   - Provide a clear description of your changes
   - Include any relevant issue numbers
   - Ensure all tests pass

### 🎯 Areas for Contribution

- **Enhanced Security**: Implement stronger encryption methods
- **Additional Verification**: Add biometric or 2FA support
- **UI/UX Improvements**: Create web or mobile interfaces
- **Database Optimization**: Improve data storage and retrieval
- **Testing**: Add comprehensive unit and integration tests
- **Documentation**: Improve code documentation and examples

## 📞 Contact & Support

### 🚀 Request New Features

Have an idea for a new feature or improvement? I'd love to hear from you!

**Contact Methods:**

- **Email**: [wissemhajbi2002@gmail.com](mailto:wissemhajbi2002@gmail.com)
- **GitHub Issues**: Create an issue in this repository
- **Pull Requests**: Submit your feature implementations

### 💬 Feature Request Guidelines

When requesting new features, please include:

- **Clear Description**: What you want to achieve
- **Use Case**: Why this feature would be valuable
- **Implementation Ideas**: Any thoughts on how it could work
- **Priority Level**: How important this is for your use case

### 🐛 Bug Reports

Found a bug? Please report it with:

- Steps to reproduce the issue
- Expected vs actual behavior
- System information (OS, Python version, etc.)
- Error messages or logs

## 📄 License

This project is open source. Please check the LICENSE file for details.

## 🙏 Acknowledgments

- Built with Google's Agent Development Kit (ADK)
- Powered by Gemini 2.0 Flash AI model
- Inspired by modern authentication security practices

---

**Made with ❤️ by [Wissem Hajbi](mailto:wissemhajbi2002@gmail.com)**

_Lockmind - Secure authentication through intelligent personal verification_
