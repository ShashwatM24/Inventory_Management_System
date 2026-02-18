# Quick Setup Guide

## Step 1: Add Your Gemini API Key

1. Open `.env` file
2. Add your Gemini API key:
   ```
   GEMINI_API_KEY=your_actual_api_key_here
   ```

## Step 2: Choose MongoDB Option

### Option A: Local MongoDB (Current Setup)
- Already configured in `.env`
- Works only when your PC is on
- Good for: Local development

### Option B: MongoDB Atlas (Recommended for Showcasing)

**Setup Steps:**

1. **Create Free Account**
   - Go to: https://www.mongodb.com/cloud/atlas/register
   - Sign up with email

2. **Create Cluster**
   - Click "Build a Database"
   - Choose "FREE" (M0 Sandbox)
   - Select region closest to you
   - Click "Create"

3. **Create Database User**
   - Go to "Database Access"
   - Click "Add New Database User"
   - Username: `admin`
   - Password: Create a strong password (save it!)
   - Click "Add User"

4. **Whitelist IP Address**
   - Go to "Network Access"
   - Click "Add IP Address"
   - Click "Allow Access from Anywhere" (for demo purposes)
   - Click "Confirm"

5. **Get Connection String**
   - Go to "Database" → "Connect"
   - Choose "Connect your application"
   - Copy the connection string
   - It looks like: `mongodb+srv://admin:<password>@cluster0.xxxxx.mongodb.net/...`

6. **Update .env File**
   - Open `.env`
   - Comment out local MongoDB:
     ```
     # MONGODB_URI=mongodb://localhost:27017/
     ```
   - Uncomment Atlas and paste your connection string:
     ```
     MONGODB_URI=mongodb+srv://admin:YOUR_PASSWORD@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority
     ```
   - Replace `<password>` with your actual password
   - Replace `xxxxx` with your cluster ID

## Step 3: Seed Demo Data

```bash
python utils/seed_data.py
```

This creates:
- Demo user: `admin` / `admin123`
- 3 suppliers
- 18 products

## Step 4: Run Application

```bash
streamlit run app.py
```

## Step 5: Login

- Username: `admin`
- Password: `admin123`

## Troubleshooting

### MongoDB Connection Failed
- **Local**: Ensure MongoDB service is running
- **Atlas**: Check connection string, password, and IP whitelist

### API Key Error
- Verify Gemini API key in `.env`
- No spaces or quotes around the key

### Import Errors
- Run: `pip install -r requirements.txt`

## Next Steps

1. Test all features
2. Add your own products
3. Generate some bills
4. Try the AI chatbot
5. View analytics

## For Showcasing

**With Local MongoDB:**
- ❌ Won't work when laptop is off
- ❌ Can't share with others remotely

**With MongoDB Atlas:**
- ✅ Works 24/7
- ✅ Can deploy to Streamlit Cloud
- ✅ Share with anyone via URL
- ✅ Perfect for portfolio

**Recommendation:** Use Atlas for your final project!
