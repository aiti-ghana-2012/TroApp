# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Station'
        db.create_table('trotro_station', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('gpsLocation', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('trotro', ['Station'])

        # Adding model 'Route'
        db.create_table('trotro_route', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fare', self.gf('django.db.models.fields.IntegerField')()),
            ('destination', self.gf('django.db.models.fields.related.ForeignKey')(related_name='destination', to=orm['trotro.Station'])),
            ('arrival', self.gf('django.db.models.fields.related.ForeignKey')(related_name='arrival', to=orm['trotro.Station'])),
        ))
        db.send_create_signal('trotro', ['Route'])

        # Adding model 'Stop'
        db.create_table('trotro_stop', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('location', self.gf('django.db.models.fields.CharField')(default='', max_length=50)),
        ))
        db.send_create_signal('trotro', ['Stop'])

        # Adding model 'Route_stop'
        db.create_table('trotro_route_stop', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('route', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['trotro.Route'])),
            ('stop', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['trotro.Stop'])),
            ('order', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('trotro', ['Route_stop'])

        # Adding model 'ZipCode'
        db.create_table('trotro_zipcode', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('zipcode', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('statecode', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('statename', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('create_date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal('trotro', ['ZipCode'])


    def backwards(self, orm):
        # Deleting model 'Station'
        db.delete_table('trotro_station')

        # Deleting model 'Route'
        db.delete_table('trotro_route')

        # Deleting model 'Stop'
        db.delete_table('trotro_stop')

        # Deleting model 'Route_stop'
        db.delete_table('trotro_route_stop')

        # Deleting model 'ZipCode'
        db.delete_table('trotro_zipcode')


    models = {
        'trotro.route': {
            'Meta': {'object_name': 'Route'},
            'arrival': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'arrival'", 'to': "orm['trotro.Station']"}),
            'destination': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'destination'", 'to': "orm['trotro.Station']"}),
            'fare': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'trotro.route_stop': {
            'Meta': {'object_name': 'Route_stop'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'route': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['trotro.Route']"}),
            'stop': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['trotro.Stop']"})
        },
        'trotro.station': {
            'Meta': {'object_name': 'Station'},
            'gpsLocation': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'trotro.stop': {
            'Meta': {'object_name': 'Stop'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '50'}),
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