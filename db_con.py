from supabase import create_client, Client
import os
from dotenv import load_dotenv


# Load environment variables
load_dotenv()

# Supabase credentials
# Get Supabase credentials from .env
SUPABASE_URL = "https://uiejrmqsocfhdyltdttj.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVpZWpybXFzb2NmaGR5bHRkdHRqIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDI2NDU4OTYsImV4cCI6MjA1ODIyMTg5Nn0.YEa2rv3iRaQ0YrUK_EuG6bKz2CG0P25zpPtqWsuZGi0"

def get_supabase_client() -> Client:
    """Create and return a Supabase client"""
    return create_client(SUPABASE_URL, SUPABASE_KEY)
