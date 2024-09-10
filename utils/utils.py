#from django.contrib.auth.models import User, Group

#users = User.objects.all().exclude(is_superuser=True)
#group = Group.objects.get(name="gestor")
#for user in users:
#    if not user.groups.all():
#        group.user_set.add(user)


#root_group = Group.objects.get(name="root")

#billing = User.objects.get(username="billing")
#billing_groups = billing.groups.all()
#if billing_groups:
#    for group in billing_groups:
#        group.user_set.remove(billing)
#root_group.user_set.add(billing)
#suporte.is_superuser=True
#billing.set_password('#24OEOD#5EIHjPC3O4uy')
#billing.save()

#suporte = User.objects.get(username="suporte@pinegap.io")
#suporte_groups = suporte.groups.all()
#if suporte_groups:
#    for group in suporte_groups:
#        group.user_set.remove(suporte)
#root_group.user_set.add(suporte)
#suporte.is_superuser=True
#suporte.set_password('5IK%$$gjBHVhQx1Um@xV')
#suporte.save()
