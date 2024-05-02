from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from .models import BudgetCategory, Transaction

User = get_user_model()

class BaseModelTestCase(TestCase):
    def test_base_model_fields(self):
        model = BaseModel()
        self.assertIsInstance(model.id, uuid.UUID)
        self.assertIsInstance(model.created, timezone.datetime)
        self.assertIsNone(model.modified)

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
        self.assertEqual(category.owner, self.user)
        self.assertEqual(category.name, 'Test Category')
        self.assertEqual(category.description, 'Test Description')
        self.assertEqual(category.max_spend, 100.00)
        self.assertIsInstance(category.created, timezone.datetime)

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
            category = BudgetCategory.objects.create(
                owner=self.user,
                name='Test Category',
                description='Test Description',
                max_spend=-100.00
            )

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
            transaction = Transaction.objects.create(
                owner=self.user,
                category=self.category,
                amount=-50.00,
                description='Test Transaction'
            )