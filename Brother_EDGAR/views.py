###############################################
# imports

# [get_object_or_404] is needed to use pk to find account data.
from django.shortcuts import render, redirect, get_object_or_404

# importing from our models.py and forms.py
from .models import Report
from .forms import ReportForm, UpdateReportForm

# imports needed for API
import requests
import json
import yfinance as yf

###############################################
# CRUD functionality

# Function to render our home page
def be_home(request):
    # accessing modelForm-> UpdateReportForm for dropdown effect.
    form = UpdateReportForm(data=request.POST or None)

    # Checks if request method is POST
    if request.method == 'POST':
        # If the form is submitted, retrieve which Report the user wants to view
        pk = request.POST['report'] # assigning pk as the tag to identify report's fk to Report model
        # upon selection confirmation redirect to display page with pk
        return redirect('../displayReport/' + str(pk))

    content = {'form': form}  # Saves content to the template as a dictionary
    # Initial load renders the page; adds content of form to page
    return render(request, 'Brother_EDGAR/BrotherEDGAR_home.html', content)


# Function to render the Create New Reports page when requested.
def be_create(request):
    # accessing modelForm --> Report model with all fields
    form = ReportForm(data=request.POST or None)

    # Checks if request method is POST
    if request.method == 'POST':
        # This is a user input, so we need to validate entry.
        if form.is_valid():  # check to see if the submitted form is valid and if so, saves the form
            form.save()  # Saves the location identified in BrotherEDGAR_create.html form section.
            # Returns user back to the home page after saving the entry
            return redirect('BrotherEDGAR_home')

    content = {'form': form}
    return render(request, 'Brother_EDGAR/BrotherEDGAR_create.html', content)


# Function to render the Display Report page when requested
def be_displayReport(request, pk):
    # Retrieve the requested report using its primary key
    report = get_object_or_404(Report, pk=pk)

    response = report.searchType  # set variable for search type

    # Checks if request method is POST --> 'view details' button
    if request.method == 'POST':
        # direct user to selected search method
        if response == "yahoo-Finance":
            return redirect('../yahooFinance/' + str(report.pk))
        elif response == "EDGAR-Search":
            return redirect('../searchPage/' + str(report.pk))

    # Pass report info to the template
    content = {'report': report}
    return render(request, 'Brother_EDGAR/BrotherEDGAR_displayReport.html', content)


# Function to render the Update Report page when requested
def be_updateReport(request, pk):
    item = get_object_or_404(Report, pk=pk)
    form = ReportForm(request.POST or None, instance=item)

    # User defined entry so we need to validate before saving
    if form.is_valid():
        form.save()
        return redirect('../displayReport/'+str(item.pk))  # Redirect back to display page after updates are made

    context = {'form': form}
    return render(request, 'Brother_EDGAR/BrotherEDGAR_updateReport.html', context)


# Function to handle delete report requests
def be_deleteReport(request, pk):
    report = get_object_or_404(Report, pk=pk)

    # Confirming delete choice
    if request.method == "POST":
        report.delete()  # Delete entry from dB
        return redirect('BrotherEDGAR_home')

    context = {'item': report}  # item is used to display report name in the page
    return render(request, 'Brother_EDGAR/BrotherEDGAR_deleteReport.html', context)


################################################
# API functionality

# For EDGAR search page
def be_searchPage(request, pk):
    item = get_object_or_404(Report, pk=pk)
    form = ReportForm(request.POST or None, instance=item)

    context = {'form': form}
    return render(request, 'Brother_EDGAR/BrotherEDGAR_searchPage.html', context)


# For Yahoo Finance page. Includes using API
def be_yahooFinance(request, pk):
    item = get_object_or_404(Report, pk=pk)
    form = ReportForm(request.POST or None, instance=item)
    # user input ticker symbol
    symbol = item.tickerSymbol

    # This commented out section was for yahoo Finance API using RapidAPI services
    # url = "https://yahoo-finance97.p.rapidapi.com/stock-info"
    # payload = "symbol={}".format(symbol)  # passes in the ticker symbol of desired report
    # headers = {
    #    "content-type": "application/x-www-form-urlencoded",
    #    "X-RapidAPI-Key": ".....",
    #    "X-RapidAPI-Host": "yahoo-finance97.p.rapidapi.com"
    # }

    # response = requests.request("POST", url, data=payload, headers=headers)

    # print('Json Response:', response.text)  # For dev use
    # parsing through the JSON response
    # api_info = json.loads(response.text)

    # Safeguarding against APIs vanishing. Check status/body before indexing nested keys
    # print('status:', response.status_code)
    # print('Json Response:', response.text)
    # if response.status_code != 200 or "data" not in api_info:
    #    return render(request, 'Brother_EDGAR/BrotherEDGAR_yahooFinance.html', {
    #        'form': form,
    #        'item': item,
    #        'error': api_info.get('message', 'Yahoo Finance data unavailable'),
    #    })

    # data = api_info["data"]

    # Pull quote data via yfinance (no RapidAPI key needed)
    ticker = yf.Ticker(symbol)
    data = ticker.info or {}

    print('yfinance keys sample:', list(data.keys())[:20]) # dev use while mapping

    if not data or not data.get("shortName"):
        return render(request, 'Brother_EDGAR/BrotherEDGAR_yahooFinance.html',{
            'form': form,
            'item': item,
            'error': 'Yahoo data unavailable for this ticker',
        })

    company_name = data.get("shortName", "")
    business_summary = data.get("longBusinessSummary") or data.get("description")
    averageVolume = data.get("averageVolume")
    # insider_confidence = data.get("heldPercentInsiders")
    # industry_confidence = data.get("heldPercentInstitutions")
    averageVolume10days = data.get("averageVolume10days") or data.get("averageDailyVolume10Day")
    fiftyDayAverage = data.get("fiftyDayAverage")
    dayHigh = data.get("dayHigh")
    dayLow = data.get("dayLow")
    # fullTimeEmployees = data.get("fullTimeEmployees")
    circulatingSupply = data.get("circulatingSupply")
    # debtToEquity = data.get("debtToEquity")
    # grossMargins = data.get("grossMargins")
    # grossProfits = data.get("grossProfits")
    regularMarketDayLow = data.get("regularMarketDayLow")
    regularMarketDayHigh = data.get("regularMarketDayHigh")
    regularMarketOpen = data.get("regularMarketOpen")
    ask = data.get("ask")
    askSize = data.get("askSize")

    context = {'form': form, "company_name": company_name, "business_summary": business_summary,\
            "averageVolume": averageVolume, "averageVolume10days": averageVolume10days, "fiftyDayAverage": fiftyDayAverage,\
            "dayHigh": dayHigh, "dayLow": dayLow, "circulatingSupply": circulatingSupply, "regularMarketDayLow": regularMarketDayLow,\
            "regularMarketDayHigh": regularMarketDayHigh, "regularMarketOpen": regularMarketOpen, "ask": ask, "askSize": askSize}
    return render(request, 'Brother_EDGAR/BrotherEDGAR_yahooFinance.html', context)
