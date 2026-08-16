# Learning Django!
_Based on the Book 'Django 5 By Example'_

## Working with QuerySets and Managers

You can do all of this below interactivelly with:
```python manage.py shell```

### Creating Objects

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

### Updating Objects

To update an object, retrieve it from the database, change what you need, then call the object's _save()_ method.

```python
post_to_update = Post.objects.get(title='One More Post')
post_to_update.title = 'Updated title'
post_to_update.save()
```

### Retrieving Objects

To retrieve all objects of a particular model:

```python
all_posts = Post.objects.all()
```

Above, '_objects_' is a manager. In Django, each model has at least one manager, and 'objects' is how the default one is called. The return type of a model manager operation is a **QuerySet**. It returns something like this:

```
<QuerySet [<model>: <model object's to_string>, ...]>
```

for example, if we had two Posts in a database:

```
<QuerySet [<Post: This is a post title>, <Post: This is a title from a different post>]>
```

### Filtering Objects

The manager's **_filter()_** method is used to filter a QuerySet. It specifies the content of a SQL **WHERE** clause by using field lookups.

For example:

```python
Post.objects.filter(title='Another Post')
```

This searches for an exact match, so if there's any post with 'Another Post' as the title, it will be returned.

We can review the generated SQL of a QuerySet accessing the QuerySet's instance **_query_** attribute:

```python
posts = Post.objects.filter(title='Another Post')
print(posts.query)
```

And this would show the full SQL produced, for example:

```sql
SELECT “blog_post”.”id”, “blog_post”.”title”, “blog_post”.”slug”, “blog_ post”.”author_id”, “blog_post”.”body”, “blog_post”.”publish”, “blog_ post”.”created”, “blog_post”.”updated”, “blog_post”.”status” FROM “blog_post” WHERE “blog_post”.”title” = Another Post
```

### Using Field Lookups

There are multiple field lookup types. The previous example uses an exact match for the provided title. It is the same as the following one:

```python
Post.objects.filter(title__exact='Another Post')
```

But as we didn't provided any lookup type the first time, is assumed that it needs to be exact.

Sometimes we want to be case-insensitive, so we can use:

```python
Post.objects.filter(title__iexact='another post')
```

Another lookup we can use is the partial match, that works as a containment test. The **_contains_** lookup works like the SQL's **_LIKE_** operator:

```python
# Equivalent of 'SELECT * FROM Posts WHERE title LIKE %Another%'
Post.objects.filter(title__contains='Another')
```

A case-insensive version of this is:

```python
Post.objects.filter(title__icontains='another')
```

When we want to search if, for example, the ID of an object in in a list, we can use the **_in_** lookup:

```python
Post.objects.filter(id__in=[1, 3])
```

In this case, it would retrive the posts with ID 1 and 3, if they exist.

Let's check other examples.
The following example is the 'greater than' lookup:

```python
Post.objects.filter(id__gt=3)
```

And the next one, 'greater than or equal':

```python
Post.objects.filter(id__gte=3)
```

The following example is the 'less than' lookup:

```python
Post.objects.filter(id__lt=3)
```

And the next one, 'less than or equal':

```python
Post.objects.filter(id__lte=3)
```

To search for text that starts with a particular string, we can use the case sensitive or case insensitive version of **_startswith_**:

```python
Post.objects.filter(title__istartswith='another')
```

And the opposite, **_endswith_**:

```python
Post.objects.filter(title__iendswith='post')
```

There's a bunch of field lookups for date as well:

```python
from datetime import date
Post.objects.filter(publish__date=date(2026, 8, 15))
```

We can filter by year...

```python
Post.objects.filter(publish__year=2026)
```

Month...

```python
Post.objects.filter(publish__month=8)
```

Or day.

```python
Post.objects.filter(publish__day=15)
```

And the lookups can be chained. For example, this is a lookup for a value greater than a given date:

```python
Post.objects.filter(publish__date__gt=date(2026, 8, 15))
```

To lookup related object fields, the two-underscore notation is also used. The next example is the retrieval of all posts written by the user with the username 'admin':

```python
# 'author' is the field (in this case, a foreign key) in Post. 'username' is a property of User.
Post.objects.filter(author__username='admin')
```

And we can keep on chaining:

```python
Post.objects.filter(author__username__startswith='ad')
```

We can also filter by multiple fields:

```python
Post.objects.filter(author__username__startswith='ad', publish__year=2026)
```

### Chaining Filters

As the result of a filtered QuerySet is another QuerySet, we can chain them together.

```python
Post.objects.filter(publish__year=2026).filter(author__username='admin')
```

### Excluding Objects

We can exclude certain results from our QuerySet as well:

```python
Post.objects.filter(publish__year=2026).exclude(title__startswith='Another')
```

### Ordering Objects

The default order is defined in the ordering option of the model's _Meta_ (check **models.py**), but it can be overrided by using the **_order_by_** method of the manager. It can be done in ascending, descending or in random order, and it can also support multiple fields:

```python
# Ascending order is implied here
Post.objects.order_by('title')

# Descending order is indicated with a minus sign
Post.objects.order_by('-title')

# Order by multiple fields: in this case, order by author, then order by title
Post.objects.order_by('author', 'title')

# Return in a random order
Post.object.order_by('?')
```

### Limiting QuerySets

The number of results can be limited. The following example translates the SQL **_LIMIT_** clause.

```python
# "SELECT * FROM Post LIMIT 5"
Post.objects.all()[:5]
```

We can also translate the **_OFFSET_** clause, and even combine with limit:

```python
# "SELECT * FROM Post OFFSET 3 LIMIT 5"
# That means, it returns from the 3th result until the 5th
Post.objects.all()[3:5]
```

For a single object, the index can be used instead of slicing:

```python
Post.objects.all()[3]
```

### Counting Objects

For counting the total number of objects returned, we can use the **_count()_** method:

```python
Post.objects.filter(id_lt=3).count()
```

### Check if an Object Exists

We use the **_exists()_** method:

```python
Post.objects.filter(title__startswith='Why').exists()
```

### Deleting Objects

Delete an object (and any consequent object due to dependent relashionship for Foreign Key) is done with the **_delete()_** method.

```python
post = Post.objects.get(id=1)
post.delete()
```

### Complex Lookups with Q Objects

All the lookups we used above are joined with a SQL 'AND'. 
If we want something more complex, like an 'OR', we can use Q objects like this:

```python
from django.db.models import Q

starts_who = Q(title__istartswith='who')
starts_why = Q(title__istartswith='why')

# The OR statement
Post.objects.filter(starts_who | starts_why) 
```

### When QuerySets Are Evaluated

QuerySets will usually return another unevaluated QuerySet. It is only evaluated in these situations:

* The first time you iterate over them
* When you pickle or cache them
* When you call repr() or len() on them
* When you explicitly call list() on them
* When you test them in a statement, such as bool(), or, and, or if
