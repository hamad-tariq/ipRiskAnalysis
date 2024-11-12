from flask import Flask, request, jsonify
import requests
import numpy as np
import pandas as pd
import json
from flask_cors import CORS
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

def configure():
    load_dotenv()

app = Flask(__name__)
# CORS(app)  # This will enable CORS for all routes
CORS(app)

API_KEY = '1o6o8o0bd5ko9o6o635rs85jqj0no7g1upls93u8tbtt83sdt5gak24m593s6967'
API_URL = 'https://api.keepa.com/product?key={}&domain=1&asin={}'

@app.route('/detect_ip_risk', methods=['GET', 'POST', 'OPTIONS'])
def your_function():
    if request.method == 'OPTIONS':
        # Handle preflight request
        return '', 200
    # Handle your logic here
    return 'Response from server'


def detect_castle_top_pattern(series, window=336):
    if len(series) < window:
        return [0] * len(series)
    pattern_detected = [0] * window
    for i in range(window, len(series) - window):
        is_castle_top = all(series[j] > series[j - 1] and series[j] > series[j + 1] for j in range(i - window // 2, i + window // 2, 2))
        pattern_detected.append(int(is_castle_top))
    pattern_detected.extend([0] * (len(series) - len(pattern_detected)))
    return pattern_detected


def detect_flat_lines(series, min_length=960, max_length=1440):
    if len(series) < min_length:
        return [0] * len(series)

    flat_line = [0] * len(series)
    count = 0
    for i in range(1, len(series)):
        if series[i] == series[i-1]:
            count += 1
        else:
            if min_length <= count <= max_length:
                for j in range(i - count, i):
                    flat_line[j] = 1
            count = 0
    return flat_line


@app.route('/analyze_data', methods=['POST'])
def analyze_data():
    asin = request.json.get('asin')
    if not asin:
        return jsonify({'error': 'ASIN is required'}), 400

    response = requests.get(API_URL.format(API_KEY, asin))
    if response.status_code != 200:
        return jsonify({'error': f"Failed to fetch data from Keepa API, status code: {response.status_code}"}), 500

    keepa_data = response.json()
    if 'products' not in keepa_data or len(keepa_data['products']) == 0:
        return jsonify({'error': 'No products found'}), 404

    product_data = keepa_data['products'][0]
    csv_data = product_data.get('csv', [])
    offer_price_data = csv_data[3] if len(csv_data) > 3 and csv_data[3] is not None else []

    if not offer_price_data:
        return jsonify({'error': 'Offer price data is missing or not at the expected index.'}), 400

    base_date = datetime(2011, 1, 1)
    offer_price_dates = [base_date + timedelta(minutes=30 * i) for i in range(0, len(offer_price_data), 2)]
    offer_price_values = [offer_price_data[i] for i in range(1, len(offer_price_data), 2)]

    df_prices = pd.DataFrame({
        'Date': offer_price_dates,
        'OfferPrice': offer_price_values
    })

    df_prices['CastleTopPattern'] = detect_castle_top_pattern(df_prices['OfferPrice'])
    df_prices['FlatLine'] = detect_flat_lines(df_prices['OfferPrice'])

    if len(df_prices) >= 336:
        df_prices['Drop7Days'] = df_prices['OfferPrice'].diff(periods=-336)
        df_prices['LargeDrop7Days'] = (df_prices['Drop7Days'] >= 4) & (df_prices['Drop7Days'] < 7)
        df_prices['ExtraLargeDrop7Days'] = df_prices['Drop7Days'] >= 7

    if len(df_prices) >= 96:
        df_prices['Drop2Days'] = df_prices['OfferPrice'].diff(periods=-96)
        df_prices['LargeDrop2Days'] = df_prices['Drop2Days'] >= 4
        df_prices['ExtraLargeDrop2Days'] = df_prices['Drop2Days'] >= 7

    df_prices['IsSeasonal'] = df_prices['Date'].apply(lambda x: x.month in [10, 11, 12])
    df_prices['SeasonalDrop'] = df_prices['LargeDrop7Days'] & df_prices['IsSeasonal']
    df_prices['NonSeasonalDrop'] = df_prices['LargeDrop7Days'] & ~df_prices['IsSeasonal']

    risk_factors = []
    total_score, individual_scores = assign_score(df_prices, product_data, risk_factors)
    response = {
        "total_score": int(total_score),
        "individual_scores": individual_scores,
        "risk_factors": risk_factors
    }

    return jsonify(response)


def assign_score(df, product_data, risk_factors):
    scores = {
        # Quick drop events
        'large_drop_7days': 20 if df['LargeDrop7Days'].sum() == 1 else 30 if 2 <= df['LargeDrop7Days'].sum() <= 4 else 40 if df['LargeDrop7Days'].sum() >= 5 else 0,
        'large_drop_2days': 25 if df['LargeDrop2Days'].sum() == 1 else 35 if 1 <= df['LargeDrop2Days'].sum() <= 4 else 45 if df['LargeDrop2Days'].sum() >= 5 else 0,
        'extra_large_drop_7days': 50 if df['ExtraLargeDrop7Days'].sum() == 1 else 55 if 1 <= df['ExtraLargeDrop7Days'].sum() <= 4 else 0,
        'extra_large_drop_2days': 80 if df['ExtraLargeDrop2Days'].sum() == 1 else 85 if df['ExtraLargeDrop2Days'].sum() > 1 else 0,

        # Castle Top Pattern events
        'castle_top_pattern_single': 5 if df['CastleTopPattern'].sum() > 0 else 0,
        'castle_top_pattern_multiple': 15 if df['CastleTopPattern'].sum() > 1 else 0,
        'castle_top_pattern_majority': 50 if df['CastleTopPattern'].sum() > 90 else 0,

        # Seasonal Drops
        'non_seasonal_drop': 10 if df['NonSeasonalDrop'].sum() > 0 else 0,
        'seasonal_drop': -15 if df['SeasonalDrop'].sum() > 0 else 0,

        # Consistent New Offer Count
        'consistent_new_offer_20_30_days': 15 if df['FlatLine'].sum() == 1 else 0,
        'consistent_new_offer_multiple': 20 if df['FlatLine'].sum() > 1 else 0,
        'consistent_new_offer_extra_long_single': 25 if df['FlatLine'].sum() > 30 else 0,
        'consistent_new_offer_extra_long_multiple': 30 if df['FlatLine'].sum() > 30 else 0,
        'consistent_new_offer_super_long': 40 if df['FlatLine'].sum() > 60 else 0,

        # Buybox consistency
        'consistent_buybox_20_30_days_single': 20 if 'buyBoxWinner' in product_data and len(product_data['buyBoxWinner']) == 1 else 0,
        'consistent_buybox_20_30_days_multiple': 25 if 'buyBoxWinner' in product_data and len(product_data['buyBoxWinner']) > 1 else 0,
        'consistent_buybox_extra_long_single': 30 if 'buyBoxWinner' in product_data and len(product_data['buyBoxWinner']) > 30 else 0,
        'consistent_buybox_extra_long_multiple': 40 if 'buyBoxWinner' in product_data and len(product_data['buyBoxWinner']) > 60 else 0,
        'consistent_buybox_super_long': 50 if 'buyBoxWinner' in product_data and len(product_data['buyBoxWinner']) > 90 else 0,

        # Listing age
        'new_listing': -5 if (datetime.now() - df['Date'].min()).days < 200 else 0,
        'very_new_listing': -10 if (datetime.now() - df['Date'].min()).days < 60 else 0,

        # Sales volume
        'high_sales': -10 if product_data.get('salesRank', 0) > 100 else 0,
        'very_high_sales': -15 if product_data.get('salesRank', 0) > 250 else 0,

        # Evidence of sales
        'no_evidence_sales_suspicious': -25 if df['FlatLine'].sum() > 0 and df['OfferPrice'].max() <= 100 else 0,

        # Listing control signs
        'strong_listing_control': 5 if product_data.get('previous_year_signs') == 'strong' else 0,
        'very_strong_listing_control': 10 if product_data.get('previous_year_signs') == 'very strong' else 0,
        'no_strong_listing_control': -10 if product_data.get('previous_year_signs') == 'no' else 0,

        # BuyBox control
        'buybox_double_feature': 75 if product_data.get('buyBoxWinnerCount', 0) > 1 else 0,
        'buybox_full_control': 50 if product_data.get('buyBoxWinnerFullControl', False) else 0,
    }

    descriptions = {
        'large_drop_7days': "A fairly significant drop in new offer count data",
        'large_drop_2days': "A significant drop in new offer count",
        'extra_large_drop_7days': "A very significant drop in new offer count in sales history for this item",
        'extra_large_drop_2days': "An extremely significant drop in new offer count",
        'castle_top_pattern_single': "Sellers coming on and off the listing in a steady and very frequent pattern",
        'castle_top_pattern_multiple': "Frequent occurrences of sellers coming on and off the listing in a steady and very frequent pattern",
        'castle_top_pattern_majority': "Most of the listing contains occurrences of sellers coming on and off the listing in a steady and very frequent pattern",
        'non_seasonal_drop': "Significant drops in new offer count have been made outside of seasonal peaks",
        'seasonal_drop': "Significant drops in new offer count have been made inside of seasonal sales peaks (Q4)",
        'consistent_new_offer_20_30_days': "Very consistent new offer count for 20+ days",
        'consistent_new_offer_multiple': "More than one instance of a consistent new offer count lasting 20+ days",
        'consistent_new_offer_extra_long_single': "Very consistent new offer count lasting over a month",
        'consistent_new_offer_extra_long_multiple': "More than one instance of a very consistent new offer count lasting over a month",
        'consistent_new_offer_super_long': "Extra long periods of very consistent new offer count shown",
        'consistent_buybox_20_30_days_single': "One instance of a fairly consistent buybox price shown",
        'consistent_buybox_20_30_days_multiple': "More than one instance of a fairly consistent buybox price",
        'consistent_buybox_extra_long_single': "One instance of a very consistent buybox price lasting longer than a month",
        'consistent_buybox_extra_long_multiple': "More than one instance of a very consistent buybox price lasting longer than a month",
        'consistent_buybox_super_long': "Extremely long periods of consistent buybox offer shown",
        'new_listing': "This listing is fairly new which means data is less conclusive",
        'very_new_listing': "This listing is very new which means data is less conclusive",
        'high_sales': "Monthly sales appear high which may lessen the risk factor",
        'very_high_sales': "Monthly sales appear very high which may lessen the risk factor",
        'no_evidence_sales_suspicious': "No solid sales evidence while BuyBox and new offer count are rigid",
        'strong_listing_control': "Strong signs of listing control in past year",
        'very_strong_listing_control': "Very strong signs of listing control in past year",
        'no_strong_listing_control': "No strong signs of listing control in past year",
        'buybox_double_feature': "A seller appears on the listing twice",
        'buybox_full_control': "One seller has 100% control of the BuyBox",
    }

    individual_scores = {key: val for key, val in scores.items() if val != 0}
    total_score = sum(individual_scores.values())
    total_score = max(total_score, 0)  # Ensure total score is not negative

    for key, value in individual_scores.items():
        risk_factors.append({
            "factor": key.replace('_', ' ').capitalize(),
            "severity": value,
            "description": descriptions[key]
        })

    return min(total_score, 95), individual_scores


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
