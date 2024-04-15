# Cluster API Get Index

This Python script is designed to interact with a cluster's API to authenticate and retrieve Logical Interface Numbers (LINs). It handles authentication securely, suppresses warnings for self-signed certificates, and implements basic error handling.

## Features

- Secure Authentication: Logs into the cluster and establishes a session with CSRF protection.
- Fetch LINs: Retrieves a list of LINs from the specified cluster.

## Prerequisites

- Python 3
- requests library

You can install the required Python library using pip:

```
pip install requests
```

## Configuration

The script uses environment variables for configuration to avoid hardcoding sensitive information:

- CLUSTER_IP: The IP address of the cluster.
- PORT: The port number used by the cluster's API.
- USER: Username for authentication.
- PASSWORD: Password for authentication.

Set these variables in your environment before running the script.

## Usage

1. Set the necessary environment variables:
   ```
   export CLUSTER_IP='192.168.1.1'
   export PORT='443'
   export USER='admin'
   export PASSWORD='password'
   ```

2. Run the script from the command line:
   python3 cluster_api_tool.py

## Handling Errors

The script includes error handling for authentication failures and API request errors. It provides detailed error messages and response statuses to help with troubleshooting.

## Security Notes

- The script disables SSL verification for the sake of simplicity and to allow the use of self-signed certificates. For production environments, it is recommended to handle SSL certificates properly.

## Contributing

Feel free to fork the repository and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the LICENSE.md file for details.
