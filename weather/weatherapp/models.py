from django.db import models

# Create your models here.
class City(models.Model):
    name = models.CharField(max_length= 45)
    
    class Meta:
        verbose_name_plural = 'cities'  #it just modifies the respective object name in admin panel for plural objects
                                        #for example instead of Citys it will be cities now in the admin panel
                                        #django be defaults just add s to the class name to make it plural ig
                                        #so by using this we can change that
