from django.db import models
import datetime
from datetime import date
import os
import uuid
from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.hashers import make_password


# Create your models here.

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

    objects = AppUserManager()
    USERNAME_FIELD = 'email'

    def get_full_name(self):
        return '{}'.format(self.username)
