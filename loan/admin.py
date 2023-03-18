from django.contrib import admin
from . import models


admin.site.register(models.UserProfile)
admin.site.register(models.Borrower)
admin.site.register(models.Investor)
admin.site.register(models.Loan)
admin.site.register(models.LoanProposal)
