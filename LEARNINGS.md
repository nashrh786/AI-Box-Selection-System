# What I Learned

Through this assignment, I gained practical experience in developing a Django-based web application and implementing business logic to solve a real-world warehouse problem.

## Key Learnings

- Designed relational database models using Django ORM.
- Built relationships using ForeignKey between Orders, Products, Order Items, and Shipping Boxes.
- Implemented a service layer ('box_selector.py') to separate business logic from views.
- Developed a rule-based recommendation algorithm that evaluates:
  - Product dimensions
  - Product weight
  - Shipping box dimensions
  - Maximum weight capacity
  - Shipping cost
  - Unused box volume
- Learned how to organize a Django project using apps, templates, URLs, models, and services.
- Customized the Django Admin Panel for easier data management.
- Created automated unit tests using Django's TestCase framework.
- Improved the user interface using Bootstrap components.
- Learned the importance of testing edge cases, such as orders that exceed the capacity of all available boxes.

## Challenges Faced

- Debugging recommendation logic when the function returned 'None'.
- Improving the scoring algorithm to balance cost and packing efficiency.
- Writing meaningful unit tests for the recommendation engine.

Overall, this assignment helped me understand how to design, implement, test, and document a complete Django application.