from django.db import models


class TelegramUser(models.Model):
    class Meta:
        app_label = 'main'
    user_id = models.IntegerField(unique=True)
    user_name = models.CharField(max_length=100)
    click = models.DecimalField(default=0, decimal_places=2, max_digits=11)
    ticket = models.IntegerField(default=0)

    def __str__(self):
        return str(self.user_name)


class Pool(models.Model):
    pool_name = models.CharField(max_length=25)
    coin = models.DecimalField(decimal_places=2, max_digits=20)
    ticket = models.IntegerField()
    z = models.IntegerField()

    def __str__(self):
        return str(self.pool_name)


class History(models.Model):
    user_id = models.IntegerField()
    action = models.TextField()
    ticket_count = models.IntegerField()
    coin_count = models.DecimalField(decimal_places=2, max_digits=21)
    balance = models.DecimalField(default=0, decimal_places=2, max_digits=21)
    time_now = models.DateTimeField(auto_now_add=True)


