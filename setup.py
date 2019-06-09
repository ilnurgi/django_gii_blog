"""
инсталятор
"""

import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='django_gii_blog',
    version='0.0.9',
    author='Ильнур Гайфутдинов',
    author_email='ilnurgi87@gmail.com',
    description='Блог',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/ilnurgi/django_gii_blog/',
    packages=setuptools.find_packages(),
    # package_data={
    #     'django_gii_blog': [
    #         'templates/admin/**/*.html',
    #         'templates/django_gii_blog/**/*.html',
    #     ]
    # }
    include_package_data=True,
)
