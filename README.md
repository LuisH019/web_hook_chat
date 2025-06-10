# Secure Chat Application - Webhook with RSA and HMAC Encryption

## Overview

This project is a secure peer-to-peer chat application that implements end-to-end encryption using RSA for message confidentiality and HMAC for message integrity verification. The application features both a web-based graphical interface and a console interface for setup.

Key security features:
- RSA asymmetric encryption for secure message transmission
- HMAC-SHA256 for message authentication
- Shared secret for additional security layer
- Automatic key exchange between peers

## Features

- **Secure Communication**: All messages are encrypted before transmission
- **Dual Interface**: Web-based GUI and console setup interface
- **Network Flexibility**: Works on the same machine or across a local network
- **Message Logging**: Complete history of all sent and received messages
- **Automatic Key Management**: Handles key exchange and rotation automatically

## System Requirements

- Python 3.7 or higher
- pip for package management

## Installation

1. Clone the repository:
   ```bash
   git clone [repository-url]
   cd secure-chat-app
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Starting the Chat Application

1. **Single Machine Mode** (two chat instances on the same machine):
   ```bash
   python chat_init.py
   ```
   Follow the console menu to configure both chat endpoints.

2. **Network Mode** (chat between two machines on the same network):
   - Run the setup on both machines with appropriate IP addresses
   - Ensure both machines can reach each other on the specified ports

### Configuration Options

When starting the application, you'll need to provide:
- A shared secret (must match between peers)
- Your chat identity name
- Port number for your instance
- Peer's chat identity name
- Peer's port number
- Peer's IP address (for network mode)

## Security Implementation Details

1. **RSA Encryption**:
   - Each peer generates their own RSA key pair
   - Public keys are exchanged automatically
   - Messages are encrypted with the peer's public key

2. **HMAC Authentication**:
   - Each message includes an HMAC signature
   - Uses SHA-256 for hash generation
   - Verifies message integrity and authenticity

3. **Key Rotation**:
   - HMAC keys are periodically regenerated
   - Automatic re-exchange occurs every 50 messages

## File Structure

```
secure-chat-app/
├── models/                  # Application models
│   ├── chat_app_model.py    # Main chat logic
│   └── setup_chats.py       # Chat initialization
├── static/                  # Static web files
│   ├── css/                 # Stylesheets
│   └── js/                  # JavaScript files
├── templates/               # HTML templates
│   └── app.html             # Chat interface
├── utils/                   # Utility modules
│   ├── cryptography/        # Encryption functions
│   └── network.py           # Network utilities
├── views/                   # Application views
│   └── menu.py              # Console interface
├── chat_init.py             # Application entry point
└── requirements.txt          # Python dependencies
```

## Troubleshooting

- **Connection Issues**: Verify both peers are using the correct IP addresses and ports
- **Message Delivery Failures**: Check that the shared secret matches on both peers
- **Key Exchange Problems**: Ensure network connectivity between peers during initial setup

## Future Enhancements

- Message persistence
- Group chat functionality
- File transfer capability
- Improved key rotation policies
