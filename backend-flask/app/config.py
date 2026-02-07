import os

class Config:
    secret_key = os.getenv('SECRET_KEY') or 'Hackathon2026'
    