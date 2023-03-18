from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, BaseUserManager
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError


class UserProfileManager(BaseUserManager):
    """manager for user profiles"""

    def create_user(self, email, name, password=None):
        """create a new user profile"""
        if not email:
            raise ValueError("User must choose Email Address")
        email = self.normalize_email(email)
        user = self.model(email=email, name=name)
        user.set_password(password)
        user.save(using=self._db)

        return user

    # we need super user to have password
    def create_superuser(self, email, name, password):
        """create and save a new super user with given details"""
        user = self.create_user(email, name, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """database model for users in the system """
    email = models.EmailField(max_length=225, unique=True)
    name = models.CharField(max_length=255)
    is_activate = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = UserProfileManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        """return string represent of our user"""
        return self.email


class Borrower(models.Model):
    """Handling the borrwer model"""
    user = models.OneToOneField(
        UserProfile,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    def __str__(self):
        return self.user.name


class Investor(models.Model):
    """Handling the insvestor model"""
    user = models.OneToOneField(
        UserProfile,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    balance = models.FloatField()

    def __str__(self):
        return self.user.name


class Loan(models.Model):
    """Handling the loan model"""

    borrower = models.ForeignKey(Borrower, on_delete=models.CASCADE)

    investor = models.ForeignKey(Investor, null=True, on_delete=models.CASCADE)
    interest_rate = models.DecimalField(null=True, max_digits=5, decimal_places=2, validators=[
                                        MinValueValidator(0), MaxValueValidator(100)])

    loan_amount = models.IntegerField(validators=[MinValueValidator(0)])
    loan_period = models.IntegerField(validators=[MinValueValidator(1)])
    paid_months = models.IntegerField(
        default=0, validators=[MinValueValidator(0)])

    starting_date = models.DateTimeField(
        null=True, auto_now=False, auto_now_add=False)

    loan_status = (('Under review', 'Under review'),
                   ('Funded', 'Funded'), ('Completed', 'Completed'))

    status = models.CharField(
        max_length=100, choices=loan_status, default='Under review')

    def __str__(self):
        return "%s requests " % (self.borrower.user.name)


class LoanProposal(models.Model):
    """Handling the requests for the loan"""
    borrower = models.ForeignKey(Borrower, on_delete=models.CASCADE)
    loan = models.ForeignKey(Loan, null=True, on_delete=models.CASCADE)
    investor = models.ForeignKey(Investor, on_delete=models.CASCADE)
    interest_rate = models.DecimalField(null=True, max_digits=5, decimal_places=2, validators=[
                                        MinValueValidator(0), MaxValueValidator(100)])
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return "%s" % (self.investor.user.name)
