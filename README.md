# Mutator

## How to Run the Mutator?

### Step 1: Install the requirements.txt file
Use pip to install the requirements.

```bash
pip install -r requirements.txt
```

### Step 2: Configure your application details in cloud-proxy.py
Line 159 - 162 are mean't for configuration of your application. Following are the variables that need to be modified accordingly.
<b>app_url (mandatory)</b> - The fully qualified url of your application.
<b>app_name (optional)</b> - Name that is given to the app. Used for creating the dataset.
<b>port_no (optional)</b> - In which port you need to start the Proxy. Defaults to 2820.
<b>generate (optional)</b> - If set as True, the Proxy will be configured for dataset generation. If set as False, Proxy will be configured for mutation. Defaults to True.

### Step 3: Run cloud-proxy.py
Run cloud-proxy.py and the proxy will be up on the port mentioned in the file. After that you can enter the proxy details in your application and data can be passed for dataset generation or mutation.
