from django.urls import reverse
from .models import *
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework import status
import base64
from django.test import Client
import json


class BorrowerTests(APITestCase):


    urls={
            "signup":reverse("borrower-signup"),
            "newloan":reverse("new_loan"),
            "proposals":reverse("get_proposals"),
            "accept":reverse("proposal_accept"),
            "pay":reverse("payment"),
        }        
    def setUp(self):
        # Set up user
        self.user = UserProfile.objects.create_user(
            name='testuser',
            email='testdavid@test.com',
            password='testpass'
        )
        self.borrower=Borrower.objects.create(user=self.user)
        self.client = Client()
        credentials = f"{self.user.email}:testpass".encode('utf-8')
        auth_string = f"Basic {base64.b64encode(credentials).decode('utf-8')}"
        self.client.defaults['HTTP_AUTHORIZATION'] = auth_string
        # self.client.force_authenticate(user=self.user)


    def test_borrower_signup(self):
        response = self.client.get(self.urls["signup"],)
        print(response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_place_loan(self):
        data={
            'loan_period':24,
            'loan_amount':50000
        }
        response=self.client.post(path=self.urls["newloan"],data=json.dumps(data),content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_proposals(self):
        global proposals
        response = self.client.get(self.urls['proposals'])
        print(response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        
    def test_accept_proposal(self):
        data={
            'loan_id':1,
            'investor_id':1,
        }
        response = self.client.patch(self.urls['accept'],data=json.dumps(data),content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
 
    def test_montly_payment(self):
        data={
            'loan_id':'1',
        }
        response = self.client.patch(self.urls['pay'],data=json.dumps(data),content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        

class InvestorTests(APITestCase):


    urls={
            "signup":reverse("investor-signup"),
            "listloans":reverse("list_loans"),
            "placeproposal":reverse("place_proposals"),
        }        
    def setUp(self):
        # Set up user
        self.user = UserProfile.objects.create_user(
            name='testuser',
            email='testdavid@test.com',
            password='testpass'
        )
        self.borrower=Borrower.objects.create(user=self.user)
        self.client = Client()
        credentials = f"{self.user.email}:testpass".encode('utf-8')
        auth_string = f"Basic {base64.b64encode(credentials).decode('utf-8')}"
        self.client.defaults['HTTP_AUTHORIZATION'] = auth_string
        # self.client.force_authenticate(user=self.user)
    
    def test_investor_signup(self):
        balance={
            'balance':800000
        }
        response=self.client.post(self.urls['signup'],data=json.dumps(balance),content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_get_loans(self):

        response=self.client.get(self.urls['listloans'])
        print(response.content.decode())
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    
    def test_place_proposals(self):
        data={
            'loan_id':"1",
            'interest_rate':5,
        }
        response=self.client.post(self.urls['placeproposal'],data=json.dumps(data),content_type='application/json')
        print(response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
