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
#CORS(app)  # This will enable CORS for all routes
CORS(app)

@app.route('/detect_ip_risk', methods=['GET', 'POST', 'OPTIONS'])
def your_function():
    if request.method == 'OPTIONS':
        # Handle preflight request
        return '', 200
    # Handle your logic here
    return 'Response from server'


def detect_ip_risk(buybox_data, sellerid_history, price_history):
    buybox_threshold = 0.2  # 20% change
    price_threshold = 0.3   # 30% change
    seller_change_threshold = 5  # 5 seller changes in a short period

    buybox_changes = np.diff(buybox_data) / buybox_data[:-1]
    significant_buybox_changes = np.abs(buybox_changes) > buybox_threshold

    price_changes = np.diff(price_history) / price_history[:-1]
    significant_price_changes = np.abs(price_changes) > price_threshold

    unique_sellers, seller_counts = np.unique(sellerid_history, return_counts=True)
    frequent_sellers = seller_counts > seller_change_threshold

    risk_factors = {
        'significant_buybox_changes': int(significant_buybox_changes.sum()),
        'significant_price_changes': int(significant_price_changes.sum()),
        'frequent_sellers': int(frequent_sellers.sum())
    }

    conditions_met = 0
    if risk_factors['significant_buybox_changes'] > 5:
        conditions_met += 1
    if risk_factors['frequent_sellers'] > 3:
        conditions_met += 1
    if risk_factors['significant_price_changes'] > 10:
        conditions_met += 1

    if conditions_met == 3:
        ip_risk = 'High'
    elif conditions_met == 2:
        ip_risk = 'Moderate'
    elif conditions_met == 1:
        ip_risk = 'Low'
    else:
        ip_risk = 'No'

    # ip_risk = any(value > 0 for value in risk_factors.values())
    
    return ip_risk, risk_factors


@app.route('/hello', methods=['GET'])
def hello():
    return 'Hello World'

# @app.route('/detect_ip_risk', methods=['POST'])
# def detect_ip_risk_endpoint():
#     asin = request.json.get('asin')
#     response = requests.get(API_URL.format(API_KEY, asin))
#     json_data = response.json()
#     data = json_data['products'][0]

#     if 'products' not in json_data or len(json_data['products']) == 0:
#         return jsonify({'error': 'No products found'}), 404

#     # Extract buybox data, sellerid history, and price history
#     buybox_data = data['csv'][0][::2]  # Every even index
#     sellerid_history = data['csv'][0][1::2]  # Every odd index
#     price_history = data['csv'][1][1::2]  # Every odd index

#     price_history = price_history[:len(buybox_data)]

#     df = pd.DataFrame({
#         "Buybox Data": buybox_data,
#         "Sellerid History": sellerid_history,
#         "Price History": price_history
#     })

#     buybox_data = df["Buybox Data"]
#     sellerid_history = df["Sellerid History"]
#     price_history = df["Price History"]

#     buybox_data = pd.Series(buybox_data).fillna(method='ffill').tolist()
#     sellerid_history = pd.Series(sellerid_history).replace(-1, np.nan).fillna(method='ffill').tolist()
#     price_history = pd.Series(price_history).replace(-1, np.nan).fillna(method='ffill').tolist()

#     ip_risk, risk_factors = detect_ip_risk(buybox_data, sellerid_history, price_history)

#     # if not ip_risk:
#     #     response_risk_factors = ['None']
#     # else:
#     #     response_risk_factors = [key for key, value in risk_factors.items() if value > 0]

#     return jsonify(ip_risk=ip_risk, risk_factors=risk_factors)


# def detect_castle_top_pattern(series, window=336):
#     pattern_detected = [0] * window  # Start with zeros to handle the window size at the beginning
#     for i in range(window, len(series) - window):
#         is_castle_top = all(series[j] > series[j - 1] and series[j] > series[j + 1] for j in range(i - window // 2, i + window // 2, 2))
#         pattern_detected.append(int(is_castle_top))
#     pattern_detected.extend([0] * (len(series) - len(pattern_detected)))  # Extend with zeros to match the DataFrame length exactly
#     return pattern_detected

# def detect_flat_lines(series, min_length=960, max_length=1440):
#     flat_line = [0] * len(series)
#     count = 0
#     for i in range(1, len(series)):
#         if series[i] == series[i-1]:
#             count += 1
#         else:
#             if min_length <= count <= max_length:
#                 for j in range(i - count, i):
#                     flat_line[j] = 1
#             count = 0
#     return flat_line

# @app.route('/detect_ip_risk', methods=['POST'])
# def analyze_data():
#     asin = request.json.get('asin')
#     response = requests.get(API_URL.format(API_KEY, asin))
#     keepa_data = response.json()

#     if 'products' not in keepa_data or len(keepa_data['products']) == 0:
#         return jsonify({'error': 'No products found'}), 404
#     # with open(file_path, 'r') as file:
#     #     keepa_data = json.load(file)

#     if 'products' in keepa_data and len(keepa_data['products']) > 0:
#         product_data = keepa_data['products'][0]
#         if 'csv' in product_data:
#             csv_data = product_data['csv']
#             if len(csv_data) > 3 and csv_data[3] is not None:
#                 offer_price_data = csv_data[3]
#             else:
#                 print("Offer price data is missing or not at the expected index.")
#                 return
#         else:
#             print("CSV data is missing from the product data.")
#             return
#     else:
#         print("Product data is missing from the response.")
#         return

#     base_date = datetime(2011, 1, 1)
#     offer_price_dates = [base_date + timedelta(minutes=30 * i) for i in range(0, len(offer_price_data), 2)]
#     offer_price_values = [offer_price_data[i] for i in range(1, len(offer_price_data), 2)]

#     df_prices = pd.DataFrame({
#         'Date': offer_price_dates,
#         'OfferPrice': offer_price_values
#     })

#     # Ignore anomalies where sellers come off the listing in under 6 hours
#     df_prices['IgnoreAnomaly'] = df_prices['Date'].diff().dt.total_seconds().fillna(0) <= 21600

#     # End additional logic

#     df_prices['CastleTopPattern'] = detect_castle_top_pattern(df_prices['OfferPrice'])
#     df_prices['FlatLine'] = detect_flat_lines(df_prices['OfferPrice'])
#     df_prices['Drop7Days'] = df_prices['OfferPrice'].diff(periods=-336)
#     df_prices['LargeDrop7Days'] = (df_prices['Drop7Days'] >= 4) & (df_prices['Drop7Days'] < 7)
#     df_prices['Drop2Days'] = df_prices['OfferPrice'].diff(periods=-96)
#     df_prices['LargeDrop2Days'] = df_prices['Drop2Days'] >= 4
#     df_prices['ExtraLargeDrop7Days'] = df_prices['Drop7Days'] >= 7
#     df_prices['ExtraLargeDrop2Days'] = df_prices['Drop2Days'] >= 7

#     df_prices['IsSeasonal'] = df_prices['Date'].apply(lambda x: x.month in [10, 11, 12])
#     df_prices['SeasonalDrop'] = df_prices['LargeDrop7Days'] & df_prices['IsSeasonal']
#     df_prices['NonSeasonalDrop'] = df_prices['LargeDrop7Days'] & ~df_prices['IsSeasonal']

#     risk_factors = []
#     total_score = assign_score(df_prices, product_data, risk_factors)
#     response = {
#         "risk_score": total_score,
#         "risk_factors": risk_factors
#     }

#     # with open('risk_analysis.json', 'w') as json_file:
#     #     json.dump(response, json_file, indent=4)

#     return jsonify(response)


# def assign_score(df, product_data, risk_factors):
#     scores = {
#         'large_drop_7days': 40 * (df['LargeDrop7Days'].sum() >= 5) + 30 * (2 <= df['LargeDrop7Days'].sum() <= 4) + 20 * (df['LargeDrop7Days'].sum() == 1),
#         'large_drop_2days': 45 * (df['LargeDrop2Days'].sum() >= 5) + 35 * (1 <= df['LargeDrop2Days'].sum() <= 4) + 25 * (df['LargeDrop2Days'].sum() == 1),
#         'extra_large_drop_7days': 55 * (1 <= df['ExtraLargeDrop7Days'].sum() <= 4) + 50 * (df['ExtraLargeDrop7Days'].sum() == 1),
#         'extra_large_drop_2days': 85 * (df['ExtraLargeDrop2Days'].sum() > 1) + 80 * (df['ExtraLargeDrop2Days'].sum() == 1),
#         'castle_top_pattern': 5 * (df['CastleTopPattern'].sum() > 0),
#         'single_buybox_winner': 50 if 'buyBoxWinner' in product_data and len(product_data['buyBoxWinner']) == 1 else 75 if 'buyBoxWinner' in product_data and len(product_data['buyBoxWinner']) > 1 else 0,
#         'fba_winner': 25 if 'fbaFulfilled' in product_data and 'isFba' in product_data and product_data['fbaFulfilled'] == 'YES' and product_data['isFba'] == 'YES' else 0,
#         'seasonal_or_nonseasonal_drop': 10 if df['NonSeasonalDrop'].sum() > 0 else -15 if df['SeasonalDrop'].sum() > 0 else 0,
#         'consistent_new_offer_count': 15 if df['FlatLine'].sum() == 1 else 20 if df['FlatLine'].sum() > 1 else 0,
#         'fairly_new_listing': -5 if (datetime.now() - df['Date'].min()).days < 200 else 0,
#         'very_new_listing': -10 if (datetime.now() - df['Date'].min()).days < 60 else 0,
#         'high_sales': -10 if df['OfferPrice'].max() > 100 else 0,
#         'very_high_sales': -15 if df['OfferPrice'].max() > 250 else 0,
#         'no_evidence_sales_suspicious': -25 if df['FlatLine'].sum() > 0 else 0,
#         'strong_listing_control': 5 if 'previous_year_signs' in product_data and product_data['previous_year_signs'] == 'strong' else 0,
#         'very_strong_listing_control': 10 if 'previous_year_signs' in product_data and product_data['previous_year_signs'] == 'very strong' else 0
#     }

#     labels = {
#         'large_drop_7days': 'low' if scores['large_drop_7days'] <= 20 else 'medium' if scores['large_drop_7days'] <= 30 else 'high',
#         'large_drop_2days': 'low' if scores['large_drop_2days'] <= 25 else 'medium' if scores['large_drop_2days'] <= 35 else 'high',
#         'extra_large_drop_7days': 'low' if scores['extra_large_drop_7days'] <= 50 else 'high',
#         'extra_large_drop_2days': 'low' if scores['extra_large_drop_2days'] <= 80 else 'high',
#         'castle_top_pattern': 'low' if scores['castle_top_pattern'] == 0 else 'high',
#         'single_buybox_winner': 'low' if scores['single_buybox_winner'] == 0 else 'high',
#         'fba_winner': 'low' if scores['fba_winner'] == 0 else 'high',
#         'seasonal_or_nonseasonal_drop': 'low' if scores['seasonal_or_nonseasonal_drop'] == -15 else 'medium' if scores['seasonal_or_nonseasonal_drop'] == 10 else 'high',
#         'consistent_new_offer_count': 'low' if scores['consistent_new_offer_count'] == 0 else 'medium' if scores['consistent_new_offer_count'] == 15 else 'high',
#         'fairly_new_listing': 'low' if scores['fairly_new_listing'] == 0 else 'high',
#         'very_new_listing': 'low' if scores['very_new_listing'] == 0 else 'high',
#         'high_sales': 'low' if scores['high_sales'] == 0 else 'high',
#         'very_high_sales': 'low' if scores['very_high_sales'] == 0 else 'high',
#         'no_evidence_sales_suspicious': 'low' if scores['no_evidence_sales_suspicious'] == 0 else 'high',
#         'strong_listing_control': 'low' if scores['strong_listing_control'] == 0 else 'high',
#         'very_strong_listing_control': 'low' if scores['very_strong_listing_control'] == 0 else 'high'
#     }

#     descriptions = {
#         'large_drop_7days': "A fairly significant drop in new offer count data",
#         'large_drop_2days': "A significant drop in new offer count data",
#         'extra_large_drop_7days': "A very significant drop in new offer count data",
#         'extra_large_drop_2days': "An extremely significant drop in new offer count data",
#         'castle_top_pattern': "Sellers coming on and off the listing in a steady and very frequent pattern",
#         'single_buybox_winner': "A seller appears on the listing twice",
#         'fba_winner': "One seller appears to have 100% of the BuyBox",
#         'seasonal_or_nonseasonal_drop': "Significant drops in new offer count have been made",
#         'consistent_new_offer_count': "Very consistent new offer count for a specified duration",
#         'fairly_new_listing': "This listing is fairly new which means data is less conclusive",
#         'very_new_listing': "This listing is very new which means data is less conclusive",
#         'high_sales': "Monthly sales appear high for this listing",
#         'very_high_sales': "Monthly sales appear very high for this listing",
#         'no_evidence_sales_suspicious': "When consistent new offer count events occur, there are no signs of solid sales",
#         'strong_listing_control': "Previous to the past year of sales there has been strong signs of listing control found in the data",
#         'very_strong_listing_control': "Previous to the past year of sales there has been very strong signs of listing control found in the data"
#     }

#     for key, value in scores.items():
#         if value != 0:
#             label = labels[key]
#             risk_factors.append({
#                 "factor": key.replace('_', ' ').capitalize(),
#                 "severity": label.capitalize(),
#                 "description": descriptions.get(key, "")
#             })

#     total_score = sum(value for value in scores.values() if value != 0)
#     return min(total_score, 95)


def detect_castle_top_pattern(series, window=4320):
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


@app.route('/detect_ip_risk', methods=['POST'])
def analyze_data():
    asin = request.json.get('asin')
    response = requests.get(os.getenv('API_URL').format(os.getenv('API_KEY'), asin))
    keepa_data = response.json()

    if 'products' not in keepa_data or len(keepa_data['products']) == 0:
        return {'error': 'No products found'}

    product_data = keepa_data['products'][0]
    if 'csv' in product_data:
        csv_data = product_data['csv']
        if len(csv_data) > 3 and csv_data[3] is not None:
            offer_price_data = csv_data[3]
        else:
            return {'error': 'Offer price data is missing or not at the expected index.'}
    else:
        return {'error': 'CSV data is missing from the product data.'}

    if len(offer_price_data) < 4320:
        return {
            "risk_score": 0,
            "risk_factors": [
                {
                    "description": 'Insufficient data for 90-day analysis'
                }
            ]
        }

    base_date = datetime(2011, 1, 1)
    offer_price_dates = [base_date + timedelta(minutes=30 * i) for i in range(0, len(offer_price_data), 2)]
    offer_price_values = [offer_price_data[i] for i in range(1, len(offer_price_data), 2)]

    df_prices = pd.DataFrame({
        'Date': offer_price_dates,
        'OfferPrice': offer_price_values
    })

    df_prices['IgnoreAnomaly'] = df_prices['Date'].diff().dt.total_seconds().fillna(0) <= 21600

    df_prices['CastleTopPattern'] = detect_castle_top_pattern(df_prices['OfferPrice'])
    df_prices['FlatLine'] = detect_flat_lines(df_prices['OfferPrice'])
    
    if len(df_prices) >= 4320:
        df_prices['Drop7Days'] = df_prices['OfferPrice'].diff(periods=-4320)
        df_prices['LargeDrop7Days'] = (df_prices['Drop7Days'] >= 4) & (df_prices['Drop7Days'] < 7)
        df_prices['ExtraLargeDrop7Days'] = df_prices['Drop7Days'] >= 7
    else:
        df_prices['Drop7Days'] = [0] * len(df_prices)
        df_prices['LargeDrop7Days'] = [0] * len(df_prices)
        df_prices['ExtraLargeDrop7Days'] = [0] * len(df_prices)

    if len(df_prices) >= 96:
        df_prices['Drop2Days'] = df_prices['OfferPrice'].diff(periods=-96)
        df_prices['LargeDrop2Days'] = df_prices['Drop2Days'] >= 4
        df_prices['ExtraLargeDrop2Days'] = df_prices['Drop2Days'] >= 7
    else:
        df_prices['Drop2Days'] = [0] * len(df_prices)
        df_prices['LargeDrop2Days'] = [0] * len(df_prices)
        df_prices['ExtraLargeDrop2Days'] = [0] * len(df_prices)

    df_prices['IsSeasonal'] = df_prices['Date'].apply(lambda x: x.month in [10, 11, 12])
    df_prices['SeasonalDrop'] = df_prices['LargeDrop7Days'] & df_prices['IsSeasonal']
    df_prices['NonSeasonalDrop'] = df_prices['LargeDrop7Days'] & ~df_prices['IsSeasonal']

    risk_factors = []
    total_score = assign_score(df_prices, product_data, risk_factors)
    response = {
        "risk_score": total_score,
        "risk_factors": risk_factors
    }

    return response

def assign_score(df, product_data, risk_factors):
    current_date = datetime.now()
    days_since_listing = (current_date - df['Date'].min()).days
    # Updated scores
    scores = {
        '1_large_quick_drop': 20 * (df['LargeDrop7Days'].sum() == 1),
        '2_4_large_quick_drops': 30 * (2 <= df['LargeDrop7Days'].sum() <= 4),
        '5_or_more_large_quick_drops': 40 * (df['LargeDrop7Days'].sum() >= 5),
        '1_large_very_quick_drop': 25 * (df['LargeDrop2Days'].sum() == 1),
        '1_4_large_very_quick_drops': 35 * (1 <= df['LargeDrop2Days'].sum() <= 4),
        '5_or_more_large_very_quick_drops': 45 * (df['LargeDrop2Days'].sum() >= 5),
        '1_extra_large_quick_drop': 50 * (df['ExtraLargeDrop7Days'].sum() == 1),
        '1_4_extra_large_quick_drops': 55 * (1 <= df['ExtraLargeDrop7Days'].sum() <= 4),
        '1_extra_large_very_quick_drop': 80 * (df['ExtraLargeDrop2Days'].sum() == 1),
        'more_than_1_extra_large_very_quick_drops': 85 * (df['ExtraLargeDrop2Days'].sum() > 1),
        'frequent_castle_top_pattern': 5 * (df['CastleTopPattern'].sum() == 1),
        'frequent_castle_top_pattern_more_than_once': 15 * (df['CastleTopPattern'].sum() > 1),
        'over_90_percent_castle_top_pattern': 50 * (df['CastleTopPattern'].sum() / len(df) > 0.9),
        'non_seasonal_drop': 10 * (df['NonSeasonalDrop'].sum() > 0),
        'seasonal_drop': -15 * (df['SeasonalDrop'].sum() > 0),
        'seasonal_and_non_seasonal_drops': 0,  # Not used
        'consistent_new_offer_count_20_30_days': 15 * (df['FlatLine'].sum() == 1),
        'consistent_new_offer_count_more_than_once_20_30_days': 20 * (df['FlatLine'].sum() > 1),
        'consistent_new_offer_count_extra_long': 25 * (df['FlatLine'].sum() >= 30),
        'consistent_new_offer_count_extra_long_less_than_1': 30 * (df['FlatLine'].sum() >= 30),
        'consistent_new_offer_count_super_long': 40 * (df['FlatLine'].sum() >= 150),
        'consistent_buybox_fba_3rd_party_20_30_days': 20 * (df['FlatLine'].sum() >= 20),
        'consistent_buybox_fba_3rd_party_20_30_days_less_than_1': 25 * (df['FlatLine'].sum() >= 20),
        'consistent_buybox_fba_3rd_party_extra_long': 30 * (df['FlatLine'].sum() >= 30),
        'consistent_buybox_fba_3rd_party_extra_long_less_than_1': 40 * (df['FlatLine'].sum() >= 30),
        'consistent_buybox_fba_3rd_party_super_long': 50 * (df['FlatLine'].sum() >= 150),
        'seller_featured_on_buybox_twice': 75 * ('buyBoxWinner' in product_data and len(product_data['buyBoxWinner']) == 2),
        'one_seller_100_percent_buybox': 50 * ('buyBoxWinner' in product_data and len(product_data['buyBoxWinner']) == 1),
        'previous_strong_listing_control_yes': 5 * ('listingControl' in product_data and product_data['listingControl'] == 'YES'),
        'previous_very_strong_listing_control_yes': 10 * ('listingControl' in product_data and product_data['listingControl'] == 'VERY STRONG'),
        'previous_strong_listing_control_no': -10 * ('listingControl' in product_data and product_data['listingControl'] == 'NO'),
    }

    new_listing_score = -10 if days_since_listing < 60 else (-5 if days_since_listing < 200 else 0)
    if new_listing_score != 0:
        if days_since_listing < 60:
            risk_factors.append({
                "factor": "Very new listing",
                "severity": "Medium",
                "description": "VERY new listing (under 60 days old)"
            })
        elif days_since_listing < 200:
            risk_factors.append({
                "factor": "Fairly new listing",
                "severity": "Low",
                "description": "Fairly new listing (under 200 days old)"
            })
    
    offer_price_max = df['OfferPrice'].max()
    high_sales_score = -10 if offer_price_max > 100 else 0
    very_high_sales_score = -15 if offer_price_max > 250 else 0
    
    if very_high_sales_score != 0:
        risk_factors.append({
            "factor": "Very high sales monthly",
            "severity": "High",
            "description": "Very High monthly sales (over 250)"
        })
    elif high_sales_score != 0:
        risk_factors.append({
            "factor": "High sales monthly",
            "severity": "Medium",
            "description": "High monthly sales (over 100)"
        })
    
    labels = {
        '1_large_quick_drop': 'Low',
        '2_4_large_quick_drops': 'Medium',
        '5_or_more_large_quick_drops': 'High',
        '1_large_very_quick_drop': 'Low',
        '1_4_large_very_quick_drops': 'Medium',
        '5_or_more_large_very_quick_drops': 'High',
        '1_extra_large_quick_drop': 'High',
        '1_4_extra_large_quick_drops': 'High',
        '1_extra_large_very_quick_drop': 'Very High',
        'more_than_1_extra_large_very_quick_drops': 'Very High',
        'frequent_castle_top_pattern': 'Low',
        'frequent_castle_top_pattern_more_than_once': 'Medium',
        'over_90_percent_castle_top_pattern': 'High',
        'non_seasonal_drop': 'Low',
        'seasonal_drop': 'Medium',
        'seasonal_and_non_seasonal_drops': 'N/A',
        'consistent_new_offer_count_20_30_days': 'Low',
        'consistent_new_offer_count_more_than_once_20_30_days': 'Medium',
        'consistent_new_offer_count_extra_long': 'High',
        'consistent_new_offer_count_extra_long_less_than_1': 'High',
        'consistent_new_offer_count_super_long': 'Very High',
        'consistent_buybox_fba_3rd_party_20_30_days': 'Low',
        'consistent_buybox_fba_3rd_party_20_30_days_less_than_1': 'Medium',
        'consistent_buybox_fba_3rd_party_extra_long': 'High',
        'consistent_buybox_fba_3rd_party_extra_long_less_than_1': 'High',
        'consistent_buybox_fba_3rd_party_super_long': 'Very High',
        'seller_featured_on_buybox_twice': 'Very High',
        'one_seller_100_percent_buybox': 'High',
        'high_sales_monthly': 'Medium',
        'very_high_sales_monthly': 'High',
        'no_evidence_sales_suspicious': 'Very High',
        'previous_strong_listing_control_yes': 'Low',
        'previous_very_strong_listing_control_yes': 'Medium',
        'previous_strong_listing_control_no': 'Medium',
    }

    descriptions = {
        '1_large_quick_drop': "One large quick drop (4-6 sellers in under 7 days)",
        '2_4_large_quick_drops': "2-4 large quick drops (4-6 sellers in under 7 days)",
        '5_or_more_large_quick_drops': "5 or more large quick drops (4-6 sellers in under 7 days)",
        '1_large_very_quick_drop': "One large very quick drop (4-6 sellers in under 2 days)",
        '1_4_large_very_quick_drops': "1-4 large very quick drops (4-6 sellers in under 2 days)",
        '5_or_more_large_very_quick_drops': "5 or more large very quick drops (4-6 sellers in under 2 days)",
        '1_extra_large_quick_drop': "One extra large quick drop (7 or more sellers in under 7 days)",
        '1_4_extra_large_quick_drops': "1-4 extra large quick drops (7 or more sellers in under 7 days)",
        '1_extra_large_very_quick_drop': "One extra large very quick drop (7 or more sellers in under 2 days)",
        'more_than_1_extra_large_very_quick_drops': "More than 1 extra large very quick drop (7 or more sellers in under 2 days)",
        'frequent_castle_top_pattern': "Frequent up and down patterns in new offer count (Castle Top Shape forming consistently for over 7 days)",
        'frequent_castle_top_pattern_more_than_once': "Frequent up and down patterns in new offer count (Castle Top Shape more than once)",
        'over_90_percent_castle_top_pattern': "Over 90% of the listing has up and down pattern in new offer count (Castle Top Shape)",
        'non_seasonal_drop': "Non Seasonal drops in new offer count (outside of seasonal peaks)",
        'seasonal_drop': "Seasonal drops in new offer count (inside seasonal peaks)",
        'seasonal_and_non_seasonal_drops': "Drops occurring both inside and outside seasonal periods",
        'consistent_new_offer_count_20_30_days': "Consistent new offer count (20-30 days)",
        'consistent_new_offer_count_more_than_once_20_30_days': "More than one occurrence of consistent new offer count (20-30 days)",
        'consistent_new_offer_count_extra_long': "Consistent new offer count (extra long, a month or more)",
        'consistent_new_offer_count_extra_long_less_than_1': "Consistent new offer count (extra long, a month or more) less than once",
        'consistent_new_offer_count_super_long': "Consistent new offer count (SUPER long, 5+ months)",
        'consistent_buybox_fba_3rd_party_20_30_days': "Consistent Buybox/FBA 3rd party offer price (20-30 days)",
        'consistent_buybox_fba_3rd_party_20_30_days_less_than_1': "Consistent Buybox/FBA 3rd party offer price (20-30 days) less than once",
        'consistent_buybox_fba_3rd_party_extra_long': "Consistent Buybox/FBA 3rd party offer price (extra long, 30+ days)",
        'consistent_buybox_fba_3rd_party_extra_long_less_than_1': "Consistent Buybox/FBA 3rd party offer price (extra long, 30+ days) less than once",
        'consistent_buybox_fba_3rd_party_super_long': "Consistent Buybox/FBA 3rd party offer price (SUPER long, 5+ months)",
        'very_new_listing': "VERY new listing (under 60 days old)",
        'fairly_new_listing': "Fairly new listing (under 200 days old)",
        'seller_featured_on_buybox_twice': "Seller currently featured on the BuyBox twice",
        'one_seller_100_percent_buybox': "One seller has 100% of the BuyBox",
        'high_sales_monthly': "High monthly sales (over 100)",
        'very_high_sales_monthly': "Very High monthly sales (over 250)",
        'no_evidence_sales_suspicious': "No evidence of sales while BuyBox and new offer count are suspiciously rigid",
        'previous_strong_listing_control_yes': "Previous strong signs of listing control (YES)",
        'previous_very_strong_listing_control_yes': "Previous very strong signs of listing control (YES)",
        'previous_strong_listing_control_no': "Previous strong signs of listing control (NO)",
    }

    for key, value in scores.items():
        if value != 0:
            label = labels[key]
            risk_factors.append({
                "factor": key.replace('_', ' ').capitalize(),
                "severity": label.capitalize(),
                "description": descriptions.get(key, "")
            })

    total_score = sum(value for value in scores.values() if value != 0)
    total_score += new_listing_score + (very_high_sales_score if very_high_sales_score != 0 else high_sales_score)

    return min(total_score, 95)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
