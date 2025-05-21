import mysql.connector

def get_connection():
    print("🔍 Connecting to DB as root")
    return mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",
        password="Abcdefg2598bb4!",
        database="recommendations"
    )


def insert_coupon(coupon):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        INSERT INTO coupons (coupon_id, user_id, timestamp, stake, sport, league, company, selections)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            stake=VALUES(stake), sport=VALUES(sport), league=VALUES(league),
            company=VALUES(company), selections=VALUES(selections)
    """
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

def insert_user(user):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        INSERT INTO users (user_id, name, birth_year, country, currency, gender, registration_date, company)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            name=VALUES(name), birth_year=VALUES(birth_year), country=VALUES(country),
            currency=VALUES(currency), gender=VALUES(gender),
            registration_date=VALUES(registration_date), company=VALUES(company)
    """
    values = (
        user.user_id, user.name, user.birth_year, user.country, user.currency,
        user.gender, user.registration_date, user.company
    )
    cursor.execute(query, values)
    conn.commit()
    cursor.close()
    conn.close()

def insert_event(event):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        INSERT INTO events (event_id, sport, league, country, begin_timestamp, end_timestamp, participants, odds_home, odds_away)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            sport=VALUES(sport), league=VALUES(league), country=VALUES(country),
            begin_timestamp=VALUES(begin_timestamp), end_timestamp=VALUES(end_timestamp),
            participants=VALUES(participants), odds_home=VALUES(odds_home), odds_away=VALUES(odds_away)
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

def get_dynamic_recommendations(user_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Βρες τα sport/league που παίζει ο χρήστης
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

    #Query για να βρούμε events με ίδιο sport+league
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
