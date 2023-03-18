# from django.test import TestCase, Client
# from django.urls import reverse
# from rest_framework import status,HTTP_HEADER_ENCODING
# from rest_framework.test import APIClient
# import base64
# from .models import UserProfile




# class InvestorTestCase(TestCase):
#     """Handling tests from borrower side"""
    
#     def setUp(self):
#         self.url = {
#             "investor-signup": reverse("investor-signup"),
#             "list_loans": reverse("list_loans"),
#             "place_proposals": reverse("place_proposals"),
#         }
#         user=UserProfile.objects.create(email='mainInvestor@main.com')
#         user.set_password('12345')
#         user.save()


#     def test_signup_investor(self):
#         print(self.client.login(email='mainInvestor@main.com', password='12345'))
#         print(self.client.get(self.url['investor-signup']))
        

#     # def test_list_loan(self):
#     #     print(self.client.login(email='mainInvestor@main.com', password='12345'))
#     #     response=self.client.get(self.url['list_loans'])
#     #     print(response)


# class BorrowerTestCase(TestCase):
#     """Handling tests from Investor side"""

#     def setUp(self):
#         self.url = {
#             "borrower-signup": reverse("borrower-signup"),
#             "new_loan": reverse("new_loan"),
#             "get_proposals": reverse("get_proposals"),
#             "proposal_accept": reverse("proposal_accept"),
#             "payment": reverse("payment"),
#         }
