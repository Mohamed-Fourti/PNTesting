# PNTesting
PNTesting is a simple security tool designed to streamline basic security auditing and testing processes. It provides a user-friendly interface for performing various basic security assessments, including port scanning, SSH password cracking, and simple vulnerability reporting. 

# Login in
The Tool requires establishing a connection to a virtual machine (Cloud/local) where the tools (Nmap, Hydra) need to be installed to perform the security assessments.

![Picture1](https://github.com/Mohamed-Fourti/PNTesting/assets/61188969/79cf75a1-24ed-4e40-92c3-1989224dfac7)
![Picture2](https://github.com/Mohamed-Fourti/PNTesting/assets/61188969/f56cab84-2c60-4c76-a77f-a85834523232)

# Key Features
**Port Scanning:** The tool allows performing port scanning on multiple targets. It utilizes Nmap, to discover open ports on target systems, providing insights into network configuration and potential vulnerabilities.

![Picture3](https://github.com/Mohamed-Fourti/PNTesting/assets/61188969/e498accb-c6fe-44ff-a61e-791d2f0146cf)

**Password Cracking:** This can be used to attempt unauthorized access to unsecured machines through SSH. It utilizes Hydra to perform brute force By trying different combinations of usernames and passwords.

![Picture4](https://github.com/Mohamed-Fourti/PNTesting/assets/61188969/572f2d39-caee-4104-8945-379943c40108)

**Security Suggestions:** The tool utilizes port scan reports to generate security recommendations and best practices. It matches scanned ports with an SQLite database containing known vulnerabilities and associated countermeasures. (Still in progress)

# Getting Started
To use the tool, follow these steps:

1-Clone the repository to your local machine.

2-Install the required dependencies.

3-Launch the tool by running the Login Python script.

4-Provide the necessary login details, such as username, private key, and target system IP address.

# Disclaimer
The owner of this tool is not liable for any actions taken or consequences arising from the use it.
