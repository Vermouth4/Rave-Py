# Rave App Version 4.3 Jailbreak

## Overview

This project demonstrates a method to interact with the backend of the Rave application, version 4.3. The source code provided can be used to perform various actions within the app, such as authentication, profile management, friend requests, and more, by sending requests to the application's API endpoints.

> **Note**: This code is for educational purposes only. Unauthorized use of this code to access or manipulate the Rave app or any other platform may violate their terms of service and could result in legal consequences.

### Developed By
- **Kratos** | Saudi flag flying 🇸🇦
- **Light Xc** | The flag of the Kingdom of Saudi Arabia is flying 🇸🇦

### Credits
- **Khaleed Kratos**
- **Lait**
- **Vermouth**

## How It Works

This codebase interacts with the Rave app's backend using the following methods:

### Key Functions

- **nonce()**: Generates a unique identifier for each request.
- **gen_dev_id()**: Generates a unique device ID.
- **ts()**: Generates a timestamp used in request signing.
- **req_hash(ts, sess_id, content_len)**: Generates a request hash to authenticate API requests.

### Headers

The headers required to make successful API calls are constructed using the `Hdrs` class, which adds necessary authentication, content-type, and user-agent information.

### Service Class (Svc)

This class provides methods for making HTTP requests (`GET`, `POST`, `DELETE`, `PUT`) to the Rave app's backend API. It also includes methods for interacting with MojoAuth, an external service used for email verification.

### Client Class (Clnt)

This class extends the `Svc` class and adds functionality specific to the Rave app, such as:

- **req_verif(email, lang="en")**: Requests an email verification link.
- **mojo_status(state_id)**: Checks the status of the MojoAuth verification.
- **soborol_login(email, mojo_id_token)**: Logs in using the MojoAuth token.
- **login(email, password)**: Logs in using email and password.
- **chk_usr(username)**: Checks if a username is available.
- **acct_info()**: Retrieves account information.
- **edit_prof(name, handle, avatar)**: Edits the user's profile.

## Usage

To use this code:

1. Clone the repository.
2. Install the required dependencies using `pip install -r requirements.txt`.
3. Import and instantiate the `Clnt` class from the script.
4. Call the desired methods with the appropriate parameters.

Example:

```python
client = Clnt()
state_id = client.req_verif("your-email@example.com")
status = client.mojo_status(state_id)
print(status)
