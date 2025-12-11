# GhostTrack 👻🔍

**Open Source Intelligence (OSINT) Tool** for tracking and gathering publicly available information about IP addresses, phone numbers, and usernames across the internet.

<img src="https://github.com/HunxByts/GhostTrack/blob/main/asset/bn.png"/>

[![Version](https://img.shields.io/badge/version-3.0-blue.svg)](https://github.com/HunxByts/GhostTrack)
[![Python](https://img.shields.io/badge/python-3.6+-green.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-red.svg)](LICENSE)

---

## 🎯 What is GhostTrack?

- **Open Source Intelligence (OSINT) Tool** - Python-based information gathering tool for tracking publicly available data
- **IP Address Tracker** - Comprehensive geolocation data with country, city, ISP, timezone, coordinates for IPv4/IPv6
- **Phone Number Intelligence** - Validates and identifies phone numbers with carrier info, location, and type classification
- **Username Footprint Scanner** - Searches for username presence across 23+ social media platforms

---

## ✨ Features

### 🌐 IP Address Tracking
- IPv4 and IPv6 support with regex validation
- Geolocation (country, city, region, continent)
- ISP and organization details
- Timezone information
- Google Maps integration
- Connection type and ASN data

### 📱 Phone Number Tracking
- International format validation (E.164)
- Carrier and operator identification
- Geographic location lookup
- 11 phone number type classifications:
  - 📱 Mobile/Cellular
  - 📞 Fixed Line (Landline)
  - 🆓 Toll-Free
  - 💰 Premium Rate
  - 🌐 VoIP
  - And 6 more types
- Multiple format display (International, E.164, National)
- Timezone information

### 👤 Username Tracking
- Search across 23+ social media platforms
- Platforms include: Facebook, Twitter, Instagram, LinkedIn, GitHub, Pinterest, Tumblr, YouTube, SoundCloud, Snapchat, TikTok, Behance, Medium, Quora, Flickr, Twitch, and more
- Categorized results (Found/Not Found/Errors)
- Statistics and success rate
- Direct profile URLs

### 🛡️ Advanced Features
- Comprehensive error handling with retry mechanisms
- Input validation using regex patterns
- Color-coded terminal output
- Structured results display
- Standalone executable (.exe) support

---

## 📋 Requirements

- **Python 3.6+**
- **Operating Systems:** Windows, Linux, macOS
- **Internet Connection** (required for API calls)

### Dependencies
```
requests
phonenumbers
```

---

## 🚀 Installation

### Windows
```powershell
# Clone the repository
git clone https://github.com/HunxByts/GhostTrack.git
cd GhostTrack

# Install dependencies
pip install -r requirements.txt

# Run the tool
python GhostTR.py
```

### Linux (Debian/Ubuntu)
```bash
# Install prerequisites
sudo apt-get update
sudo apt-get install git python3 python3-pip

# Clone the repository
git clone https://github.com/HunxByts/GhostTrack.git
cd GhostTrack

# Install dependencies
pip3 install -r requirements.txt

# Run the tool
python3 GhostTR.py
```

### Termux (Android)
```bash
# Install prerequisites
pkg update
pkg install git python

# Clone the repository
git clone https://github.com/HunxByts/GhostTrack.git
cd GhostTrack

# Install dependencies
pip install -r requirements.txt

# Run the tool
python GhostTR.py
```

---

## 🎮 Usage

### Main Menu
```
       ________               __      ______                __  
      / ____/ /_  ____  _____/ /_    /_  __/________ ______/ /__
     / / __/ __ \/ __ \/ ___/ __/_____/ / / ___/ __ `/ ___/ //_/
    / /_/ / / / / /_/ (__  ) /_/_____/ / / /  / /_/ / /__/ ,<   
    \____/_/ /_/\____/____/\__/     /_/ /_/   \__,_/\___/_/|_| 

              [ + ]  C O D E   B Y  H U N X  [ + ]

[ 1 ] IP Tracker
[ 2 ] Show Your IP
[ 3 ] Phone Number Tracker
[ 4 ] Username Tracker
[ 0 ] Exit
```

### Example: IP Tracking
```
Enter IP target: 8.8.8.8

✓ Valid IPv4 address detected

============= SHOW INFORMATION IP ADDRESS =============

[BASIC INFORMATION]
IP Target       : 8.8.8.8
IP Type         : IPv4
Connection Type : isp

[GEOGRAPHIC LOCATION]
Country         : United States 🇺🇸 (US)
City            : Mountain View
Region          : California (CA)
...
```

### Example: Phone Number Tracking
```
Enter phone number target Ex [+6281xxxxxxxxx] : +15551234567

[VALIDATION STATUS]
Status          : ✓ Valid
Valid Number    : True

[NUMBER FORMATS]
International    : +1 555 123 4567
E.164 Format     : +15551234567
...

[NUMBER TYPE & DESCRIPTION]
Type            : Mobile/Cellular 📱
Description     : This is a mobile phone number
```

### Example: Username Tracking
```
Enter Username : github

Searching across 23 platforms...

[✓ FOUND PROFILES - 15]
 1. GitHub         → https://www.github.com/github
 2. Twitter        → https://www.twitter.com/github
...

[✗ NOT FOUND - 6]
   Periscope
   Ello
...
```

---

## 🔧 Building Executable

Create a standalone Windows executable that doesn't require Python installation:

### Using Batch Script
```batch
.\build_exe.bat
```

### Using PowerShell Script
```powershell
.\build_exe.ps1
```

### Manual Build
```bash
pip install pyinstaller
pyinstaller --onefile --name GhostTrack --clean GhostTR.py
```

The executable will be created in the `dist/` folder: `dist\GhostTrack.exe`

For detailed build instructions, see [BUILD.md](BUILD.md)

---

## 🧪 Test Cases

### Test Case 1: IP Address Validation
- **Valid IPv4:** `8.8.8.8` (Google DNS)
- **Valid IPv6:** `2001:4860:4860::8888`
- **Invalid:** `256.1.1.1` (should show error)

### Test Case 2: Phone Number Validation
- **With country code:** `+6281234567890` ✓
- **Without country code:** `8123456789` ✗
- **Invalid characters:** `+62-812-abc-defg` ✗

### Test Case 3: Username Search
- **Popular username:** `github` or `google` (should find multiple)
- **Random string:** `xyzabc123notreal456` (should show not found)
- **Invalid format:** `user@domain!` ✗

### Test Case 4: Error Handling
- Empty input test
- Network timeout simulation
- Retry functionality test

---

## 📚 Documentation

### Regex Patterns
- **IPv4:** Validates each octet (0-255) with strict format checking
- **IPv6:** Comprehensive pattern supporting full, compressed, and mixed notation
- **Username:** Allows alphanumeric characters, dots, underscores, and hyphens

### Phone Number Types
The tool identifies 11 different phone number types:
1. Mobile/Cellular - Standard smartphones
2. Fixed Line - Landline/home phones
3. Fixed Line or Mobile - Ambiguous type
4. Toll-Free - Free call numbers (e.g., 1-800)
5. Premium Rate - Paid services (e.g., 1-900)
6. Shared Cost - Split payment
7. VoIP - Internet-based numbers
8. Personal Number - Universal routing
9. Pager - Legacy paging services
10. UAN - Universal Access Numbers
11. Voicemail - Direct voicemail boxes

---

## 🛠️ Improvements Made

### v3.0 Updates
✅ Comprehensive error handling with retry mechanisms  
✅ Input validation using regex patterns  
✅ Removed all redundant sleep() delays for instant performance  
✅ Enhanced phone number validation (strict country code requirement)  
✅ Improved display formatting with color-coded sections  
✅ 11 detailed phone number type classifications  
✅ Executable creation system (PyInstaller)  
✅ Removed duplicate platforms  
✅ Better error messages and user guidance  

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## ⚠️ Disclaimer

This tool is for **educational and research purposes only**. Users are responsible for complying with applicable laws and regulations. The authors are not responsible for misuse of this tool.

- Only track information about yourself or with proper authorization
- Respect privacy and applicable laws (GDPR, CCPA, etc.)
- Do not use for harassment, stalking, or illegal activities

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 👨‍💻 Author

**HunxByts**

---

## 🙏 Acknowledgments

- [ipwho.is](https://ipwho.is/) - IP geolocation API
- [ipify.org](https://www.ipify.org/) - Public IP lookup
- [phonenumbers](https://github.com/daviddrysdale/python-phonenumbers) - Phone number parsing library

---

## 📞 Support

If you encounter any issues or have questions:
1. Check existing [Issues](https://github.com/HunxByts/GhostTrack/issues)
2. Create a new issue with detailed information
3. Include error messages and steps to reproduce

---

**⭐ Star this repository if you find it useful!**

<details>
<summary>:zap: Author :</summary>
- <strong><a href="https://github.com/HunxByts">HunxByts</a></strong>
</details>
