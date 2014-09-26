from numpy.distutils.core import Extension


f90periodogram = Extension(name='f90periodogram',
                           sources=['seismo/src/periodogram.f90'],
                           extra_f90_compile_args=["-fopenmp", "-lgomp"],
                           extra_link_args=["-lgomp"])

if __name__ == "__main__":
    from numpy.distutils.core import setup
    setup(name='seismo_blobs',
          description="Compiled sources for use with seismo",
          author="Ewald Zietsman",
          author_email="ewald.zietsman@gmail.com",
          ext_modules=[f90periodogram]
          )

    # Now seismo

    import setuptools
    setuptools.setup(
        name="seismo",
        version="0.1.1",
        packages=setuptools.find_packages(),

        install_requires=['numpy>=1.9'],

        # metadata for upload to PyPI
        author="Ewald Zietsman",
        author_email="ewald.zietsman@gmail.com",
        description="Timeseries stuff for asteroseismology",
        license="MIT",
        keywords="time series frequency",
    )
