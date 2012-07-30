# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Stop.accumulated_distance'
        db.add_column('trotro_stop', 'accumulated_distance',
                      self.gf('django.db.models.fields.FloatField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Stop.accumulated_distance'
        db.delete_column('trotro_stop', 'accumulated_distance')


    models = {
        'trotro.route': {
            'Meta': {'object_name': 'Route'},
            'arrival': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'arrival'", 'to': "orm['trotro.Station']"}),
            'departure': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'destination'", 'to': "orm['trotro.Station']"}),
            'fare': ('django.db.models.fields.FloatField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'total_distance': ('django.db.models.fields.FloatField', [], {'default': '0'})
        },
        'trotro.route_stop': {
            'Meta': {'object_name': 'Route_stop'},
            'accumulated_distance': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'route': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'stops'", 'to': "orm['trotro.Route']"}),
            'stop': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['trotro.Stop']"}),
            'stop_fare': ('django.db.models.fields.FloatField', [], {'default': '0'})
        },
        'trotro.station': {
            'Meta': {'object_name': 'Station'},
            'gpsLocation': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'trotro.stop': {
            'Meta': {'object_name': 'Stop'},
            'accumulated_distance': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'gpsLocation': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'trotro.zipcode': {
            'Meta': {'ordering': "['zipcode']", 'object_name': 'ZipCode'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'create_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'statecode': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'statename': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'zipcode': ('django.db.models.fields.CharField', [], {'max_length': '5'})
        }
    }

    complete_apps = ['trotro']