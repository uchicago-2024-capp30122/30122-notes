# Testing

As you've no doubt discovered through working on PAs, tests are useful for ensuring that code works as expected.

We break our code into functions and classes to encapsulate functionality that we intend to reuse.
These boundaries also provide a natural place to test our code.

If you only have one big function that does everything, it can be difficult to test:

```python

def advance_all_students_with_passing_grades():
    conn = sqlite3.connect('students.db')
    c = conn.cursor()
    c.execute('''
    SELECT student.id, avg(class.grade) as average 
    FROM students JOIN classes ON students.id = classes.student_id
    GROUP BY student.id HAVING average >= 70
    ''')
    students = c.fetchall()
    for student in students:
        c.execute('UPDATE student_enrollment SET grade = grade + 1 WHERE student_id = ?', (student[0],))
    conn.commit()
    conn.close()

```

How would you test this function?  You'd need to have a database with a specific set of data in it and then run the function and check that the data was updated as expected.

If you break the function up into smaller functions, you can test each function in isolation:

```python

def get_students(conn, grade_threshold=70):
    ...

def advance_student(conn, student):
    ...

```

Now you can test each function in isolation.

By having the function take parameters, you can also test the function with different inputs.

It is also possible to test the function with a mock database connection that doesn't actually connect to a database but provides the same interface.

This is called "mocking" and is a useful technique for testing code that interacts with external systems.

## `pytest`

`pytest` is a popular testing framework for Python, and the one we've been using in class.

It is easy to use and provides a lot of useful features.  Python has a built in `unittest` module, but it is more verbose and less flexible.

`pytest` provides both a command line tool `pytest`, which you've been using, and a library that you can use to help you write tests.

## `pytest` command line tool

When you run `pytest`, it will look for files named `test_*.py` in the current directory and its subdirectories. It will then run any functions in those files that start with `test_`.

If you take a look at any PA, you'll see that there are files named `test_*.py` in the `tests` directory.  This is a common convention, but you can also place the files in other directories.

Within each `test_module1.py` file, there are functions that start with `test_`.  These are the tests that `pytest` will run.  You can include other functions in the file as helper functions, but they won't be run by `pytest`.

### Simple Example

```python
# my_module.py
from collections import namedtuple

Point = namedtuple('Point', ['x', 'y'])

def circle_contains(radius: float, center: Point, point: Point):
    return (point.x - center.x) ** 2 + (point.y - center.y) ** 2 <= radius ** 2

def points_within(radius: float, center: Point, points: list[Point]):
    """ Find all points within a circle. """
    return [point for point in points if circle_contains(radius, center, point)]
```

```python
# test_my_module.py

from my_module import circle_contains, points_within

origin = Point(0, 0)

def test_circle_contains():
    # centered at origin, radius 1
    assert circle_contains(1, origin, origin)
    assert circle_contains(1, origin, Point(.5, .5))

def test_circle_contains_edge():
    assert circle_contains(1, origin, Point(1, 0))  # on the circle

def test_circle_contains_outside():
    assert not circle_contains(1, origin, Point(1.1, 0))
```

Now running `pytest` would run the test function and report the results.

## `assert`

The `assert` statement is used to check that a condition is true.

If the condition is `True`, nothing happens. If the condition is `False`, an `AssertionError` is raised.

You can also provide a message to be printed if the assertion fails:

```python
assert 1 == 2, "1 is not equal to 2"
```

**Note:** `assert` is not a function. Using parentheses leads to confusing results because the parentheses are interpreted as a tuple.

```python
assert(1 == 2, "1 is not equal to 2")

# This is equivalent to:
assert (1 == 2, "1 is not equal to 2")

```

### Aside: Truthiness

In Python, every type has an implicit conversion to a boolean value.  This is called "truthiness".

The following values are considered "falsey":

* `False`
* `None`
* `0`   # int
* `0.0` # float
* `0j`  # complex
* ""    # empty string
* []    # empty list
* ()    # empty tuple
* {}    # empty dict
* set() # empty set

All other values are considered `True`.

```{python}
values = [False, None, 0, 0.0, 0j, "", [], (), {}, set()]
values += [True, 42, 3.14, "hello", [1, 2, 3], {"a": 1}]
for value in values:
    # notice we're using the value as a boolean expression here
    if value:
        print(f"{value} is True")
    else:
        print(f"{value} is False")
```

## Writing good tests

Above we had the tests

```python
def test_circle_contains():
    # centered at origin, radius 1
    assert circle_contains(1, origin, origin)
    assert circle_contains(1, origin, Point(.5, .5))

def test_circle_contains_edge():
    assert circle_contains(1, origin, Point(1, 0))  # on the circle

def test_circle_contains_outside():
    assert not circle_contains(1, origin, Point(1.1, 0))
```

Why not just do this?

```python

def test_circle_contains():
    # centered at origin, radius 1
    assert circle_contains(1, origin, origin)
    assert circle_contains(1, origin, Point(.5, .5))
    assert circle_contains(1, origin, Point(1, 0))  # on the circle
    assert not circle_contains(1, origin, Point(1.1, 0))
```

If the first assertion fails, the second assertion will not be run.  This makes it harder to debug the problem.

As you've no doubt noticed throughout these courses, granular tests make debugging easier. It is also easier to reason about what isn't yet being tested.

**What bugs could be lurking in the code above?**

### General Rules

* Each test should test one thing.
* Each test should be independent of the others.
* Each test should be repeatable.
* Each test should be easy to understand.

### What Tests To Write

When considering what to test, usually there are a couple of obvious cases.  For a string distance function, you might consider you need to have at least one test for when the strings are identical, and one test for when the strings are completely different.

Those are the obvious cases, it is then worth considering edge cases.  What about an empty string?  Perhaps a string with one character as well?

**(0, 1, Many)** is a good rule to consider.


### Test One Thing

If you were testing a function that summed a list of numbers, consider these two approaches:

```python
def test_sum():
    assert sum([]) == 0
    assert sum([1]) == 1
    assert sum([1, 2, 3]) == 6
    with pytest.raises(TypeError):
        sum([1, "hello"])
```

```python
def test_sum_empty():
    assert sum([]) == 0

def test_sum_one():
    assert sum([1]) == 1

def test_sum_many():
    assert sum([1, 2, 3]) == 6

def test_sum_type_error():
    with pytest.raises(TypeError):
        sum([1, "hello"])
```

By having each test focus on one thing, test failures will be more informative.

### Test Independence

Tests should be independent of each other.  This means that if one test fails, it should not affect the outcome of any other test.

This can be a challenge when testing functions that modify data or global state.

For example:

```python

def test_create_user():
    db = Database("test.db")
    db.create_user(username="alice")
    assert db.get_user(username="alice").id == 1

def test_delete_user():
    db = Database("test.db")
    db.delete_user(username="alice")
    assert db.get_user(username="alice") is None
```

These tests are not independent.  If the first test fails, the second test will fail because the database will be empty.

You'd instead likely need to do something like this:

```python
def create_test_database():
    remove_file_if_exists("test.db")
    db = Database("test.db")
    db.init_schema()
    return db

def test_create_user():
    db = create_test_database()
    db.create_user(username="alice")
    assert db.get_user(username="alice").id == 1

def test_delete_user():
    db = create_test_database()
    db.create_user(username="alice")
    db.delete_user(username="alice")
    assert db.get_user(username="alice") is None
```

Note: `test_delete_user` will fail if `create_user` doesn't work.  There's still a dependency in terms of behavior in this case, but you can see that the tests can now be run independently of one another since each starts with a blank database.

#### `pytest` Fixtures

Another way to handle this is to use `pytest` fixtures.  A fixture is a function that is run before each test.  It can be used to set up the test environment.

```python
import pytest

@pytest.fixture
def db():
    remove_file_if_exists("test.db")
    db = Database("test.db")
    db.init_schema()
    return db

# parameter names must match fixture names
def test_create_user(db):
    db.create_user(username="alice")
    assert db.get_user(username="alice").id == 1

def test_delete_user(db):
    db.create_user(username="alice")
    db.delete_user(username="alice")
    assert db.get_user(username="alice") is None
```

This is a powerful feature that can be used to set up complex test environments.

### Test Repeatability

Tests should be repeatable.  This means that if a test fails, it should be possible to run it again and get the same result.

This means that tests should not depend on external factors such as:

* The current time or date
* Random numbers
* The state of the network
* The state of the database

To reduce the chance of a test failing due to an external factor, you can use a library like `freezegun` to freeze the current time that a test sees.  The `mock` module can be used to mock out external functions so they return consistent data for the purpose of the test.

`freezegun`: <https://github.com/spulec/freezegun>

`mock`: <https://docs.python.org/3/library/unittest.mock.html>

### Test Readability

Tests should be easy to understand.  This means that the test should be written in a way that makes it clear what is being tested and what the expected result is.

Make liberal use of comments and descriptive test names to make it clear what is being tested so that when a modification to the code in the future breaks a test, it is easy to understand why.

## Test Driven Devleopment

Test Driven Development (TDD) is a software development process that involves writing tests before writing the code that will be tested.

In many ways this is how your PAs have been structured. By knowing what the expected output is, you can write tests that will fail if the code is not working correctly.

It can be useful to write tests before writing the code that will be tested.  This can help you think through the problem and make sure you understand what the code is supposed to do.

## Unit Testing vs. Integration Testing

Unit tests are tests that test individual units of code.  These are usually functions or methods.

Integration tests are tests that test how different units of code work together. It can be useful to have a mixture of both, but unit tests are usually easier to write and maintain.

In our initial example, we broke `advance_all_students_with_passing_grade` into smaller functions.  It may still make sense in some cases to test the integration of these functions to make sure that (e.g.) the list of users being returned is still in the same format expected by the `advance_student` function.

## `pytest` Features

### `pytest.fixture`

As shown above, `pytest` fixtures can be used to set up the test environment or provide data to tests.

```python
import pytest

@pytest.fixture
def user_list()
    return [
        {"name": "alice", "id": 1, "email": "alice@domain"},
        {"name": "carol", "id": 3, "email": "carol@domain"},
        {"name": "bob", "id": 2, "email": "bob@domain"},
        {"name": "diego", "id": 4, "email": "diego@otherdomain"},
    ]

def test_sort_users(user_list):
    sorted_list = sort_users(user_list)
    assert sorted_list == [
        {"name": "alice", "id": 1, "email": "alice@domain"},
        {"name": "bob", "id": 2, "email": "bob@domain"},
        {"name": "carol", "id": 3, "email": "carol@domain"},
        {"name": "diego", "id": 4, "email": "diego@otherdomain"},
    ]

def test_filter_users(user_list):
    filtered_list = filter_users(user_list, domain="domain")
    assert filtered_list == [
        {"name": "alice", "id": 1, "email": "alice@domain"},
        {"name": "bob", "id": 2, "email": "bob@domain"},
        {"name": "carol", "id": 3, "email": "carol@domain"},
    ]
```

### `pytest.raises`

It's often desirable to test that certain errors were raised.  `pytest.raises` can be used to test that a function raises an exception.

```python
def test_reject_invalid_domain():
    with pytest.raises(ValueError):
        validate_email("alice@invalid$")
```

### Parameterized Tests

Sometimes the same test needs to be run with different inputs. `pytest` provides a way to do this with parameterized tests.

```python
@pytest.mark.parametrize("str1,str2,expected", [
    ("abc", "abd", 1),
    ("abc", "abc", 0),
    ("abc", "xyz", 3),
])
def test_hamming_distance(str1, str2, expected):
    assert hamming_distance(str1, str2) == expected
```

This runs as three distinct tests in `pytest`, converting each input to a distinct test by calling the test function with the parameters.