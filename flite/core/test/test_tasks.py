

from django.test import TestCase
from django.core import mail
from flite.users.models import User
from flite.core.models import BudgetCategory, Transaction
from flite.core.tasks import check_budget_threshold
from decimal import Decimal

class TestCheckBudgetThresholdTask(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('testuser', 'test@example.com', 'password')
        self.category = BudgetCategory.objects.create(name='Test Category', description='Test description', max_spend=100.00, owner=self.user)

    def test_check_budget_threshold_below_threshold(self):
        Transaction.objects.create(owner=self.user, category=self.category, amount=Decimal('40.00'), description='Test transaction')
        self.assertEqual(len(mail.outbox), 0)
        
    def test_check_budget_threshold_multiple_categories(self):
        transaction = Transaction.objects.create(owner=self.user, category=self.category, amount=Decimal('50.00'))
        category2 = BudgetCategory.objects.create(name='Test Category 2', description='Test description 2', max_spend=200.00, owner=self.user)
        Transaction.objects.create(owner=self.user, category=self.category, amount=Decimal('60.00'), description='Test transaction')

    def test_check_budget_threshold_no_transactions(self):
        empty_category = BudgetCategory.objects.create(name='Empty Category', description='Empty description', max_spend=100.00, owner=self.user)
        transaction = Transaction.objects.create(owner=self.user, category=empty_category, amount=10.00, description='Test transaction')
        check_budget_threshold(transaction)
        self.assertEqual(len(mail.outbox), 0) 
        
    def test_check_budget_threshold_below_fifty_percent(self):
        Transaction.objects.create(owner=self.user, category=self.category, amount=20.00, description='Test transaction')
        transaction = Transaction.objects.create(owner=self.user, category=self.category, amount=10.00, description='Test transaction')
        check_budget_threshold(transaction)
        self.assertEqual(len(mail.outbox), 0) 