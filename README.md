<img src="https://github.com/user-attachments/assets/3bfcbf7e-a683-4adb-a3bc-ab78fe8995cf" width="300">

![Silent Knight](https://github.com/user-attachments/assets/771c89cf-03d4-4d41-aaba-f87b7f7a01b8)
# SilentKnightIDC - prepared by Team IDC
---

### IDC Team Members
- Landon Stott - The Quantum Cryptologist (QA Lead)
- Gabriel Palma - The Hash Herold (Subdivision Leader)
- Gavin Walter - The Cybernetic Centurion (Division Leader)
- Krisha Sidella - The Packet Paladin (Organizer Leader)

### Secure Communications Division - "The Oracle Protocol" 

Following incidents of communication systems being compromised by tech-savvy inmates like the Riddler and
Cluemaster, Arkham needs a completely secure communication infrastructure. This track focuses on developing
encrypted communication systems that ensure secure information flow between all authorized parties while
preventing unauthorized access.

Team Focus Areas:
* Encrypted communication protocols
* Secure data transmission
* Network security infrastructure
* Secure messaging systems
* Data integrity verification

### Project Notes

#### Script to run loginFastAPI.py
python -m uvicorn loginFastAPI:app --host localhost --port 8000

### Code packages to run app.py
pip install cryptography

### Code packages to run test cases 
pip install pytest httpx

pip install pytest

python -m pytest test_main.py -v
