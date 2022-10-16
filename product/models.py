from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.text import slugify
import datetime
from django.urls import reverse
# from django.core.urlresolvers import reverse
# Create your models here.


class Product(models.Model):
    PRDName = models.CharField(max_length=100 , verbose_name=_("اسم النتج "))
    PRDCategory = models.ForeignKey('Category' , on_delete=models.CASCADE , blank=True, null=True ,verbose_name=_("الصنف "))
    PRDBrand = models.ForeignKey('settings.Brand' , on_delete=models.CASCADE , blank=True, null=True ,verbose_name=_("الماركه "))
    PRDDesc = models.TextField(verbose_name=_("وصف المنتج"))
    PRDImage = models.ImageField(upload_to='prodcut/' , verbose_name=_("Image") , blank=True, null=True)
    PRDImage2 = models.ImageField(upload_to='prodcut/', verbose_name=_("Image"), blank=True, null=True)
    PRDImage3 = models.ImageField(upload_to='prodcut/', verbose_name=_("Image"), blank=True, null=True)
    PRDPrice = models.DecimalField(max_digits=5  , decimal_places=2 , verbose_name=_("السعر"))
    PRDDiscountPrice = models.DecimalField(max_digits=5  , decimal_places=2 , verbose_name=_("السعر بعد التخفيض"))
    PRDCost = models.DecimalField(max_digits=5 , decimal_places=2 , verbose_name=_("التكلفة"))
    PRDCreated = models.DateTimeField(default = datetime.datetime.now ,verbose_name=_("وقت الاضاقه"))

    PRDSLug = models.SlugField(blank=True, null=True , verbose_name=_("عنوان URL"))
    PRDISNew = models.BooleanField(default=True , verbose_name=_("المنج جديد "))
    PRDISBestSeller = models.BooleanField(default=False , verbose_name=_("الاكثر مبيعا"))

    
    def save(self , *args , **kwargs):
        if not self.PRDSLug :
            self.PRDSLug = slugify(self.PRDName)
        super(Product , self).save(*args , **kwargs)
    
    class Meta:
        verbose_name = _("Product")
        verbose_name_plural = _("Products")
        ordering =['PRDCreated']

    def get_absolute_url(self):
        return reverse('products:product_detail', kwargs={'slug': self.PRDSLug})

    def __str__(self):
        return self.PRDName





class ProductImage(models.Model):
    PRDIProduct = models.ForeignKey(Product , on_delete=models.CASCADE , verbose_name=_("Product"))
    PRDIImage = models.ImageField(upload_to='prodcut/' , verbose_name=_("Image"))

    @property
    def __str__(self):
        return str(self.PRDIProduct)


class Category(models.Model):
    CATName = models.CharField(max_length=50 , verbose_name=_("Name"))
    CATParent = models.ForeignKey('self' ,limit_choices_to={'CATParent__isnull' : True}, verbose_name=_("Main Category"), on_delete=models.CASCADE , blank=True, null=True)
    CATDesc = models.TextField( verbose_name=_("Description"))
    CATImg = models.ImageField(upload_to='category/' , verbose_name=_("Image"))

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.CATName



class Product_Alternative(models.Model):
    PALNProduct = models.ForeignKey(Product , on_delete=models.CASCADE , related_name='main_prodcut' , verbose_name=_("Product"))
    PALNAlternatives = models.ManyToManyField(Product , related_name='alternative_products'  , verbose_name=_("Alternatives"))
    
    class Meta:
        verbose_name = _("Product Alternative")
        verbose_name_plural = _("Product Alternatives")

    def __str__(self):
        return str(self.PALNProduct)


class Product_Accessories(models.Model):
    PACCProduct = models.ForeignKey(Product , on_delete=models.CASCADE , related_name='mainAccessory_prodcut' , verbose_name=_("Product"))
    PACCAlternatives = models.ManyToManyField(Product , related_name='accessories_products' , verbose_name=_("Accessories"))
      
    class Meta:
        verbose_name = _("Product Accessory")
        verbose_name_plural = _("Product Accessories")

    def __str__(self):
        return str(self.PACCProduct)





