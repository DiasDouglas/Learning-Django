# Learning Django!
## _Based on the Book 'Django 5 By Example'_

### Working with QuerySets and Managers

You can do all of this below interactivelly with:
```python manage.py shell```

#### Creating Objects

``` python 
from django.contrib.auth.models import User
from blog.models import Post

user = User.objects.get(username='admin')
post = Post(title='Another Post',
            slug='another-post',
            body='Post body.',
            author=user)
post.save()
```

1. The 'blog' app uses the 'User' model from Django auth, so we import it
2. This is our created Post model
3. We retrieve an user with the _get()_ method, matching by _username_
4. We create a new instance of Post
5. We save the newly created Post in the database using _save()_

We could have created the object and saved in a single operation using the _create()_ method:

``` python
Post.objects.create(title='One More Post',
            slug='one-more-post',
            body='Another Post body.',
            author=user)
```

We can also search for an object, and if it doesn't exist, create it first and then return it, using _get_or_create()_. It returns a tuple, where the first item is the retrieved object, and the second is a Boolean indicating if it was created or not.

```python
user, created = User.objects.get_or_create(username='another-user')
```

#### Updating Objects

```python
post_to_update = Post.objects.get(title='One More Post')
post_to_update.title = 'Updated title'
post_to_update.save()
```
