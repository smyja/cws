from django.core.exceptions import ValidationError
from django.test import TestCase
from flite.core.models import BudgetCategory, Transaction
from flite.users.models import User
class TestBudgetCategoryModel(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('testuser', 'test@example.com', 'password')

    def test_budget_category_creation(self):
        category = BudgetCategory.objects.create(name='Test Category', description='Test description', max_spend=100.00, owner=self.user)
        self.assertEqual(category.name, 'Test Category')
        self.assertEqual(category.description, 'Test description')
        self.assertEqual(category.max_spend, 100.00)
        self.assertEqual(category.owner, self.user)
        self.assertIsNotNone(category.id)
        self.assertIsNotNone(category.created)
        self.assertIsNotNone(category.modified)

    def test_budget_category_max_spend_negative(self):
        with self.assertRaises(ValidationError):
            category = BudgetCategory(name='Test Category', description='Test description', max_spend=-100.00, owner=self.user)
            category.full_clean()

class TestTransactionModel(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('testuser', 'test@example.com', 'password')
        self.category = BudgetCategory.objects.create(name='Test Category', description='Test description', max_spend=100.00, owner=self.user)

    def test_transaction_creation(self):
        transaction = Transaction.objects.create(owner=self.user, category=self.category, amount=50.00, description='Test transaction')
        self.assertEqual(transaction.owner, self.user)
        self.assertEqual(transaction.category, self.category)
        self.assertEqual(transaction.amount, 50.00)
        self.assertEqual(transaction.description, 'Test transaction')
        self.assertIsNotNone(transaction.id)
        self.assertIsNotNone(transaction.created)
        self.assertIsNotNone(transaction.modified)

    def test_transaction_amount_negative(self):
        with self.assertRaises(ValidationError):
            transaction = Transaction(owner=self.user, category=self.category, amount=-10.00, description='Test transaction')
            transaction.full_clean()