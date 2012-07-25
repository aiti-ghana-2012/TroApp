from django.db import models
#from field import CoordinatesField
from django.contrib import admin
#from django.newforms import FormField 
import datetime

class Station(models.Model):
    name = models.CharField(max_length=200)
    gpsLocation = models.CharField(max_length=50)
    # help_text=_("Please click on the marker.")
    
    def __unicode__(self):
        return self.name


class Route(models.Model):
    fare = models.IntegerField()
    destination = models.ForeignKey(Station, related_name='destination')
    arrival = models.ForeignKey(Station, related_name='arrival')

    def __unicode__(self):
        router = str(self.destination) + ' - ' + str(self.arrival)
        return router 

class Stop(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=50, default= '')
    

    def __unicode__(self):
        return self.name

    
class Route_stop(models.Model):
    route = models.ForeignKey(Route)
    stop = models.ForeignKey(Stop)
    order = models.IntegerField()

    def __unicode__(self):
        RouteStop =str(self.route) + 'the stop'
        return RouteStop
    


class RouteInline(admin.TabularInline):
    model=Route
    extra= 2
    fk_name='destination'   # to dissociate the foreignkeys

class StopInline(admin.TabularInline):
    model=Stop
    extra = 2

class RouteStopInline(admin.TabularInline):
    model = Route_stop
    extra = 2

class StationAdmin(admin.ModelAdmin):
    fieldsets = [(None,{'fields':['name']}),
                 ('GPS-Info',{'fields':['gpsLocation'],'classes':['collapse']}),
          
                ]
    extra = 2
    inlines = [RouteInline]

    list_display = ['name','gpsLocation']
    list_filter = ['arrival']
    search_fields = ['name']

class StopAdmin(admin.ModelAdmin):
    fieldsets = [ (None,{'fields':['name']}),
                 ('GPS-Info',{'fields':['location'],'classes':['collapse']}),
          
                ]
    list_display = ['name','location']
    list_filter = ['name']
    search_fields = ['name']

    inlines = [RouteStopInline]

    

class RouteAdmin(admin.ModelAdmin):
    fieldsets = [ ('Cost',{'fields':['fare']}),
                 ('stations',{'fields':['destination','arrival']}),
                ]
    list_display = ['destination','arrival','fare']
    list_filter = ['arrival','destination']
    
    
    

 
class ZipCode(models.Model):
    zipcode = models.CharField(max_length=5)
    city = models.CharField(max_length=64)
    statecode = models.CharField(max_length=2)
    statename = models.CharField(max_length=32)
    create_date = models.DateTimeField(default=datetime.datetime.now)
 
    def __unicode__(self):
        return "%s, %s (%s)" % (self.city, self.statecode, self.zipcode)
 
    class Meta:
        ordering = ['zipcode']


admin.site.register(Station, StationAdmin)
admin.site.register(Stop,StopAdmin)
admin.site.register(Route,RouteAdmin)
admin.site.register(Route_stop)
admin.site.register(ZipCode)
