from flask import Flask, request, jsonify
from sqlalchemy import select, insert, update, delete, text
from backend import (
    shorten_url_table, 
    shorten_url_table_stats, 
    engine)
import string
import random
from dataclasses import dataclass
from typing import Optional

app = Flask(__name__)

@dataclass
class ShortenUrl:
    id: int
    url: str
    short_code: str
    updated_at: Optional[str]
    created_at: Optional[str]



def make_short_code() -> str:
    characters = string.ascii_letters + string.digits
    short_code = ''.join(random.choice(characters) for i in range(6))
    return short_code


@app.route('/shorten', methods=['POST'])
def shorten():
    data = request.get_json()
    url = data.get('url')

    with engine.connect() as connection:

        if not url:
            return jsonify({'error': 'URL is required'}), 400
        
        # Validate if url exists
        row = connection.execute(select(shorten_url_table).where(shorten_url_table.c.url == url)).first()

        if not row:
            insert_statement = insert(shorten_url_table).values(
                url=url,
                short_code=make_short_code()
            )
            result = connection.execute(insert_statement)

            connection.commit()
            
            id = result.inserted_primary_key

            row = connection.execute( select(shorten_url_table).where(shorten_url_table.c.id == id[0]))

            response = ShortenUrl(*row.first()).__dict__
        else:
            return jsonify({'error': 'URL already exists'}), 400

        return response, 200

@app.route('/shorten/<short_code>', methods=['GET'])
def get_url(short_code: str):

    with engine.connect() as connection:
        select_stmt = select(shorten_url_table).\
            where(shorten_url_table.c.short_code == short_code)

        
        row = connection.execute(select_stmt).first()

        if not row:
            return jsonify({'error': 'URL not found'}), 404

        shorten_obj = connection.execute(select(shorten_url_table).where(shorten_url_table.c.short_code == short_code)).first()

        id = shorten_obj.id

        shorten_stats_count = connection.execute(select(shorten_url_table_stats).\
                                           where(shorten_url_table_stats.c.shorten_url_id == id)).first()
        if not shorten_stats_count:
            insert_statement = insert(shorten_url_table_stats).values(
                shorten_url_id=id,
                access_count=1
            )
            connection.execute(insert_statement)
            connection.commit()
        else:
            update_statement = update(shorten_url_table_stats).\
                where(shorten_url_table_stats.c.shorten_url_id == id).\
                    values(access_count=shorten_stats_count.access_count+1)
            connection.execute(update_statement)
            connection.commit()
        """
        select_statement = select(shorten_url_table,
                                  shorten_url_table_stats).\
            join(shorten_url_table_stats, shorten_url_table.c.id==shorten_url_table_stats.c.shorten_url_id).\
                where(shorten_url_table.c.short_code == short_code)
        """
        select_stmt = text("""
            SELECT u.id,
                u.url,
                u.short_code,
                u.created_at,
                u.updated_at,
                s.access_count
            FROM shorten_urls u
            JOIN shorten_url_stats s ON u.id = s.shorten_url_id;

            """)
        shorten_object = connection.execute(select_stmt).first()

        response = shorten_object._asdict()
        

        return response, 200

if __name__ == '__main__':
    app.run('0.0.0.0', port=5001, debug=True)