from django.db import models

# Create your models here.
class Document(models.Model):
    mendeley_id = models.CharField(max_length=100, null=True, unique=True)
    title = models.CharField(max_length=256)
    tags = models.CharField(max_length=512)
    websites = models.CharField(max_length=1024, default='')
    abstract = models.TextField(null=True)
    categories = models.ManyToManyField(Category)
    groups = models.ManyToManyField(MendeleyGroup)

    year = models.DateTimeField(default=timezone.now())
    keywords = models.CharField(max_length=250, blank=True)
    author = models.CharField(max_length=100, blank=True)

    classified = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('home')
    
    def get_categories(self):
        return list(self.categories.all)


class MendeleyGroup(models.Model):
    # Mendeley User to handle the group
    mendeley_username = models.CharField(max_length=250)

    mendeley_password = models.CharField(max_length=250)
    # Mendeley Group Id
    mendeley_id = models.CharField(max_length=36)
    name = models.CharField(max_length=250)
    # endeley URL
    link = models.CharField(max_length=250, default='www.mendeley.com')
    # Mendeley Group access type
    access_level = models.CharField(max_length=20, choices=[('private','private'), ('invite_only','invite_only'), ('public','public')], default='private')
    # Documents in the Group.

    # Categories in the Group

    def __str__(self):
        return self.name

    def documents(self):
        return self.document_set.all()

    def categories(self):
        return Category.objects.filter(group=self)

    def save(self):
        super().save()
        try:
            c = Category.objects.get(cat_id=self.mendeley_id)
            return
        except Category.DoesNotExist:
            c = Category(name='root', group=self, cat_id=self.mendeley_id)
            c.save()

    def get_docs_amount(self):
        return self.document_set.all().count()