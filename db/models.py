from django.db import models
import datetime
from datetime import date
import os
import uuid
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.hashers import make_password

# Create your models here.
from django.utils.timezone import now


class AppUserManager(BaseUserManager):
    # date_of_birth, password=None):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """

        if not email:
            raise ValueError('Users must have an valid name')

        user = self.model(
            email=email,
            password=password
            # date_of_birth=date_of_birth,
            # date_of_birth=NULL,
        )

        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):  # date_of_birth, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """

        password = make_password(password, salt='lenmo')
        print(password)
        user = self.create_user(email=email,
                                password=password,
                                # date_of_birth=date_of_birth
                                # date_of_birth=NULL
                                )
        user.type = "ADMIN"
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    ACCOUNT_TYPE_ADMIN = "ADMIN"
    ACCOUNT_TYPE_BORROWER = "BORROWER"
    ACCOUNT_TYPE_INVESTOR = "INVESTOR"

    ACCOUNT_TYPE_LIST = ((ACCOUNT_TYPE_ADMIN, ACCOUNT_TYPE_ADMIN),
                         (ACCOUNT_TYPE_BORROWER, ACCOUNT_TYPE_BORROWER),
                         (ACCOUNT_TYPE_INVESTOR, ACCOUNT_TYPE_INVESTOR))

    MAIL_GENDER = "MALE"
    FEMALE_GENDER = "FEMALE"

    GENDER_LIST = ((MAIL_GENDER, MAIL_GENDER),
                   (FEMALE_GENDER, FEMALE_GENDER)
                   )

    def get_upload_to_img(self, filename):
        extension = os.path.splitext(filename)[1]
        datePart = date.today().strftime("/%Y/%d/%m/")
        result = 'users' + datePart + str(uuid.uuid4()) + extension
        return result

    class Meta:
        db_table = 'users'

    id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=255, unique=False)
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True, null=True,
                              default=None)
    password = models.CharField(max_length=255, null=False, blank=False)

    phone = models.CharField(max_length=15, unique=True, null=True, blank=True)
    type = models.CharField(max_length=15, choices=ACCOUNT_TYPE_LIST,
                            default=ACCOUNT_TYPE_BORROWER)
    gender = models.CharField(max_length=10, choices=GENDER_LIST,
                              default=MAIL_GENDER)
    balance = models.PositiveIntegerField(default=0, null=False, blank=True)
    objects = AppUserManager()
    USERNAME_FIELD = 'email'

    def get_full_name(self):
        return '{}'.format(self.username)


class Loan(models.Model):
    LOAN_STATUS_WAITING = "WAITING"
    LOAN_STATUS_FUNDED = "FUNDED"
    LOAN_STATUS_COMPLETED = "COMPLETED"

    LOAN_STATUS_LIST = ((LOAN_STATUS_FUNDED, LOAN_STATUS_FUNDED),
                        (LOAN_STATUS_COMPLETED, LOAN_STATUS_COMPLETED),
                        (LOAN_STATUS_WAITING, LOAN_STATUS_WAITING))

    class Meta:
        db_table = 'Loan'

    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField(auto_created=True, default=now, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    amount = models.PositiveIntegerField(default=0, null=False, blank=True)
    period = models.PositiveIntegerField(default=0, null=False, blank=True)
    status = models.CharField(max_length=15, choices=LOAN_STATUS_LIST,
                              default=LOAN_STATUS_WAITING)
    user = models.ForeignKey('User', on_delete=models.CASCADE)


class LoanPayments(models.Model):
    PAYMENT_STATUS_PAID = "PAID"
    PAYMENT_STATUS_NOT_PAID = "NOT PAID"

    PAYMENT_STATUS_LIST = ((PAYMENT_STATUS_PAID, PAYMENT_STATUS_PAID),
                           (PAYMENT_STATUS_NOT_PAID, PAYMENT_STATUS_NOT_PAID),
                           )

    class Meta:
        db_table = 'LoanPayments'

    id = models.BigAutoField(primary_key=True)
    amount = models.PositiveIntegerField(default=0, null=False, blank=True)
    due_date = models.DateTimeField(auto_created=True, default=now, blank=True)
    status = models.CharField(max_length=15, choices=PAYMENT_STATUS_LIST,
                              default=PAYMENT_STATUS_PAID)
    loan = models.ForeignKey('Loan', on_delete=models.CASCADE)


class Offer(models.Model):
    OFFER_STATUS_ACCEPTED = "ACCEPTED"
    OFFER_STATUS_NOT_ACCEPTED = "NOT ACCEPTED YET"

    OFFER_STATUS_LIST = ((OFFER_STATUS_ACCEPTED, OFFER_STATUS_ACCEPTED),
                         (OFFER_STATUS_NOT_ACCEPTED, OFFER_STATUS_NOT_ACCEPTED),
                         )

    class Meta:
        db_table = 'Offers'

    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField(auto_created=True, default=now, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    loan = models.ForeignKey('Loan', on_delete=models.CASCADE)
    interest_rate = models.PositiveIntegerField(default=0, null=False, blank=True)

    status = models.CharField(max_length=25, choices=OFFER_STATUS_LIST,
                              default=OFFER_STATUS_NOT_ACCEPTED)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
