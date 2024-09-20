"""
Script to be called every time the articles database should be updated
"""

import os
import psycopg2
from psycopg2 import sql
import streamlit as st

PATH_ARTICLES_ACTIVE = "../ArticlesActive"
PATH_ARTICLES_UNACTIVE = "../ArticlesUnactive"


def check_articles_exists(cursor, filename):
    query = sql.SQL("SELECT * FROM articles WHERE name = %s")
    cursor.execute(query, [filename])
    return cursor.fetchone()

def update_article(cursor, filename, active):
    query = sql.SQL("""
        UPDATE articles
        SET active = %s
        WHERE name = %s
    """)
    cursor.execute(query, [active, filename])

def insert_article(cursor, filename, path, active):
    query = sql.SQL("""
        INSERT INTO articles(name, path, active)
        VALUES (%s, %s, %s)
    """)
    cursor.execute(query, [filename, path, active])
    


db_config = st.secrets["connections"]["postgresql"]
conn = psycopg2.connect(host=db_config['host'],
                      port=db_config['port'],
                      database=db_config['database'],
                      user= db_config['username'],
                      password= db_config['password'])
cursor = conn.cursor()

pdf_files_active = [os.path.join(PATH_ARTICLES_ACTIVE,f) for f in os.listdir(PATH_ARTICLES_ACTIVE) if f.endswith(".pdf")]
pdf_files_unactive= [os.path.join(PATH_ARTICLES_UNACTIVE,f) for f in os.listdir(PATH_ARTICLES_UNACTIVE) if f.endswith(".pdf")]

for pdf in pdf_files_active:
    name = os.path.basename(pdf)
    active = True
    article_exists = check_articles_exists(cursor, name)

    if article_exists:
        update_article(cursor, name, active)
    else:
        insert_article(cursor, name, os.path.abspath(pdf), active)

for pdf in pdf_files_unactive:
    name = os.path.basename(pdf)
    active = False
    article_exists = check_articles_exists(cursor, name)

    if article_exists:
        update_article(cursor, name, active)
    else:
        insert_article(cursor, name, os.path.abspath(pdf), active)

conn.commit()
cursor.close()
conn.close()
print("Changes realized on the articles database.")

