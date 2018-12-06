import setuptools

with open("README.md", "r") as fh:

    long_description = fh.read()

setuptools.setup(

     name='timelock',  

     version='0.1',

     scripts=['timelock'] ,

     author="Ber Saxon",

     author_email="auto@eagle.icu",

     description="A timeshift lockfile emulator.",

     long_description=long_description,

   long_description_content_type="text/markdown",

     url="https://eagle.icu",

     packages=setuptools.find_packages(),

     classifiers=[

         "Programming Language :: Python :: 3",

         "License :: OSI Approved :: MIT License",

         "Operating System :: OS Independent",

     ],

 )