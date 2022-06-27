from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw
from django.utils.safestring import mark_safe






class CustomUserManager(BaseUserManager):

    def _create_user(self, email, password, **extra_fields):
        '''
        Create and save a User with the given email and password.
        '''
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)


        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    username = None # override user from base user class
    email = models.EmailField(verbose_name="Email", null=True, unique=True, max_length=100)
    qr_code = models.ImageField(upload_to='qr_codes', blank=True)


    # create qrcode with save user
    def save (self, *args, **kwargs):
        if ( not self.id == 'qr_code-{self.id}.png'):
            try:
                qrcode_img = qrcode.make(self.id)
                canvas = Image.new('RGB', (330,330), 'white')
                draw = ImageDraw.Draw(canvas)
                canvas.paste(qrcode_img)
                fname = f'qr_code-{self.id}.png'
                buffer = BytesIO()
                canvas.save(buffer,'PNG')
                self.qr_code.save(fname, File(buffer), save=False)
                canvas.close()
                super().save(*args,**kwargs)
            except IOError :
                pass

    USERNAME_FIELD = 'email' # make the user log in with the email
    REQUIRED_FIELDS = []

    objects = CustomUserManager() # custom manager create above 

    def __str__(self):
        return self.email
    
    # to create mini image qrcode 
    def image_tag(self):
        return mark_safe('<img src="{}" height="100"/>'.format(self.qr_code.url))

    image_tag.short_description = 'Image'

