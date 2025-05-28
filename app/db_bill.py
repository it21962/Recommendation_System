import mysql.connector

def get_connection():
    print("Connecting to DB as root")
    return mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",
        password="Abcdefg2598bb4!",
        database="recommendations"
    )


import mysql.connector
from mysql.connector import IntegrityError

def insert_coupon(coupon):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT 1 FROM coupons WHERE coupon_id = %s", (coupon.coupon_id,))
    if cursor.fetchone():
        cursor.close()
        conn.close()
        return False

    query = '''
        INSERT INTO coupons (coupon_id, user_id, timestamp, stake, sport, league, company, selections)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    '''
    values = (
        coupon.coupon_id,
        coupon.user_id,
        coupon.timestamp,
        coupon.stake,
        coupon.sport,
        coupon.league,
        coupon.company,
        coupon.selections
    )
    cursor.execute(query, values)
    conn.commit()
    cursor.close()
    conn.close()
    return True


def insert_user(user):
    conn = get_connection()
    cursor = conn.cursor()

    table = f"{user.company.lower()}_users"
    cursor.execute(f"SELECT 1 FROM {table} WHERE user_id = %s", (user.user_id,))
    if cursor.fetchone():
        cursor.close()
        conn.close()
        return False

    query = f'''
        INSERT INTO {table} (user_id, name, birth_year, country, currency, gender, registration_date, company)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    '''
    values = (
        user.user_id, user.name, user.birth_year, user.country, user.currency,
        user.gender, user.registration_date, user.company
    )

    try:
        cursor.execute(query, values)
        conn.commit()
        return True
    except:
        return False
    finally:
        cursor.close()
        conn.close()


def insert_event(event):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT 1 FROM events WHERE event_id = %s", (event.event_id,))
    if cursor.fetchone():
        cursor.close()
        conn.close()
        return False

    query = """
        INSERT INTO events (event_id, sport, league, country, begin_timestamp, end_timestamp, participants, odds_home, odds_away)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = (
        event.event_id, event.sport, event.league, event.country,
        event.begin_timestamp, event.end_timestamp,
        event.participants, event.odds_home, event.odds_away
    )
    cursor.execute(query, values)
    conn.commit()
    cursor.close()
    conn.close()
    return True


def get_dynamic_recommendations(user_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # sport / league που παίζει ο χρήστης
    cursor.execute("""
        SELECT DISTINCT sport, league
        FROM coupons
        WHERE user_id = %s
    """, (user_id,))
    interests = cursor.fetchall()

    if not interests:
        cursor.close()
        conn.close()
        return []

    #Query για να βρούμε events με ίδιο sport και league
    recommendations = []
    for interest in interests:
        cursor.execute("""
            SELECT event_id, participants, odds_home, odds_away, begin_timestamp, end_timestamp
            FROM events
            WHERE sport = %s AND league = %s
        """, (interest['sport'], interest['league']))
        matched_events = cursor.fetchall()

        for event in matched_events:
            home, away = event["participants"].split(",")
            recommendations.append({
                "event_id": event["event_id"],
                "home_team": home.strip(),
                "away_team": away.strip(),
                "odds_home": event["odds_home"],
                "odds_away": event["odds_away"],
                "stake": 20.0,
                "user_id": user_id
            })

    cursor.close()
    conn.close()
    return recommendations

import json

def get_user_company(user_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    for table in ["novibet_users", "stoiximan_users"]:
        cursor.execute(f"SELECT company FROM {table} WHERE user_id = %s", (user_id,))
        result = cursor.fetchone()
        if result:
            cursor.close()
            conn.close()
            return result["company"]
    cursor.close()
    conn.close()
    return None

def get_display_config(company: str):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT config FROM company_configs WHERE company = %s", (company,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    if result:
        return json.loads(result["config"])
    return {}

def save_company_config(casino_id: int, config: dict):
    conn = get_connection()
    cursor = conn.cursor()

    config_str = json.dumps(config)

    # Αν υπάρχει ήδη, κάνε UPDATE, αλλιώς INSERT
    cursor.execute("SELECT 1 FROM company_configs WHERE id = %s", (casino_id,))
    exists = cursor.fetchone()

    if exists:
        cursor.execute("UPDATE company_configs SET config = %s WHERE id = %s", (config_str, casino_id))
    else:
        raise ValueError("Casino ID does not exist in company_configs")

    conn.commit()
    cursor.close()
    conn.close()

