from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from flite.core.models import BudgetCategory, Transaction

User = get_user_model()

class BudgetCategoryModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_budget_category_creation(self):
        category = BudgetCategory.objects.create(
            owner=self.user,
            name='Test Category',
            description='Test Description',
            max_spend=100.00
        )
        self.assertEqual(category.owner, self.user)
        self.assertEqual(category.name, 'Test Category')
        self.assertEqual(category.description, 'Test Description')
        self.assertEqual(category.max_spend, 100.00)

    def test_budget_category_str(self):
        category = BudgetCategory.objects.create(
            owner=self.user,
            name='Test Category',
            description='Test Description',
            max_spend=100.00
        )
        self.assertEqual(str(category), 'Test Category')

class TransactionModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.category = BudgetCategory.objects.create(
            owner=self.user,
            name='Test Category',
            description='Test Description',
            max_spend=100.00
        )

    def test_transaction_creation(self):
        transaction = Transaction.objects.create(
            owner=self.user,
            category=self.category,
            amount=50.00,
            description='Test Transaction'
        )
        self.assertEqual(transaction.owner, self.user)
        self.assertEqual(transaction.category, self.category)
        self.assertEqual(transaction.amount, 50.00)
        self.assertEqual(transaction.description, 'Test Transaction')

    def test_transaction_str(self):
        transaction = Transaction.objects.create(
            owner=self.user,
            category=self.category,
            amount=50.00,
            description='Test Transaction'
        )
        self.assertEqual(str(transaction), f'{self.category.name} - 50.00')

    def test_transaction_amount_validation(self):
        with self.assertRaises(ValidationError):
            transaction = Transaction(
                owner=self.user,
                category=self.category,
                amount=-50.00,  # invalid amount
                description='Test Transaction'
            )
            transaction.full_clean()