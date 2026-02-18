# Vaultly Inventory Management System - Technical Documentation

## 1. Project Overview
Vaultly is an advanced, AI-powered inventory management system designed to streamline business operations. It combines traditional inventory control with Generative AI to offer features like natural language querying, automated content generation, and intelligent search.

### Tech Stack
- **Frontend/Backend Framework**: Streamlit (Python)
- **Database**: MongoDB (Local or Atlas)
- **AI Engine**: Google Gemini Pro (via `google-generativeai`)
- **Optimization**: Scaledown API (for context window management)
- **Visualization**: Plotly
- **Authentication**: bcrypt for password hashing

---

## 2. System Architecture

### 2.1 Core Components
1.  **Streamlit App (`app.py`)**: The entry point that handles routing, authentication, and the global sidebar.
2.  **Views (`views/`)**: Separate modules for each page (Dashboard, Inventory, Chat, etc.) to maintain a clean codebase.
3.  **Services (`services/`)**: 
    - `ai_service.py`: Encapsulates all interactions with LLMs, including context gathering, RAG implementation, and prompt engineering.
4.  **Models (`models/`)**: Data abstraction layer using PyMongo to interact with MongoDB collections.

### 2.2 AI Integration Flow
1.  **User Input**: User asks a question or gives a command in the Chat UI.
2.  **Intent Recognition**: The system executes regex-based or logic-based checks (e.g., detecting "search" keywords for RAG).
3.  **Context Gathering**:
    - Fetches product data, sales summaries, and low-stock alerts.
    - Uses **Scaledown API** to compress massive JSON data into token-efficient text.
4.  **RAG (Retrieval-Augmented Generation)**:
    - If a search intent is detected, specific database queries run *before* the LLM call.
    - Results are injected into the system prompt.
5.  **LLM Processing**: Gemini processes the enriched prompt and generates a response or structured JSON action.
6.  **Action Execution**: The app parses the JSON response to perform actions like creating Purchase Orders or rendering charts.

---

## 3. Key Features Deep Dive

### 3.1 Smart Search (RAG)
Unlike simple string matching, the Smart Search feature decomposes user queries into multi-term AND logic conditions.
- **Trigger**: "Find", "Search", "Where is".
- **Logic**: Searches across Name, SKU, Category, and Description fields simultaneously.
- **Benefit**: Allows users to find specific items even with partial or mixed queries (e.g., "Gaming Chair Red").

### 3.2 AI-Powered Email Drafting
Users can command the AI to draft emails for suppliers or clients.
- **Format**: The AI outputs a JSON object with `recipient`, `subject`, and `body`.
- **UI**: The chat interface renders this as a formatted card with a **"🚀 Send via Email App"** button that opens the user's default mail client (`mailto:` link).

### 3.3 Sales Analytics
Real-time sales insights are injected into the AI's context.
- **Data Source**: Aggregates data from `SalesOrder` collection.
- **Metrics**: Total Revenue, Order Count, Average Order Value, Top Selling Products.
- **Interaction**: Users can ask natural language questions like "How is our revenue this week?" without needing to navigate to the analytics dashboard.

---

## 4. Database Schema

The system uses a document-oriented NoSQL schema in MongoDB.

### **Users Collection**
- `username`: String (Unique)
- `password`: String (Hashed)
- `role`: String (Admin/User)
- `name`: String

### **Products Collection**
- `name`: String
- `sku`: String (Unique)
- `category`: String
- `price`: Float
- `stock`: Integer
- `description`: String
- `supplier_id`: ObjectId

### **Suppliers Collection**
- `name`: String
- `email`: String
- `phone`: String
- `address`: String

### **PurchaseOrders Collection**
- `po_number`: String (Unique)
- `supplier_name`: String
- `items`: Array of Objects `{product_id, quantity, price}`
- `status`: String (Draft, Sent, Received)
- `created_at`: DateTime

### **SalesOrders Collection**
- `order_id`: String
- `customer_name`: String
- `items`: Array of Objects
- `total_amount`: Float
- `date`: DateTime

---

## 5. Setup & Installation

See `SETUP_GUIDE.md` for quick start instructions.

**Environment Variables (.env)**
```env
MONGODB_URI=...
DATABASE_NAME=inventory_management
GEMINI_API_KEY=...
SCALEDOWN_API_KEY=...
SECRET_KEY=...
```

---

## 6. Troubleshooting

**Common Issues:**
- **"DuplicateWidgetID"**: Occurs if Streamlit renders multiple widgets with same ID. Fixed by assigning unique keys based on history index.
- **"Connection Error"**: Check MongoDB service status or Atlas whitelist IP settings.
- **AI Not Responding**: Verify `GEMINI_API_KEY` quota and validity.

---
*Generated: February 2026*
