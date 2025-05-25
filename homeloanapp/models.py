from django.db import models
import math

# Choice Constants
SEX_CHOICES = [
    ("Male", "Male"),
    ("Female", "Female")
]

MARTIAL_STATUS = [
    ("Married", "Married"),
    ("Unmarried", "Unmarried")
]

COLLATERAL_AREA = [
    ("Main Business Area", "Main Business Area"),
    ("Simple Business Area", "Simple Business Area"),
    ("Dense/Main Residential Area", "Dense/Main Residential Area"),
    ("Simple Residential Area", "Simple Residential Area"),
    ("Other Area", "Other Area")
]

EDUCATION_CHOICES = [
    ("Master", "Master"),
    ("Bachelor", "Bachelor"),
    ("+2", "+2"),
    ("slc", "slc")
]

INCOME_TYPE = [
    ("upto loan tenure permanent income", "Upto loan tenure permanent income"),
    ("upto near loan tenure permanent income", "Upto near loan tenure permanent income"),
    ("upto half of the loan tenure", "Upto half of the loan tenure"),
    ("probability of upto half of the loan tenure", "Probability of upto half of the loan tenure"),
    ("other", "Other")
]

CLIENT_DIS = [
    ("Less than 2km", "Less than 2km"),
    ("2km to 5km", "2km to 5km"),
    ("5km to 10km", "5km to 10km"),
    ("10km to 15km", "10km to 15km"),
    ("More than 15km", "More than 15km")
]

BANKING_YEARS = [
    ("more than 5 years", "More than 5 years"),
    ("(4-5)years", "(4-5) years"),
    ("(3-4)years", "(3-4) years"),
    ("(1-3)years", "(1-3) years"),
    ("less than 1 year", "Less than 1 year")
]

CREDIT_HISTORY = [
    ("payment after full rebate", "Payment after full rebate"),
    ("payment after 50 percent rebate", "Payment after 50 percent rebate"),
    ("no banking transactions", "No banking transactions"),
    ("payment period less than 3 months", "Payment period less than 3 months"),
    ("payment period more than 3 months", "Payment period more than 3 months"),
    ("payment period more than 6 months", "Payment period more than 6 months")
]

CREDIT_SIFARIS = [
    ("Excellent", "Excellent"),
    ("Very Good", "Very Good"),
    ("Simple", "Simple"),
    ("Weak", "Weak"),
    ("Risky", "Risky")
]

BUSINESSTYPES = [
    ("Agriculture", "Agriculture"),
    ("Medical", "Medical"),
    ("Petroleum", "Petroleum"),
    ("Retail", "Retail"),
    ("Liquors & Drinks", "Liquors & Drinks"),
    ("Hardware", "Hardware"), ("None","None")
]

class ClientDetails(models.Model):
    # Personal Information
    name = models.CharField(max_length=300, default='Sumam limbu')
    dob = models.CharField(max_length=10, default='2008/10/10')
    citizenship = models.CharField(max_length=20, default='1234')
    sex = models.CharField(max_length=8, choices=SEX_CHOICES, default="Male")
    martial = models.CharField(max_length=20, choices=MARTIAL_STATUS, default="Married")
    father = models.CharField(max_length=300, default="shyam rai")
    education = models.CharField(max_length=10, choices=EDUCATION_CHOICES, default="Bachelor")
    address = models.CharField(max_length=50, default='Itahari')
    dependent = models.PositiveIntegerField(default=3)
    
    # Employment Section
    employer = models.CharField(max_length=150, blank=True, null=True, default='rbbl')
    position = models.CharField(max_length=150, blank=True, null=True, default='Assistant')
    service_time = models.PositiveIntegerField(blank=True, null=True, default=5)
    
    # Business Section
    firm_name = models.CharField(max_length=150, blank=True, null=True, default='rbbl')
    business_type = models.CharField(
        max_length=150, 
        choices=BUSINESSTYPES, 
        default="Agriculture", 
        blank=True, 
        null=True
    )
    pan_no = models.PositiveIntegerField(blank=True, null=True, default='12345')
    firm_address = models.CharField(max_length=150, blank=True, null=True, default='Itahari-20')
   
    # Income Section
    salary = models.FloatField(default=0.0)
    business_income = models.FloatField(default=0.0)
    agriculture = models.FloatField(default=0.0)
    house_rent = models.FloatField(default=0.0)
    family_income = models.FloatField(default=0.0)
    other_income = models.FloatField(default=0.0)
   
    # Loan Application
    loan_amount = models.PositiveIntegerField()
    tenure = models.PositiveIntegerField(default=10)
    interest = models.FloatField(default=10.12)
    loan_type = models.CharField(max_length=50, default='Home')
    
    # Collateral Section
    plot_no = models.CharField(max_length=50, default='5684')
    plot_area = models.CharField(max_length=50, default='0-0-10-0')
    plot_address = models.CharField(max_length=200, blank=True, null=True, default='Itahari-20')
    plot_owner = models.CharField(max_length=150, default='Roshan Rai')
    plot_value = models.FloatField(default=4632450)
    home_value = models.FloatField(default=0.0)
    plot_market_value = models.FloatField(blank=True, null=True, default=200000)

    # Other Property
    land_value = models.PositiveIntegerField(default=0)
    buildingvalue = models.PositiveIntegerField(default=0)
    family_property = models.PositiveIntegerField(default=0)
    vehicle = models.FloatField(default=0.0)
    
    # Credit Score 
    collateral_place = models.CharField(
        max_length=60, 
        choices=COLLATERAL_AREA, 
        default="Main Business Area"
    )
    income_tenure = models.CharField(
        max_length=200,
        choices=INCOME_TYPE,
        default="upto loan tenure permanent income"
    )
    client_distance = models.CharField(
        max_length=200, 
        choices=CLIENT_DIS, 
        default="Less than 2km"
    )
    banking_history = models.CharField(
        max_length=100,
        choices=CREDIT_HISTORY,
        default="payment after full rebate",
        null=True
    )
    banking_year = models.CharField(
        max_length=100,
        choices=BANKING_YEARS,
        default="more than 5 years"
    )
    loan_committee = models.CharField(
        max_length=20,
        choices=CREDIT_SIFARIS,
        default="Excellent"
    ) 
    loan_status = models.CharField(
        max_length=20,
        default="preview",
        null=True,
        blank=True
    ) 
    
    def __str__(self):
        return self.name
    
    # Financial Calculations
    @property
    def yearly_income(self):
        return sum([
            self.salary,
            self.business_income,
            self.agriculture,
            self.house_rent,
            self.family_income
        ])

    @property
    def monthly_income(self):
        return round(self.yearly_income,2)

    @property
    def actual_loan_amt(self):
        return (self.home_value * 70) / 100

    @property
    def selfinvest(self):
        return self.home_value - self.actual_loan_amt

    @property
    def tot_coll(self):
        return self.plot_value + self.home_value

    @property
    def monthly_saving(self):
        return round(self.monthly_income / 2, 2)

    @property
    def emi(self):
        principal = self.loan_amount
        monthly_rate = self.interest / 1200
        months = self.tenure * 12
        
        if monthly_rate == 0:  # Handle interest-free loans
            return principal / months
        
        return int(
            (principal * monthly_rate * (1 + monthly_rate)**months) / 
            ((1 + monthly_rate)**months - 1)
        )
           
    @property
    def loan_to_coll(self):
        try:
            return round((self.loan_amount / self.tot_coll) * 100, 2)
        except ZeroDivisionError:
            return 0

    @property
    def loan_to_invest(self):
        try:
            return round((self.actual_loan_amt / self.home_value) * 100, 2)
        except ZeroDivisionError:
            return 0
        
    @property
    def kista_to_income(self):
        try:
            return round((self.emi / self.monthly_income) * 100, 2)
        except ZeroDivisionError:
            return 0
    
    # Credit Score Calculations
    @property
    def p1(self):
        try:
            ratio = (self.plot_market_value + self.home_value) / self.actual_loan_amt
            if ratio < 1.5: return 5
            if ratio < 2: return 4
            if ratio < 2.5: return 3
            if ratio < 3: return 2
            return 1
        except ZeroDivisionError:
            return 5
    
    @property
    def p1_weight(self):
        return 0.2 * self.p1
         
    @property
    def p2(self):
        mapping = {
            "Main Business Area": 1,
            "Simple Business Area": 2,
            "Dense/Main Residential Area": 3,
            "Simple Residential Area": 4
        }
        return mapping.get(self.collateral_place, 5)
    
    @property
    def p2_weight(self):
        return round(self.p2 * 0.1, 1)
        
    @property
    def p3(self):
        try:
            total_assets = sum([
                self.plot_market_value,
                self.land_value,
                self.buildingvalue,
                self.family_property,
                self.vehicle
            ])
            ratio = total_assets / self.actual_loan_amt
            
            if ratio < 3: return 5
            if ratio <= 3.5: return 4
            if ratio <= 4: return 3
            if ratio <= 5: return 2
            return 1
        except ZeroDivisionError:
            return 5
        
    @property
    def p3_weight(self):
        return 0.1 * self.p3    
        
    @property
    def p4(self):
        try:
            ratio = self.actual_loan_amt / self.monthly_income
            if ratio < 1.5: return 5
            if ratio < 2: return 4
            if ratio < 2.5: return 3
            if ratio < 3: return 2
            return 1
        except ZeroDivisionError:
            return 5
    
    @property
    def p4_weight(self):
        return self.p4 * 0.2
       
    @property
    def p5(self):
        mapping = {
            "upto loan tenure permanent income": 1,
            "upto near loan tenure permanent income": 2,
            "upto half of the loan tenure": 3,
            "probability of upto half of the loan tenure": 4
        }
        return mapping.get(self.income_tenure, 5)
   
    @property
    def p5_weight(self):
        return self.p5 * 0.1
       
    @property
    def p6(self):
        mapping = {
            "Less than 2km": 1,
            "2km to 5km": 2,
            "5km to 10km": 3,
            "10km to 15km": 4
        }
        return mapping.get(self.client_distance, 5)
    
    @property
    def p6_wt(self):
        return self.p6 * 0.05  
        
    @property
    def p7(self):
        mapping = {
            "payment after full rebate": 1,
            "payment after 50 percent rebate": 2,
            "no banking transactions": 3,
            "payment period less than 3 months": 4,
            "payment period more than 3 months": 5
        }
        return mapping.get(self.banking_history, 6)
    
    @property
    def p7_wt(self):
        return round(self.p7 * 0.05,2)     
    
    @property
    def p8(self):
        mapping = {
            "more than 5 years": 1,
            "(4-5)years": 2,
            "(3-4)years": 3,
            "(1-3)years": 4
        }
        return mapping.get(self.banking_year, 5)
          
    @property
    def p8_wt(self):
        return round(self.p8 * 0.05,2)      
    
    @property
    def p9(self):
        mapping = {
            "Excellent": 1,
            "Very Good": 2,
            "Simple": 3,
            "Weak": 4
        }
        return mapping.get(self.loan_committee, 5)
    
    @property
    def p9_wt(self):
        return round(self.p9 * 0.15, 2)
    
    @property
    def total_score(self):
        return round(sum([
            self.p1_weight,
            self.p2_weight,
            self.p3_weight,
            self.p4_weight,
            self.p5_weight,
            self.p6_wt,
            self.p7_wt,
            self.p8_wt,
            self.p9_wt
        ]), 2)
        
    @property
    def credit_result(self):
        score = self.total_score
        if score <= 1.5: return "Very Good"
        if score <= 2.5: return "Good"
        if score <= 3: return "ok"
        if score <= 3.5: return "To be Sub-standard"
        if score <= 4.5: return "Sub-Standard"
        return "Bad"


# Loan Disbursement Model
class LoanDisbursement(models.Model):
    LOAN_DISBURSE_STATUS = [
        ('Disbursed', 'Disbursed'),
        ('Not Disbursed', 'Not Disbursed'),
    ]
    
    client = models.OneToOneField(
        ClientDetails, 
        on_delete=models.CASCADE,
        related_name='disbursement'
    )
    account_no = models.CharField(max_length=20, unique=True)
    disbursement_date = models.DateField()
    disbursement_status = models.CharField(
        max_length=15, 
        choices=LOAN_DISBURSE_STATUS, 
        default='Not Disbursed'
    )
    
    def __str__(self):
        return f"Disbursement for {self.client.name} (Account: {self.account_no})"


# Loan Settlement Model
class LoanSettlement(models.Model):
    SETTLEMENT_STATUS = [
        ('Active', 'Active'),
        ('Closed', 'Closed'),
    ]
    
    client = models.OneToOneField(
        ClientDetails, 
        on_delete=models.CASCADE,
        related_name='settlement'
    )
    settle_date = models.DateField(null=True, blank=True)
    settle_status = models.CharField(
        max_length=10, 
        choices=SETTLEMENT_STATUS, 
        default='Active'
    )
    
    def __str__(self):
        return f"Settlement status for {self.client.name}: {self.settle_status}"