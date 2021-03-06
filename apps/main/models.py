# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from ..LR.models import User
from django.db import models

class Manager(models.Manager):
    def validate(self,postData, user_id):
        print 'in validator'
        results = {
            'errors': [],
            'status': True
        }
        if len(postData['author']) < 2:
            results['errors'].append('Please enter a valid name')
            results['status'] = False
        if len(postData['quote']) < 10:
            results['errors'].append('Quotes cannot be less than 10 characters')
            results['status'] = False
        if results['status'] is False:
            print 'Error in validation'
            return results
        user = User.objects.get(id=user_id)
        create = Quote.objects.create(author=postData['author'],quote=postData['quote'],user=user)
        print 'finished with validation'
        return results

    def favVal(self, quote_id, user_id):
        print 'in favVal'
        print 'quote_id: {}'.format(quote_id)
        print 'user_id: {}'.format(user_id)
        results = {
            'status': True,
            'errors': [],
        }
        user = User.objects.get(id=user_id)
        quote = Quote.objects.get(id=quote_id)
        print 'quote: {}'.format(quote)
        # if quote id already exists in user's favorites, skip create, is there a more direct way?
        try:
            favorites = Favorite.objects.filter(user=user_id)
        except Favorite.DoesNotExist:
            favorites = None
        switch = False
        if favorites:
            for favoriteObj in favorites:
                print 'in loop - quote: {}'.format(quote)
                print 'in loop - favoriteObj: {}'.format(favoriteObj.quote)
                if favoriteObj.quote == quote:
                    switch = True
            if switch == True:
                return results
            else:
                fave = Favorite.objects.create(quote=quote,user=user)
                return results
        else:
            fave = Favorite.objects.create(quote=quote,user=user)
            return results

class Quote(models.Model):
    quote = models.TextField()
    author = models.CharField(max_length=100)
    user = models.ForeignKey(User, related_name='poster')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = Manager()
    def __repr__(self):
        return "Quote: \n{}\n{}\n{}".format(self.quote,self.author,self.user)
    def __str__(self):
        return str(self.id)

class Favorite(models.Model):
    quote = models.ForeignKey(Quote)
    user = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = Manager()
    def __str__(self):
        return str(self.id)
