# Python Inventory Management System

A comprehensive inventory management system built with Python, Streamlit, MongoDB, and AI capabilities powered by Google Gemini and Scaledown APIs.

## 🚀 Features

- **User Authentication** - Secure login/register with bcrypt password hashing
- **Inventory Management** - Full CRUD operations for products with SKU generation
- **Bill Generation** - Create invoices with automatic PDF export
- **AI Assistant** - Gemini-powered chatbot with Scaledown context compression
- **Analytics & Reports** - Sales trends, revenue analysis, and inventory valuation
- **Supplier Management** - Track and manage suppliers
- **Low Stock Alerts** - Automatic notifications for products below reorder level
- **Stock Movement Tracking** - Complete audit trail of inventory changes

## 📋 Prerequisites

- Python 3.10 or higher
- MongoDB (local or MongoDB Atlas)
- Google Gemini API key
- Scaledown API key 

## 🛠️ Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd Inventory_Management(P)
```

### 2. Create virtual environment

```bash
python -m venv venv

# Windows
.\venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the root directory:

```env
# MongoDB Configuration
MONGODB_URI=mongodb://localhost:27017/
DATABASE_NAME=inventory_management

# API Keys
GEMINI_API_KEY=your_gemini_api_key_here
SCALEDOWN_API_KEY=your_scaledown_api_key_here

# Application Settings
SECRET_KEY=your_secret_key_here
APP_NAME=Inventory Management System
```

### 5. Set up MongoDB

**Option A: Local MongoDB**
- Install MongoDB from https://www.mongodb.com/try/download/community
- Start MongoDB service

**Option B: MongoDB Atlas (Cloud)**
- Create free account at https://www.mongodb.com/cloud/atlas
- Create a cluster
- Get connection string and update `MONGODB_URI` in `.env`

### 6. Seed demo data (optional)

```bash
python utils/seed_data.py
```

This creates:
- Demo user: `admin` / `admin123`
- 3 suppliers
- 18 products across 5 categories

## 🚀 Running the Application

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

## 📱 Usage

### Login
- Use demo credentials: `admin` / `admin123`
- Or register a new account

### Dashboard
- View key metrics and analytics
- Monitor low stock items
- See recent bills and sales trends

### Inventory Management
- Add/edit/delete products
- Adjust stock levels
- Search and filter products
- Track stock movements

### Bill Generation
- Create invoices with cart system
- Automatic stock deduction
- PDF export functionality
- Search and view bill history

### AI Assistant
- Ask questions about inventory
- Get product recommendations
- View compression stats (Scaledown)
- Sample questions provided

### Analytics
- Sales trends and forecasting
- Top selling products
- Revenue by category
- Inventory valuation
- Export reports to CSV

### Supplier Management
- Add/edit/delete suppliers
- View associated products
- Track supplier information

## 🏗️ Project Structure

```
Inventory_Management(P)/
├── app.py                      # Main application
├── requirements.txt            # Dependencies
├── .env                        # Environment variables
├── config/
│   ├── database.py            # MongoDB configuration
├── models/
│   ├── user.py                # User model
│   ├── product.py             # Product model
│   ├── bill.py                # Bill model
│   └── supplier.py            # Supplier model
├── services/
│   └── ai_service.py          # AI integration
├── pages/
│   ├── 1_📊_Dashboard.py
│   ├── 2_📦_Inventory.py
│   ├── 3_🤖_AI_Chat.py
│   ├── 4_📄_Bills.py
│   ├── 5_📈_Analytics.py
│   └── 6_🏢_Suppliers.py
└── utils/
    ├── helpers.py             # Utility functions
    └── seed_data.py           # Demo data generator
```

## 🔑 API Keys

### Google Gemini API
1. Visit https://makersuite.google.com/app/apikey
2. Create API key
3. Add to `.env` as `GEMINI_API_KEY`

### Scaledown API (Optional)
1. Visit https://scaledown.ai
2. Sign up and get API key
3. Add to `.env` as `SCALEDOWN_API_KEY`

## 📊 Technologies Used

- **Frontend/Backend**: Streamlit
- **Database**: MongoDB (PyMongo)
- **AI**: Google Gemini API
- **Compression**: Scaledown API
- **PDF Generation**: fpdf2
- **Data Visualization**: Plotly
- **Data Processing**: Pandas
- **Authentication**: bcrypt

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License.

## 👨‍💻 Author

Created with ❤️ for efficient inventory management

## 🐛 Troubleshooting

### MongoDB Connection Issues
- Ensure MongoDB is running
- Check `MONGODB_URI` in `.env`
- For Atlas, whitelist your IP address

### API Key Errors
- Verify API keys in `.env`
- Check API key validity
- Ensure proper formatting

### PDF Generation Issues
- Check `bills/` directory exists
- Verify write permissions
- Install fpdf2: `pip install fpdf2`

## 📞 Support

For issues and questions, please open an issue on GitHub.
