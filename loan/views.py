from django.shortcuts import render
from rest_framework import viewsets
from . import serializers
from . import models
from rest_framework.authentication import TokenAuthentication
from rest_framework.authentication import BasicAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
import json
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
import datetime

LEANME_FEE=3.00


class UserProfileViewSet(viewsets.ModelViewSet):
    """handle creating and updating profiles """
    serializer_class = serializers.UserProfileSerializer
    search_fields = ('name', 'email',)

    def get_queryset(self):
        pass


@api_view(['POST','GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([BasicAuthentication])
def sign_up_borrower(request):
    """Handling signing up as borrower"""
    models.Borrower.objects.get_or_create(user=request.user)
    return Response({'Message':'You signed up as borrower, thanks!'})

@api_view(['POST','GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([BasicAuthentication])
def sign_up_investor(request):
    """Handling signing up as investor"""
    data = json.loads(request.body)
    models.Investor.objects.get_or_create(user=request.user,balance=data['balance'])
    return Response({'Message':'You signed up as Investor, thanks!'})



@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([BasicAuthentication])
def place_loan(request):
    """Handling place a loan to investors"""
    data = json.loads(request.body)
    borrower=models.Borrower.objects.get(user=request.user)
    models.Loan.objects.get_or_create(borrower=borrower,loan_amount=data['loan_amount'],loan_period=data['loan_period'])
    return Response({'Message': 'Done!'}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([BasicAuthentication])
def get_loans(request):
    """Handling place a loan to investors"""
    loans=models.Loan.objects.all().values('id','loan_period','loan_amount').filter(investor_id=None)
    return Response(loans)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([BasicAuthentication])
def place_proposal(request):
    """Handling sending request to the borrower"""
    data = json.loads(request.body)
    investor=models.Investor.objects.get(user=request.user)
    loan_amount=models.Loan.objects.values('loan_amount').filter(id=data['loan_id'])[0]
    investor_balance=investor.balance
    total_amount=loan_amount['loan_amount']+LEANME_FEE

    if total_amount<=investor_balance:
            loan=models.Loan.objects.filter(id=data['loan_id'])[0]
            borrower=models.Borrower.objects.filter(user=loan.borrower)[0]
            models.LoanProposal.objects.get_or_create(loan=loan,investor=investor,borrower=borrower,interest_rate=data['interest_rate'])
            return Response({'Message': 'Proposal sent!'}, status=status.HTTP_200_OK)
    else:
        return Response({'Message': 'You don\'t have the required balance'}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([BasicAuthentication])
def get_proposals(request):
    """Handling place a loan to investors"""
    borrower=models.Borrower.objects.get(user=request.user) 
    loan_proposal=models.LoanProposal.objects.values('interest_rate','accepted','loan_id','investor_id').filter(borrower=borrower)
    return Response(loan_proposal)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
@authentication_classes([BasicAuthentication])
def accept_proposal(request):
    """Handling place a loan to investors"""
    data = json.loads(request.body)
    loan_proposal=models.LoanProposal.objects.filter(loan=data['loan_id'],investor=data['investor_id'])
    loan_proposal.update(accepted=True)
    models.LoanProposal.objects.filter(loan=data['loan_id'],accepted=False).delete()
    loan_proposal_values=loan_proposal.values('loan_id','investor_id','interest_rate')[0]
    models.Loan.objects.filter(id=int(data['loan_id'])).update(interest_rate=loan_proposal_values['interest_rate'],status='Funded',investor=loan_proposal_values['investor_id'],starting_date=datetime.datetime.now())
    return Response({'Message':'Proposal Accepted!'})


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
@authentication_classes([BasicAuthentication])
def montly_payment(request):
    """Handling place a loan to investors"""
    data = json.loads(request.body)
    loan=models.Loan.objects.filter(id=data['loan_id'])
    print(loan)
    loan_values=loan.values('paid_months','loan_period')[0]
    print(loan_values)
    if loan_values['paid_months']<loan_values['loan_period']:
        loan.update(paid_months=loan_values['paid_months']+1)
        return Response({'Message':f"You paid{loan_values['paid_months']+1} month. You have {loan_values['loan_period']-loan_values['paid_months']-1} months to go"})

    elif loan_values['paid_months']==loan_values['loan_period']:
        loan.update(status='Completed')
        return Response({'Message':'Thanks for using Lenme! All of your payments done successfully!'})
    
    else:
        return Response({'Message':'You don\'t need to pay anything'})


