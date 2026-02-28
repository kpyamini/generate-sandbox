# OpenAPI Mock Generator

A FastAPI service that accepts an OpenAPI specification file and uses OpenAI GPT to automatically generate a **NodeRED mock endpoints JSON** and a **Postman collection JSON**.

This tool will come handy if you want to experiment with an API running on a mock server and test its functionality using postman.

---

## Features

- Upload any OpenAPI spec file (`.yaml` or `.json`)
- Generates a NodeRED-importable mock flow JSON
- Generates a Postman-importable collection JSON
- Powered by OpenAI `gpt-4.1-nano`

---

## Requirements

- Python 3.8+
- An OpenAI API key

---

## Installation

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd <your-project-folder>
   ```

2. **Install dependencies:**
   ```bash
   pip install fastapi uvicorn python-dotenv openai
   ```

3. **Create a `.env` file** in the project root:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

---

## Running the Server

```bash
uvicorn main:app --reload
```

The server will start at `http://127.0.0.1:8000`

> Replace `main` with your actual filename (without `.py`) if it differs.

---

## API Endpoint

### `POST /generate-sandbox`

Accepts an OpenAPI spec file and returns generated NodeRED and Postman JSONs.

**Request:**
- Method: `POST`
- Content-Type: `multipart/form-data`
- Body: a file field named `file` containing your OpenAPI spec

**Response:**
```json
{
  "nodered": { ... },
  "postman": { ... }
}
```

---

## Testing with Postman

1. Open Postman
2. Set method to **POST**
3. Enter URL: `http://127.0.0.1:8000/generate-sandbox`
4. Go to **Body** → select **form-data**
5. Add a key named `file`, change the type to **File**, and upload your OpenAPI spec
6. Click **Send**

---

## Project Structure

```
.
├── main.py          # FastAPI application
├── .env             # Environment variables (do not commit)
├── .env.example     # Example env file (safe to commit)
└── README.md
```

---

## .gitignore

Make sure to add the following to your `.gitignore`:

```
.env
__pycache__/
*.pyc
```

---

## Environment Variables

| Variable | Description |
|---|---|
| `OPENAI_API_KEY` | Your OpenAI API key |