import uuid
from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from flite.core.models import BudgetCategory, Transaction
from datetime import timedelta

User = get_user_model()

class BudgetCategoryTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_budget_category_creation(self):
        category = BudgetCategory.objects.create(
            owner=self.user,
            name='Test Category',
            description='Test Description',
            max_spend=100.00
        )
        self.assertIsInstance(category.id, uuid.UUID)
        self.assertIsInstance(category.created, timezone.datetime)
        self.assertIsInstance(category.modified, timezone.datetime)
        self.assertEqual(category.owner, self.user)
        self.assertEqual(category.name, 'Test Category')
        self.assertEqual(category.description, 'Test Description')
        self.assertEqual(category.max_spend, 100.00)

    def test_budget_category_str_representation(self):
        category = BudgetCategory.objects.create(
            owner=self.user,
            name='Test Category',
            description='Test Description',
            max_spend=100.00
        )
        self.assertEqual(str(category), 'Test Category')

    def test_budget_category_max_spend_validation(self):
        with self.assertRaises(ValidationError):
            category = BudgetCategory(
                owner=self.user,
                name='Test Category',
                description='Test Description',
                max_spend=-100.00
            )
            category.full_clean()

    def test_budget_category_invalid_data(self):
        with self.assertRaises(ValidationError):
            category = BudgetCategory(
                owner=self.user,
                name='',  # empty name
                description='Test Description',
                max_spend=100.00
            )
            category.full_clean()

        with self.assertRaises(ValidationError):
            category = BudgetCategory(
                owner=self.user,
                name='Test Category',
                description='',  # empty description
                max_spend=100.00
            )
            category.full_clean()

    def test_budget_category_relationships(self):
        category = BudgetCategory.objects.create(
            owner=self.user,
            name='Test Category',
            description='Test Description',
            max_spend=100.00
        )
        self.assertEqual(category.owner, self.user)

    def test_budget_category_data_integrity(self):
        with self.assertRaises(ValidationError):
            category = BudgetCategory(
                owner=self.user,
                name='Test Category',
                description='Test Description',
                max_spend=-100.00  # invalid max_spend
            )
            category.full_clean()

    def test_budget_category_querysets(self):
        # Test filtering by owner
        categories = BudgetCategory.objects.filter(owner=self.user)
        self.assertEqual(categories.count(), 0)

        # Test filtering by name
        categories = BudgetCategory.objects.filter(name='Test Category')
        self.assertEqual(categories.count(), 0)

class TransactionTestCase(TestCase):
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
        self.assertIsInstance(transaction.id, uuid.UUID)
        self.assertIsInstance(transaction.created, timezone.datetime)
        self.assertIsInstance(transaction.modified, timezone.datetime)
        self.assertEqual(transaction.owner, self.user)
        self.assertEqual(transaction.category, self.category)
        self.assertEqual(transaction.amount, 50.00)
        self.assertEqual(transaction.description, 'Test Transaction')
        self.assertIsInstance(transaction.date, timezone.datetime)

    def test_transaction_str_representation(self):
        transaction = Transaction.objects.create(
            owner=self.user,
            category=self.category,
            amount=50.00,
            description='Test Transaction'
        )
        self.assertEqual(str(transaction), 'Test Category - 50.00')

    def test_transaction_amount_validation(self):
        with self.assertRaises(ValidationError):
            transaction = Transaction(
                owner=self.user,
                category=self.category,
                amount=-50.00,
                description='Test Transaction'
            )
            transaction.full_clean()

    def test_transaction_invalid_data(self):
        with self.assertRaises(ValidationError):
            transaction = Transaction(
                owner=self.user,
                category=self.category,
                amount='invalid',  # invalid amount
                description='Test Transaction'
            )
            transaction.full_clean()

        with self.assertRaises(ValidationError):
            transaction = Transaction(
                owner=self.user,
                category=self.category,
                amount=-50.00,  # invalid amount
                description='Test Transaction'
            )
            transaction.full_clean()

    def test_transaction_relationships(self):
        transaction = Transaction.objects.create(
            owner=self.user,
            category=self.category,
            amount=50.00,
            description='Test Transaction'
        )
        self.assertEqual(transaction.owner, self.user)
        self.assertEqual(transaction.category, self.category)

    def test_transaction_data_integrity(self):
        with self.assertRaises(ValidationError):
            transaction = Transaction(
                owner=self.user,
                category=self.category,
                amount=-50.00,  # invalid amount
                description='Test Transaction'
            )
            transaction.full_clean()

    def test_transaction_querysets(self):
        # Test filtering by owner
        transactions = Transaction.objects.filter(owner=self.user)
        self.assertEqual(transactions.count(), 0)

        # Test filtering by category
        transactions = Transaction.objects.filter(category=self.category)
        self.assertEqual(transactions.count(), 0)

        # Test filtering by date
        transactions = Transaction.objects.filter(date__gte=timezone.now() - timedelta(days=1))
        self.assertEqual(transactions.count(), 0)
