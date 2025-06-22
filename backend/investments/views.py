from rest_framework.decorators import api_view
from rest_framework.response import Response
import math
import yfinance as yf
import requests


@api_view(["POST"])
def calculate_investment(request):
    data = request.data
    initial = float(data["initial"])
    monthly = float(data["monthly"])
    years = int(data["years"])
    rate = float(data["rate"]) / 100
    inflation = float(data["inflation"]) / 100

    months = years * 12
    r_monthly = rate / 12
    r_real_monthly = ((1 + rate) / (1 + inflation)) ** (1/12) - 1

    # Nominal FV = compound principal + future value of a series
    nominal_fv = initial * ((1 + r_monthly) ** months) + \
                 monthly * (((1 + r_monthly) ** months - 1) / r_monthly)

    # Real FV = inflation-adjusted growth
    real_fv = initial * ((1 + r_real_monthly) ** months) + \
              monthly * (((1 + r_real_monthly) ** months - 1) / r_real_monthly)

    # Generate yearly breakdown (12 points)
    nominal_values = []
    real_values = []

    for year in range(1, years + 1):
        m = year * 12
        fv_nom = initial * ((1 + r_monthly) ** m) + monthly * (((1 + r_monthly) ** m - 1) / r_monthly)
        fv_real = initial * ((1 + r_real_monthly) ** m) + monthly * (((1 + r_real_monthly) ** m - 1) / r_real_monthly)
        nominal_values.append(round(fv_nom, 2))
        real_values.append(round(fv_real, 2))

    return Response({
        "nominal": round(nominal_fv, 2),
        "real": round(real_fv, 2),
        "yearly_values": [
            {"year": i + 1, "nominal": nominal_values[i], "real": real_values[i]}
            for i in range(years)
        ]
    })



@api_view(["GET"])
def buffet_analysis(request):

    ticker = request.GET.get("ticker", "").upper()
    if not ticker:
        return Response({"error": "Ticker is required"}, status=400)
    
    stock = yf.Ticker(ticker)
    info = stock.info

    try:
        roe = round(info["returnOnEquity"] * 100, 2)
        debt_equity = round(info["debtToEquity"], 2)
        pe_ratio = round(info["trailingPE"], 2)
        eps = info["trailingEps"]
        current_price = info["currentPrice"]
    except KeyError:
        return Response({"error": "Missing financial data"}, status=500)

    # Simple DCF: EPS * (1 + growth rate)^n * terminal multiple / (1 + discount rate)^n
    try:
        growth_rate = info.get("earningsQuarterlyGrowth", 0.1)
        discount_rate = 0.10  # Buffett often uses 10%
        terminal_multiple = 15  # Conservative assumption
        years = 10

        future_value = eps * ((1 + growth_rate) ** years) * terminal_multiple
        intrinsic_value = future_value / ((1 + discount_rate) ** years)
    except Exception:
        intrinsic_value = None

    return Response({
        "ticker": ticker,
        "price": current_price,
        "PE_ratio": pe_ratio,
        "ROE": roe,
        "Debt_to_Equity": debt_equity,
        "Intrinsic_Value_Estimate": round(intrinsic_value, 2) if intrinsic_value else "N/A"
    })