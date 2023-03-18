from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register('register', views.UserProfileViewSet, basename='Register')

urlpatterns = [
        path('', include(router.urls)),

        path('Borrower/',views.sign_up_borrower,name='borrower-signup'),
        path('Investor/',views.sign_up_investor,name='investor-signup'),

        path('Place-loan/',views.place_loan,name='new_loan'),
        path('Available-loans/',views.get_loans,name='list_loans'),

        path('Propose/',views.place_proposal,name='place_proposals'),
        path('Get-proposal/',views.get_proposals,name='get_proposals'),
        path('Accept-proposal/',views.accept_proposal,name='proposal_accept'),

        path('Accepted-payment/',views.montly_payment,name='payment'),
]
