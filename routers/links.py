from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, HttpUrl
import random
import string
import psycopg2
from psycopg2 import sql
from datetime import datetime

router = APIRouter()

class LinkCreate(BaseModel):
    url: HttpUrl
    custom_slug: str = Query(None, min_length=3, max_length=32)

def generate_random_slug(length=8):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def insert_link(original_url, slug):
    conn = psycopg2.connect("dbname=yourdbname user=youruser password=yourpassword")
    cursor = conn.cursor()
    try:
        cursor.execute(
            sql.SQL("INSERT INTO links (original_url, slug, created_at) VALUES (%s, %s, %s) RETURNING id;"),
            (original_url, slug, datetime.utcnow())
        )
        link_id = cursor.fetchone()[0]
        conn.commit()
        return link_id
    except psycopg2.IntegrityError:
        conn.rollback()
        raise HTTPException(status_code=409, detail="Slug already exists")
    finally:
        cursor.close()
        conn.close()

@router.post("/api/v1/links", status_code=201)
async def create_link(link: LinkCreate):
    if link.custom_slug:
        slug = link.custom_slug
    else:
        slug = generate_random_slug()

    link_id = insert_link(link.url, slug)
    return {"id": link_id, "original_url": link.url, "slug": slug, "created_at": datetime.utcnow()}
