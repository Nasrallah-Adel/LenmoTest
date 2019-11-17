import datetime

from celery.schedules import crontab
from celery.task import periodic_task
from celery.utils.log import get_task_logger

from db.models import LoanPayments, Loan

logger = get_task_logger(__name__)


# celery -A LenmoTest worker -l info -B
# celery -A LenmoTest beat -l info

@periodic_task(run_every=(crontab(hour="*/24")), name="payment_task", ignore_result=True)
def payment_task():
    now = datetime.datetime.now()
    nowdelta = now + datetime.timedelta(days=2)
    now = now.strftime("%Y-%m-%d")
    nowdelta = nowdelta.strftime("%Y-%m-%d")
    payments = LoanPayments.objects.filter(due_date__exact=nowdelta, status=LoanPayments.PAYMENT_STATUS_NOT_PAID)
    for payment in payments:
        print("send email to borrower :  " +
              str(payment.loan.user.username) + " -- >" +
              str(payment.loan.user.email) +
              " --  You must Make Sure you have enough Money in your balance to pay back the loan payment and it will be " +
              str(payment.amount))
    payments = LoanPayments.objects.filter(due_date__lte=now, status=LoanPayments.PAYMENT_STATUS_NOT_PAID)
    for payment in payments:
        if payment.loan.user.balance >= payment.amount:
            borrower = payment.loan.user

            borrower.balance = borrower.balance - payment.amount
            borrower.save()
            investor = payment.offer.user
            investor.balance = investor.balance + payment.amount
            investor.save()

            print("send email to borrower :  " +
                  str(payment.loan.user.username) + " -- >" +
                  str(payment.loan.user.email) +
                  " --  The balance of : " +
                  str(payment.amount) +
                  " $  has been withdrawn to repay the loan payment")

            print("send email to investor :  " +
                  str(payment.offer.user.username) + " -- >" +
                  str(payment.offer.user.email) +
                  " --  Mr. " +
                  str(payment.loan.user.username) +
                  " has made the loan payment of " +
                  str(payment.amount) +
                  " $ , and its value has been added to your account ")
            payment.status = LoanPayments.PAYMENT_STATUS_PAID
            payment.save()
        else:
            print("send email to borrower " +
                  str(payment.loan.user.username) + " -- > " +
                  str(payment.loan.user.email) + " " +
                  "You do not have enough Money to pay your loan payment ")
    loans = Loan.objects.filter(status=Loan.LOAN_STATUS_FUNDED).values_list(
        'id')
    for loan in loans:
        print(loan[0])
        payments = LoanPayments.objects.filter(loan__id=loan[0])
        flag = True
        for payment in payments:
            if payment.status != LoanPayments.PAYMENT_STATUS_PAID:
                flag = False
                break
        if flag:
            loan = Loan.objects.get(id=loan[0])
            loan.status = Loan.LOAN_STATUS_COMPLETED
            loan.save()
