from django.db import models


class Event(models.Model):
    id=models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    heure = models.TimeField()
    date = models.DateField()
    lieu=models.CharField(max_length=15)
   # lead = models.ForeignKey(Lead, on_delete=models.PROTECT)  # Clé étrangère vers Lead
    #utilisateurid = models.ForeignKey(User, on_delete=models.PROTECT)  # Clé étrangère vers User

    def _str_(self):
        return self.title