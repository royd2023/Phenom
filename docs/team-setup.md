# Team Setup Guide - U-CHS

Step-by-step guide for setting up U-CHS with Supabase for team collaboration.

## Why Supabase?

- ✅ **Shared Database** - Everyone works with the same data
- ✅ **No Local PostgreSQL** - One less thing to install
- ✅ **Built-in Storage** - Image uploads handled automatically
- ✅ **Real-time Updates** - See changes instantly
- ✅ **Free Tier** - Perfect for development

## One-Time Team Setup (Do This Once)

### 1. Create Supabase Project

**Designate ONE person** (e.g., Person B from roadmap) to:

1. Go to [supabase.com](https://supabase.com)
2. Sign up / Log in
3. Click "New Project"
4. Fill in:
   - **Name**: U-CHS Development
   - **Database Password**: Generate a strong password (SAVE THIS!)
   - **Region**: Choose closest to your team
   - **Pricing Plan**: Free
5. Wait 2 minutes for project creation

### 2. Create Storage Bucket

In your Supabase project:

1. Go to **Storage** (left sidebar)
2. Click **New bucket**
3. Name: `crop-images`
4. **Public bucket**: ✅ Check this (so images are accessible)
5. Click **Create bucket**

### 3. Set Bucket Policies (Make it Public)

1. Click on `crop-images` bucket
2. Go to **Policies** tab
3. Click **New Policy** → **For full customization**
4. Add this policy:

```sql
-- Allow public read access
CREATE POLICY "Public Access"
ON storage.objects FOR SELECT
USING ( bucket_id = 'crop-images' );

-- Allow authenticated uploads
CREATE POLICY "Authenticated Upload"
ON storage.objects FOR INSERT
WITH CHECK ( bucket_id = 'crop-images' );
```

### 4. Share Team Credentials

**Person B** shares these with the team (via secure channel - NOT public GitHub!):

#### Get Database URL:
1. Go to **Settings** → **Database**
2. Scroll to **Connection string** → **URI**
3. Copy the connection string (looks like):
   ```
   postgresql://postgres:[YOUR-PASSWORD]@db.xxx.supabase.co:5432/postgres
   ```

#### Get API Credentials:
1. Go to **Settings** → **API**
2. Copy:
   - **Project URL**: `https://xxx.supabase.co`
   - **anon public** key (long string)

## Individual Developer Setup (Each Person Does This)

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd Phenom
```

### 2. Create .env File

```bash
# Copy the example
cp .env.example .env

# Open in your editor
code .env  # or nano .env, or vim .env
```

### 3. Fill in Team Credentials

Replace with values from Person B:

```bash
# Supabase Database
DATABASE_URL=postgresql://postgres:[PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres

# Supabase API
SUPABASE_URL=https://[PROJECT-REF].supabase.co
SUPABASE_KEY=[YOUR-ANON-KEY]
SUPABASE_BUCKET=crop-images

# Generate your own secret key (each developer can have different one for local dev)
SECRET_KEY=$(openssl rand -hex 32)

# Rest can stay as defaults
DEBUG=True
USE_GPU=False
```

### 4. Start Development

```bash
# Option A: Using Docker (Recommended)
docker-compose up

# Option B: Manual
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### 5. Verify Connection

Visit: http://localhost:8000/api/docs

Try the `/api/v1/health` endpoint - should return:
```json
{
  "status": "healthy",
  "version": "0.1.0",
  ...
}
```

## Database Schema Setup (Do Once)

After everyone is connected, ONE person should run:

```bash
# TODO: Add Alembic migration when we create database models
# For now, tables will be created automatically when first used
```

## Team Collaboration Workflow

### Sharing Data

Since everyone uses the same Supabase database:

1. **Upload an image** → Everyone can see it
2. **Create analysis** → Appears in everyone's history
3. **Test with real data** → No need for mock data

### Best Practices

1. **Don't delete others' data** unless coordinating
2. **Use descriptive filenames** for test images
3. **Tag test data** (e.g., username in metadata)
4. **Communicate** before running migrations or schema changes

## Troubleshooting

### "Connection refused" errors

- Check your `DATABASE_URL` is correct
- Verify Supabase project is running (check dashboard)
- Check your IP isn't blocked (Supabase free tier is worldwide)

### "Storage bucket not found"

- Verify bucket name is exactly `crop-images`
- Check bucket is created in Supabase dashboard
- Ensure `SUPABASE_BUCKET` in .env matches

### "Unauthorized" errors

- Check `SUPABASE_KEY` is the **anon** key, not service_role
- Verify key hasn't been regenerated in Supabase dashboard

### Images not uploading

- Check storage policies are set correctly
- Verify bucket is **public**
- Check file size limits (default 50MB)

## Switching to Production Later

When deploying to production:

1. Create **separate** Supabase project for production
2. Use environment variables to switch between dev/prod
3. Keep dev database for testing

## Alternative: Local Development

If working offline or wanting isolated data:

```bash
# Use local PostgreSQL instead
docker-compose --profile local-db up

# Update .env to:
DATABASE_URL=postgresql://uchs_user:uchs_password@localhost:5432/uchs_db
STORAGE_PROVIDER=local  # Store images locally
```

## Need Help?

- **Supabase Docs**: https://supabase.com/docs
- **Team Lead**: [Person B - your contact info]
- **Project Issues**: Create GitHub issue
