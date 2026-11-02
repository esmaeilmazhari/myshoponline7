from django.db import models
from django.conf import settings
from django.utils.safestring import mark_safe

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="نام دسته‌بندی")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="شناسه لینک")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "دسته‌بندی"
        verbose_name_plural = "دسته‌بندی‌ها"


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products', verbose_name="دسته‌بندی", null=True, blank=True)
    title = models.CharField(max_length=200, verbose_name="نام محصول")
    description = models.TextField(verbose_name="توضیحات")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="قیمت اصلی (تومان)")
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="قیمت با تخفیف (تومان)")
    stock = models.IntegerField(default=0, verbose_name="موجودی انبار")
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name="تصویر محصول")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")

    def __str__(self):
        return self.title

    @property
    def get_discount_percentage(self):
        if self.discount_price and self.price > self.discount_price:
            discount = self.price - self.discount_price
            percentage = (discount / self.price) * 100
            return int(percentage)
        return 0


class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'در انتظار پرداخت'),
        ('success', 'پرداخت موفق'),
        ('failed', 'پرداخت ناموفق'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="کاربر")
    full_name = models.CharField(max_length=100, verbose_name="نام مشتری")
    address = models.TextField(verbose_name="آدرس پستی")
    phone = models.CharField(max_length=15, verbose_name="شماره تماس")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="مجموع مبلغ")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="وضعیت پرداخت")
    tracking_code = models.CharField(max_length=50, blank=True, null=True, verbose_name="کد رهگیری")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت سفارش")

    def __str__(self):
        return f"سفارش {self.id} - {self.full_name}"

    def status_colored(self):
        if self.status == 'success':
            return mark_safe('<span style="color: green; font-weight: bold;">✔️ پرداخت موفق</span>')
        elif self.status == 'failed':
            return mark_safe('<span style="color: red; font-weight: bold;">❌ پرداخت ناموفق</span>')
        return mark_safe('<span style="color: orange;">⏳ در انتظار</span>')
    
    status_colored.short_description = 'وضعیت'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, verbose_name="سفارش")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="محصول")
    quantity = models.PositiveIntegerField(default=1, verbose_name="تعداد")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="قیمت در زمان خرید")

    def __str__(self):
        return f"{self.quantity} عدد از {self.product.title}"
    # ... (کدهای قبلی مدل‌ها) ...

# 👇 این کد را به انتهای فایل models.py اضافه کنید
from django.db.models.signals import pre_delete
from django.dispatch import receiver

@receiver(pre_delete, sender=Order)
def restore_stock_on_order_delete(sender, instance, **kwargs):
    # اگر وضعیت سفارش "ناموفق" نباشد، یعنی موجودی کسر شده است و باید برگردد
    if instance.status in ['pending', 'success']:
        for item in instance.items.all():
            product = item.product
            product.stock += item.quantity
            product.save()