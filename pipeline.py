import os
import random
import duckdb
import pandas as pd
from faker import Faker

fake = Faker()

CSV_PATH = "data/youtube_data.csv"
DB_PATH = "database/youtube_analytics.duckdb"

# -------------------------------------------------------------------
# STEP 1: GENERATE EXACT 250 REALISTIC RECORDS
# -------------------------------------------------------------------
def generate_250_records_dataset():
    print("--- [STEP 1] Generating 250-Row Realistic Dataset ---")
    
    categories = ['Education', 'Gaming', 'Tech', 'Music', 'Entertainment', 'Finance', 'Food', 'Travel', 'Fitness', 'Automobile']
    
    tech_topics = ['Python Tutorial', 'AI Tools', 'iPhone Review', 'DuckDB Crash Course', 'Web Dev 2026', 'Data Science Guide']
    gaming_topics = ['GTA 6 Walkthrough', 'Valorant Highlights', 'Minecraft Hardcore', 'Apex Legends Pro', 'Fortnite Stream']
    edu_topics = ['SQL vs NoSQL', 'Machine Learning 101', 'Calculus Made Easy', 'Resume Tips', 'Exam Preparation']
    music_topics = ['Lofi Beats 24/7', 'Acoustic Cover', 'EDM Party Mix', 'Piano Melodies', 'Pop Hit Single']
    ent_topics = ['Standup Comedy', 'Movie Review', 'Daily Vlog', 'Behind The Scenes', 'Celebrity Interview']

    dataset = []
    
    for i in range(1, 251):  # Exactly 250 rows
        cat = random.choice(categories)
        
        # Topic selection based on category
        if cat == 'Tech':
            title_base = random.choice(tech_topics)
        elif cat == 'Gaming':
            title_base = random.choice(gaming_topics)
        elif cat == 'Education':
            title_base = random.choice(edu_topics)
        elif cat == 'Music':
            title_base = random.choice(music_topics)
        else:
            title_base = random.choice(ent_topics)
            
        title = f"{title_base} - Part {random.randint(1, 10)}" if random.random() > 0.5 else title_base
        views = random.randint(10000, 3500000)
        likes = int(views * random.uniform(0.02, 0.10))
        comments = int(likes * random.uniform(0.05, 0.20))
        
        dataset.append({
            'video_id': f'VID_{i:03d}',
            'title': title,
            'category': cat,
            'views': views,
            'likes': likes,
            'comment_count': comments
        })
        
    df = pd.DataFrame(dataset)
    df.to_csv(CSV_PATH, index=False)
    print(f"[SUCCESS] Dataset created with exactly {len(df)} rows at '{CSV_PATH}'")
    return df

# -------------------------------------------------------------------
# STEP 2: PIPELINE EXECUTION & DUCKDB STORAGE
# -------------------------------------------------------------------
def run_pipeline():
    os.makedirs("data", exist_ok=True)
    os.makedirs("database", exist_ok=True)
    
    # Generate 250 rows CSV
    df = generate_250_records_dataset()
    
    print("\n--- [STEP 2] Cleaning & Storing Data in DuckDB ---")
    
    # Quality Cleanups
    df = df.drop_duplicates(subset=['video_id'])
    df = df[df['views'] > 0]
    df['category'] = df['category'].fillna('General')
    
    # Store in DuckDB
    conn = duckdb.connect(DB_PATH)
    conn.execute("CREATE OR REPLACE TABLE youtube_analytics AS SELECT * FROM df")
    conn.close()
    
    print(f"[COMPLETED] Total {len(df)} clean records successfully stored in DuckDB!")

if __name__ == "__main__":
    run_pipeline()