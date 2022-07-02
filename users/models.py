import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.db.models.signals import post_save
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw
from django.utils.safestring import mark_safe
from django.core.validators import MaxValueValidator, MinValueValidator 




BOOL_CHOICES = ((True, 'TAK'), (False, 'NIE'))



# USER_TYPE_CHOICES = (
#       (1, 'student'),
#       (2, 'teacher'),
#       (3, 'secretary'),
#       (4, 'supervisor'),
#       (5, 'admin'),
#   )

#   user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES)

class UserManager(BaseUserManager):

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
        extra_fields.setdefault('is_superuser', True)
       

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)
#custom user
class User(AbstractUser):
    username = None # override user from base user class / delete username
    email = models.EmailField(verbose_name='Email', null=True, unique=True, max_length=100)
    qr_code = models.ImageField(upload_to='qr_codes', blank=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    position = models.ForeignKey('Position',related_name='user_position', on_delete=models.PROTECT ,null=True, blank=False)
    country = models.ForeignKey('Country', related_name='country_user',null=True, on_delete=models.PROTECT,)
    department = models.ForeignKey( 'Department',related_name='department_user',  blank=False, on_delete=models.PROTECT, null=True,)
    
    doctor = models.BooleanField(choices=BOOL_CHOICES, default=False)
    rescuer_kkp = models.BooleanField(choices=BOOL_CHOICES, default=False)
    category_b_driver = models.BooleanField(choices=BOOL_CHOICES, default=False)
    aut_to_drive_emergency_vehicles = models.BooleanField(choices=BOOL_CHOICES, default=False)
    aut_to_drive_foundation_vehicles = models.BooleanField(choices=BOOL_CHOICES, default=False)
    camp_counselor = models.BooleanField(choices=BOOL_CHOICES, default=False)
    maltese_instructor = models.BooleanField(choices=BOOL_CHOICES, default=False)
    
    

    # create qrcode with save user
    def save(self, *args, **kwargs):
        if not self.qr_code: #if qr_code exist, do nothing
            qrcode_img = qrcode.make(self.id)
            canvas = Image.new('RGB', (365,365), 'white')
            draw = ImageDraw.Draw(canvas)
            canvas.paste(qrcode_img)
            fname = f'qr_code-{self.id}.png'
            buffer = BytesIO()
            canvas.save(buffer,'PNG')
            self.qr_code.save(fname, File(buffer), save=False)
            canvas.close()
        super().save(*args,**kwargs)
                
    USERNAME_FIELD = 'email' # make the user log in with the email
    REQUIRED_FIELDS = []

    objects = UserManager() # custom manager create above 

    def __str__(self):
        # if self.first_name is None:
        #     self.first_name = self.email
        #     return self.first_name
        # return self.email
        return f'{self.first_name} {self.last_name}' 
    
    # to create mini image qrcode 
    def image_tag(self):
        return mark_safe('<img src="{}" height="100"/>'.format(self.qr_code.url))
    image_tag.short_description = 'QR Code'

    class Meta:
            verbose_name_plural = "Użytkownik"

#EVENT 
class Event(models.Model):
    type_event = models.ForeignKey('TypeEvent', related_name='type_events',on_delete=models.PROTECT, null=True,)
    event = models.CharField(max_length=50)
    member = models.ManyToManyField(User, related_name = 'members_event', through='MemberEvent',blank=True,)
    event_for_benefi = models.BooleanField(choices=BOOL_CHOICES, default=False)
    num_const_benefi = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(50)])
    num_disposable_benefi = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(50)])
    num_pers_secure = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(50)])
    donati_value_pln = models.IntegerField()
    currency = models.ForeignKey('Currency', related_name='currencya', on_delete=models.PROTECT, null=True)
    donati_weight = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(50)])
    event_incom = models.IntegerField()
    event_cost = models.IntegerField()
    observations = models.TextField(max_length=255)
    positiv_elem = models.TextField(max_length=255)
    improvment_elem = models.TextField(max_length=255)

    def __str__(self):
        return self.event

    class Meta:
        verbose_name_plural = "Wydarzenie"

class Entitlements(models.Model):
    expiration_date = models.DateField()

class Position(models.Model):
    position_name =  models.CharField(max_length=20,verbose_name="Stanowisko", unique=True)
    

    def __str__(self):
        return self.position_name

    class Meta:
        verbose_name_plural = "Stanowisko"
        
class Country(models.Model):
    TYPE_CHOICES=(
        ('polska', ("Polska")),
        )

    country  = models.CharField(max_length=20, default='polska', null=True, choices=TYPE_CHOICES, unique=True)
    

    def __str__(self):
        return self.country

    class Meta:
            verbose_name_plural = "Kraj"

class Department(models.Model):
    department = models.CharField('Oddział',max_length=15,  unique=True)

    def __str__(self):
        return self.department
    
    class Meta:
            verbose_name_plural = "Oddział"

class TypeEvent(models.Model):
    
    types = models.CharField('Rodzaj wydarzenia',max_length=40, unique=False)
    added_by = models.ForeignKey(User, related_name='event_type_added_by',blank=False,  on_delete=models.PROTECT, default=User )
    depart_show = models.ManyToManyField('Department' )
    


    def __str__(self):
        return str(self.types)
    
    def save(self, *args, **kwargs):
        if not self.added_by: 
            self.added_by = User
        super().save(*args,**kwargs)

    class Meta:
        verbose_name_plural = "Rodzaj Wydarzenia"

class MemberEvent(models.Model):
    TYPE_CHOICES=(
        ('kierowca', ("Kierowca")),
        ('koordynator', ("Koordynator")),
        ('lekarz', ("Lekarz")),
        ('pomoc_techniczna', ("Pomoc Techniczna")),
        ('ratownik', ("Ratownik")),
        ('szef_akcji', ("Szef Akcji")),
        ('wolontariusz_administracyjny', ("Wolontariusz Administracyjny")),
        ('wolontariusz', ("Wolontariusz")),
        )

    member = models.ForeignKey(User,related_name='member_event', on_delete=models.PROTECT, blank=False, null=False)
    user = models.ForeignKey(Event, related_name='user_member', on_delete=models.PROTECT,#blank=False,null=False)
    )
    is_work = models.BooleanField(choices=BOOL_CHOICES, default=True)
    hourse_work = models.IntegerField( validators=[MinValueValidator(0), MaxValueValidator(24)])
    is_prepare = models.BooleanField(choices=BOOL_CHOICES, default=False)
    hourse_prepare = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(24)])

    def save(self, *args, **kwargs):
        if not self.is_work: 
            self.hourse_work = 0
        super().save(*args,**kwargs)


    def save(self, *args, **kwargs):
        if not self.is_prepare: 
            self.hourse_prepare = Null
        super().save(*args,**kwargs)
    


    def __str__(self):
            return str(self.user)

class Currency(models.Model):
    TYPE_CHOICES=(
        ('pln', ("PLN")),
        ('chf', ("CHF")),
        ('eur', ("EUR")),
        ('usd', ("USD")),
        )

    currency  = models.CharField(max_length=20, default='pln', null=True, choices=TYPE_CHOICES, unique=True)

    
    def __str__(self):
            return str(self.currency)