from typing import Iterable, Optional
from django.db import models
from django.contrib.auth.models import User
from .utils import validate_phone_number  

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=125, verbose_name="Название")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Post(models.Model):
    image = models.ImageField(upload_to="posts/", verbose_name="Изображение")
    title = models.CharField(max_length=125, verbose_name="Заголовок")
    description = models.TextField(max_length=500, verbose_name="Описание")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")
    location = models.CharField(max_length=125, verbose_name="Место проведения")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    
    def __str__(self):
        return f"{self.title} - {self.category} - {self.created_at}"
    
    class Meta:
        verbose_name = "Публикация"
        verbose_name_plural = "Публикации"


class HomeImage(models.Model):
    image = models.ImageField(upload_to="home_image", verbose_name="Изображение")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    
    def __str__(self) -> str:
        return f"Изображение созданная в {self.created_at}"
    
    class Meta:
        verbose_name = "Изображения Главной Странницы"


class HomeRowText(models.Model):
    title = models.CharField(max_length=125, verbose_name="Заголовок")
    description = models.TextField(max_length=500, verbose_name="Описание")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self) -> str:
        return self.title
    
    class Meta:
        verbose_name = "Row Text Главное Странницы"
        verbose_name_plural = "Row Text Главных Странниц"


class Contact(models.Model):
    name = models.CharField(max_length=125, verbose_name="Имя")
    email = models.EmailField(max_length=125, verbose_name="Почта")
    message = models.TextField(max_length=500, verbose_name="Сообщение")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    
    def __str__(self):
        return f"{self.name} - {self.created_at}"
    
    class Meta:
        verbose_name = "Сообщение"
        verbose_name_plural = "Сообщения"


class ContactSlider(models.Model):
    image = models.ImageField(upload_to="contact_slider", verbose_name="Изображение", help_text="Размер изображения - 3840x2160")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    
    def __str__(self):
        return f"Изображение созданное в - {self.created_at}"
    
    class Meta:
        verbose_name = "Сладер Контакта"
        verbose_name_plural = "Сладеры Контактов"


class Anime(models.Model):
    image = models.URLField(verbose_name="Ссылка на изображение")
    title = models.CharField(max_length=125, verbose_name="Название")
    category = models.CharField(max_length=125, verbose_name="Категория")
    description = models.TextField(max_length=800, verbose_name="Описание")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self) -> str:
        return f"{self.title} - {self.category} - {self.created_at}"
    
    class Meta:
        verbose_name = "Аниме"
        verbose_name_plural = "Аниме"


class Profile(models.Model):
    image = models.ImageField(  upload_to="profile/", 
                                verbose_name="Фотография", 
                                help_text="Картинка должна быть Х на Х", 
                                blank=True, 
                                null=True)

    balance = models.PositiveIntegerField(default=0, 
                                          verbose_name="Баланс")

    phone = models.CharField(max_length=20, 
                             unique=True, 
                             verbose_name="Номер телефона", 
                             blank=True, null=True, 
                             validators=[validate_phone_number])

    birth_date = models.DateField(verbose_name="Дата рождения", 
                                  blank=True, 
                                  null=True)

    about = models.TextField(max_length=200, 
                             verbose_name="Обо мне", 
                             blank=True, 
                             null=True)

    user = models.OneToOneField(User, 
                                on_delete=models.CASCADE, 
                                verbose_name="Пользователь")

    created_at = models.DateTimeField(auto_now_add=True)

    
    def __str__(self) -> str:
        return f"{self.user.first_name.title()} {self.user.last_name.title()[0]}."
    
    def get_by_phone(self, phone):
        return Profile.objects.get(phone=phone)
    
    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"
        ordering = ["-created_at"]


class Transaction(models.Model):
    sender_phone = models.CharField(max_length=20,
                                      verbose_name='Номер телефона отправителя')
    
    recipient_phone = models.CharField(max_length=20,
                                       verbose_name='Номер телефона получателя')
    
    summa = models.PositiveIntegerField(default=100, 
                                        verbose_name="Сумма")
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    def save(self, *args, **kwargs):
        try:
            sender_profile = Profile.objects.get(phone=self.sender_phone)
        except Profile.DoesNotExist:
            raise Exception('Профиль отправителя не найден \
                                или У вы не указали номер телефона')
        
        try:
            recipient_profile = Profile.objects.get(phone=self.recipient_phone)
        except Profile.DoesNotExist:
            raise Exception('Профиль получателя не найден')
        
        if sender_profile.balance < self.summa:
            raise Exception('Недастаточно средств на балансе отправителя')
        
        sender_profile.balance -= self.summa
        recipient_profile.balance += self.summa
        sender_profile.save()
        recipient_profile.save()
        super().save(*args, **kwargs)
        
    def __str__(self) -> str:
        return f"{self.sender_phone_id} -> {self.recipient_phone_id}"
    
    class Meta:
        verbose_name = "Транзакция"
        verbose_name_plural = "Транзакции"
        ordering = ["-created_at"]