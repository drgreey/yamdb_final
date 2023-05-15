from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from api_yamdb.settings import ADMIN, MAX_SCORE, MIN_SCORE, MODERATOR, USER

from .validators import year_validator


class User(AbstractUser):
    username = models.CharField('Логин', max_length=150, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    first_name = models.CharField('Имя', max_length=150, blank=True, null=True)
    last_name = models.CharField(
        'Фамилия', max_length=150, blank=True, null=True
    )
    bio = models.TextField('Биография', blank=True, null=True)
    role = models.CharField(
        'Роль',
        choices=(
            (USER, 'user'),
            (MODERATOR, 'moderator'),
            (ADMIN, 'admin'),
        ),
        max_length=9,
        default=USER,
    )
    confirmation_code = models.TextField(
        'Проверочный код', blank=True, null=True
    )

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ('email',)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username',)

    def __str__(self):
        return self.username[:30]

    @property
    def is_admin(self):
        return self.role == ADMIN

    @property
    def is_moderator(self):
        return self.role == MODERATOR


class Genre(models.Model):
    name = models.CharField('Название', max_length=256)
    slug = models.SlugField('Слаг жанра', max_length=50, unique=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('name',)

    def __str__(self):
        return self.name[:30]


class Category(models.Model):
    name = models.CharField('Название', max_length=256)
    slug = models.SlugField('Слаг категории', max_length=50, unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('name',)

    def __str__(self):
        return self.name[:30]


class Title(models.Model):
    name = models.CharField('Название', max_length=256)
    year = models.IntegerField('Год выпуска', validators=[year_validator])
    description = models.TextField('Описание', blank=True, null=True)
    genre = models.ManyToManyField(Genre, verbose_name='Жанр')
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        null=True,
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('name',)

    def __str__(self):
        return self.name[:30]


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        related_name='reviews',
        on_delete=models.CASCADE,
    )
    text = models.TextField('Отзыв')
    pub_date = models.DateTimeField(
        'Время публикации',
        auto_now_add=True,
    )
    author = models.ForeignKey(
        User,
        verbose_name='Рецензирующий',
        on_delete=models.CASCADE,
        related_name='reviews',
    )
    score = models.IntegerField(
        'Оценка',
        validators=[
            MinValueValidator(
                limit_value=MIN_SCORE,
                message=f'Оценка не может быть меньше {MIN_SCORE}',
            ),
            MaxValueValidator(
                limit_value=MAX_SCORE,
                message=f'Оценка не может быть больше {MAX_SCORE}',
            ),
        ],
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-pub_date',)
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_review',
            )
        ]

    def __str__(self):
        return self.text[:30]


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        verbose_name='Автор комментария',
        related_name='comments',
        on_delete=models.CASCADE,
    )
    review = models.ForeignKey(
        Review,
        verbose_name='Отзыв',
        related_name='comments',
        on_delete=models.CASCADE,
    )
    text = models.TextField('Комментарий')
    pub_date = models.DateTimeField(
        'Время публикации отзыва',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:30]
