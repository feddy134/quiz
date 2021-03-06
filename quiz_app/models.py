from django.db import models
from django.utils.translation import ugettext_lazy as _
from users.models import User
import uuid
# Create your models here.


class Category(models.Model):
    """
    Stores details of a single Category,
    related to :model:`users.User`
    """
    class Meta:
        verbose_name_plural = _("Categories")

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    image = models.ImageField()
    title = models.CharField(_("Title"), max_length=200)
    description = models.CharField(_('Description'), max_length=1024)
    time_limit = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.title}'


class Question(models.Model):
    """
    Stores details of a single Question,
    related to :model:`quiz_app.Category`
    """
    class Meta:
        verbose_name_plural = _("Questions")

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    question_title = models.CharField(_('Question title'), max_length=1024)
    MCQ = 'MC'
    FILL_IN_THE_BLANKS = 'FI'
    UNDEFINED = 'UD'
    TYPE_CHOICES = [
        (MCQ, 'MCQ'),
        (FILL_IN_THE_BLANKS, 'Fill in the blanks'),
    ]
    type_of_question = models.CharField(
        max_length=2, choices=TYPE_CHOICES, default=UNDEFINED)

    def __str__(self):
        return f'{self.category} | {self.question_title}'


class MCQOptions(models.Model):
    """
    Stores Options of a Question whose type is MCQ,
    related to :model:`quiz_app.Category`
    """
    class Meta:
        verbose_name_plural = _("MCQ Options")

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    question = models.ForeignKey(Question, on_delete=models.PROTECT)
    option = models.CharField(_("Option"), max_length=200)
    is_correct = models.BooleanField(_("Correct answer?"), default=False)

    def __str__(self):
        return f'{self.question} | {self.option}'


class FillInTheBlank(models.Model):
    """
    Stores Options of a Question whose type is MCQ,
    related to :model:`quiz_app.Category`
    """
    class Meta:
        verbose_name_plural = _("Fill In The Blanks")

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    question = models.ForeignKey(Question, on_delete=models.PROTECT)
    correct_answer = models.CharField(_("Correct Answer"), max_length=200)

    def __str__(self):
        return f'{self.question} | {self.correct_answer}'


class Progress(models.Model):
    """
    Stores Progress of the student with the category,
    related to :model:`quiz_app.Category`
    """
    class Meta:
        verbose_name_plural = _("Progress")

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    student = models.ForeignKey(User, on_delete=models.PROTECT)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    start_time = models.DateTimeField(_("Start time"))
    end_time = models.DateTimeField(_("End time"))
    marks = models.IntegerField(_("Marks"), default=0)
    is_in_progress = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.student} | {self.category}'


class StudentQuestion(models.Model):
    """
    Stores Answers of the student for the question,
    related to :model:`quiz_app.Category`
    """
    class Meta:
        verbose_name_plural = _("Student Question")

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)

    student = models.ForeignKey(User, on_delete=models.PROTECT)
    question = models.ForeignKey(Question, on_delete=models.PROTECT)
    option_choosed = models.ForeignKey(
        MCQOptions, on_delete=models.PROTECT, blank=True, null=True)  # if the question is MCQ
    answer_given = models.CharField(
        _("Answer Given by the student"), max_length=200, blank=True, null=True)  # if the question is Fill in the blanks
    is_correct = models.BooleanField(_("Correct?"))
    is_attempted = models.BooleanField(_("Attempted?"))

    def __str__(self):
        return f'{self.student} | {self.question}'
