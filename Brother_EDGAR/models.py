from django.db import models


# Creates the Report Model
class Report(models.Model):
    searchTypes = [('yahoo-Finance', 'yahoo-Finance'), ('EDGAR-Search', 'EDGAR-Search')]
    # fields
    report_name = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    searchType = models.CharField(max_length=15, choices=searchTypes)
    tickerSymbol = models.CharField(max_length=50, blank=False, null=False)
    CIK = models.CharField(max_length=10, blank=True, null=True)

    # Defines the model Manager for this class as Reports
    Reports = models.Manager()
    # Allows references to a specific report be returned as the report's name not as the primary key
    def __str__(self):
        return self.report_name


# Creates the updateReport model
class UpdateReport(models.Model):
    # {{form.report}} Links Report model to this model using FK. Also provides dropdown choice menu effect
    report = models.ForeignKey(Report, on_delete=models.CASCADE)

    # Defines the model Manager for Update Reports
    UpdateReports = models.Manager()
