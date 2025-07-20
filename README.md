# AniNews Project Setup

An ai newsletter, hosted at news.iqs8.org. Instructions below on how to run your own. 

---

## 1. Prerequisites

- [Node.js](https://nodejs.org/) (for serverless functions)
- [Python 3.8+](https://www.python.org/) (for SendEmail-TimerTrigger)
- [Azure Functions Core Tools](https://docs.microsoft.com/azure/azure-functions/functions-run-local) (for local Azure Functions development)
- **An [OpenAI API key](https://platform.openai.com/account/api-keys)**
- **A Gmail account with an [App Password](https://support.google.com/accounts/answer/185833?hl=en) for programmatic email sending**
- **An [Azure CosmosDB](https://azure.microsoft.com/en-us/products/cosmos-db/) instance**

---

## 2. Set Up Environment Variables Locally

Before deploying, you should configure your environment variables for local testing.

Create a file named `local.settings.json` inside both the `SendEmail-TimerTrigger/` and `server-serverless/` directories:

```json
{
  "IsEncrypted": false,
  "Values": {
    "AzureWebJobsStorage": "UseDevelopmentStorage=true",
    "FUNCTIONS_WORKER_RUNTIME": "python",
    "COSMOS_ENDPOINT": "<your-cosmos-db-endpoint>",
    "COSMOS_KEY": "<your-cosmos-db-key>",
    "COSMOS_DATABASE": "<your-database-name>",
    "COSMOS_CONTAINER": "<your-container-name>",
    "GMAIL_USERNAME": "<your-gmail-username>",
    "GMAIL_PASSWORD": "<your-gmail-app-password>",
    "OPENAI_KEY": "<your-openai-api-key>"
  }
}
```

**Replace all values in angle brackets with your own credentials.**

> **Note:** Make sure your `.gitignore` file includes `local.settings.json` so your secrets are never committed.  
> Add the following lines to your `.gitignore` if they are not already present:
> ```
> local.settings.json
> **/local.settings.json
> ```

---

## 3. Install Dependencies

### For Node.js (server-serverless):

```sh
cd server-serverless
npm install
```

### For Python (SendEmail-TimerTrigger):

```sh
cd ../SendEmail-TimerTrigger
pip install -r requirements.txt
```

---

## 4. Deployment Order (IMPORTANT)

**You must deploy the serverless backend (server-serverless) before deploying the frontend and the SendEmail-TimerTrigger function.**

- The backend provides the `/api/unsubscribe/{user_id}` endpoint, which is required for the unsubscribe link in emails sent by the timer trigger function (`sendEmails.py`, line 63).
- The frontend and the timer trigger function both depend on the deployed backend URL.

---

## 5. Running Locally

- **Azure Functions:**  
  Use Azure Functions Core Tools to run the Python function locally:
  ```sh
  func start
  ```

- **Node.js Serverless Functions:**  
  Use your preferred method (e.g., `npm start` or `func start` if using Azure Functions).

Test your functions locally to ensure everything works before deploying to Azure.

---

## 6. Deploy Azure Resources

### a. Deploy CosmosDB

Set up your CosmosDB instance in Azure if you haven't already.  
Take note of your CosmosDB endpoint, key, database name, and container name.  
You will need these values for your environment configuration.

### b. Deploy Serverless Backend (server-serverless) **[Deploy this first!]**

Deploy the serverless backend (subscribe/unsubscribe endpoints) to Azure.  
After deployment, you will have the necessary backend URL for the unsubscribe link and for the frontend to use.

### c. Deploy Azure Functions (SendEmail-TimerTrigger)

Deploy the SendEmail-TimerTrigger function to Azure.  
**Before deploying, update the unsubscribe link in `sendEmails.py` (line 63) to use your actual deployed backend URL:**
```python
unsub_link = f"https://your-server-url/api/unsubscribe/{user_id}"
```
Replace `https://your-server-url` with your real backend URL.

---

## 7. Set Up Environment Variables in Azure

When deploying to Azure, add all the variables from your `local.settings.json` files to your Azure Function App’s **Application Settings** in the Azure Portal.  
`local.settings.json` is for local development only and is not uploaded to Azure.

---

## 8. Set Up the Frontend

After deploying your backend (subscribe endpoint), update your frontend to use the correct API endpoint.

1. Open `HTML/main.js`.
2. Find the line with the `endpoint` variable:
   ```js
   const endpoint = "https://your-backend-url/api/subscribe"; // <-- replace with your real endpoint
   ```
3. Replace the placeholder URL with your actual deployed backend URL.
4. Save the file.
5. Deploy the front end on whichever service you like. 

> **Note:** Do not commit your real endpoint to the repository.

---

## 9. Security

- `local.settings.json` is in `.gitignore` and should not be tracked.

---