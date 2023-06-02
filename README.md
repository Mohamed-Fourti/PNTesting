# PNTesting
PNTesting is a simple security tool designed to streamline basic security auditing and testing processes. It provides a user-friendly interface for performing various basic security assessments, including port scanning, SSH password cracking, and simple vulnerability reporting. 

# Login in
The Tool requires establishing a connection to a virtual machine (Cloud/local) where the tools (Nmap, Hydra) need to be installed to perform the security assessments.

![Picture1](https://github.com/Mohamed-Fourti/PNTesting/assets/61188969/9713dc1c-5f1d-4ae6-ada0-39cee84b7d1d)
![Picture2](https://github.com/Mohamed-Fourti/PNTesting/assets/61188969/d00acbb9-4ebe-4e0f-85ff-2f0d0853c804)

# Key Features
**Port Scanning:** The tool allows performing port scanning on multiple targets. It utilizes Nmap, to discover open ports on target systems, providing insights into network configuration and potential vulnerabilities.

![Picture3](https://github.com/Mohamed-Fourti/PNTesting/assets/61188969/41eaeb6d-3876-400e-8224-42b6c86e26b9)

**Password Cracking:** This can be used to attempt unauthorized access to unsecured machines through SSH. It utilizes Hydra to perform brute force By trying different combinations of usernames and passwords.

![Picture4](https://github.com/Mohamed-Fourti/PNTesting/assets/61188969/52b04586-94bf-4a2f-82c3-07402aa70ad5)

**Security Suggestions:** The tool utilizes port scan reports to generate security recommendations and best practices. It matches scanned ports with an SQLite database containing known vulnerabilities and associated countermeasures. (Still in progress)

# Getting Started
To use the tool, follow these steps:

1-Clone the repository to your local machine.

2-Install the required dependencies.

3-Launch the tool by running the Login Python script.

4-Provide the necessary login details, such as username, private key, and target system IP address.

# Disclaimer
The owner of this tool is not liable for any actions taken or consequences arising from the use it.
