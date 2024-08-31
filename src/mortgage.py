from __future__ import division
from datetime import date

P0 = 417000  # dollar initial principal amount

r = 3.625 # percentage interest per annum

period = 360   # number of months to pay off loan

r_pm = r / 12   # monthly interest rate

start_date = date(2012, 9, 1)   # time when we started making payments

today = date.today()

num_payments_sofar = (today.year - start_date.year)*12 + (today.month - start_date.month)

freq = 1  # number of times per month payment made

payment = 1901.73/freq  # amount payed per period

# every so many months, make an extra payment
extra_payment_freq = 6

# you pay this much times the normal amount every `extra_payment_freq`
# months. Thus a value of 2 means you make 1 extra payment every so many
# months. Leave at 1 if you wish to NOT make extra payments.
extra_payment_ratio = 1

interest_per_payment = r/100/12/freq
P = P0
total_interest = 0
total_payment = 0
num_payments = 0

while P > 0:
    interest = P*interest_per_payment
    total_interest += interest

    if (num_payments + 1) % extra_payment_freq == 0:
        this_payment = extra_payment_ratio*payment
    else:
        this_payment = payment

    total_payment += this_payment
    P = P + interest - this_payment

    if P*(1 + interest_per_payment) < payment:
        total_payment += P
        P = 0

    num_payments += 1

    if num_payments == num_payments_sofar:
        print '****** Current status *****'
        print 'Total payment:', total_payment
        print 'Total interest:', total_interest
        print 'Remaining principal', P

    # if num_payments % 12 == 0:
    #     print '==== Year %g ====' % (num_payments/12) 
    #     print 'Total payment:', total_payment
    #     print 'Total interest:', total_interest
    #     print 'Remaining principal', P

print '==== Final tally ==='
print 'Total payment:', total_payment
print 'Total interest:', total_interest
print 'Total number of payments (%g years, %g months)' % (num_payments // 12, num_payments % 12)
print 'Remaining principal', P

# Total payment: 247224.9
# Total interest: 132027.629673
# Total number of payments 120
# Remaining principal 301802.729673
